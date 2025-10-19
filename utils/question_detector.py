"""
Question Type Detector
Mendeteksi jenis pertanyaan dari user untuk memberikan respons yang sesuai
"""
import re
from enum import Enum
from typing import Dict, Any, List


class QuestionType(Enum):
    """Tipe pertanyaan yang dapat dideteksi"""
    CONCEPT = "concept"  # Pertanyaan tentang konsep/teori
    CODE = "code"  # Pertanyaan tentang implementasi kode
    DEBUGGING = "debugging"  # Pertanyaan debugging/troubleshooting
    HOMEWORK = "homework"  # Pertanyaan tugas/ujian (harus ditolak)
    SIMULATION = "simulation"  # Minta simulasi/trace algoritma
    GENERAL = "general"  # Pertanyaan umum


class QuestionDetector:
    """Deteksi jenis pertanyaan dari input user"""
    
    # Keywords untuk setiap tipe pertanyaan
    CONCEPT_KEYWORDS = [
        r'\b(apa itu|jelaskan|pengertian|definisi|konsep|cara kerja|prinsip|teori)\b',
        r'\b(bagaimana.*bekerja|kenapa|mengapa|kapan digunakan)\b',
        r'\b(perbedaan|perbandingan|kelebihan|kekurangan|vs)\b',
        r'\b(time complexity|space complexity|big o|kompleksitas)\b',
    ]
    
    CODE_KEYWORDS = [
        r'\b(kode|code|implementasi|program|script|syntax)\b',
        r'\b(buat|bikin|tulis|write|coding|ngoding)\b',
        r'\b(contoh.*kode|code.*example|sample.*code)\b',
        r'\b(gimana.*ngoding|cara.*coding|how.*to.*code)\b',
    ]
    
    DEBUGGING_KEYWORDS = [
        r'\b(error|bug|salah|tidak jalan|gak jalan|gak bisa)\b',
        r'\b(perbaiki|fix|benerin|debug|troubleshoot)\b',
        r'\b(kenapa.*error|why.*error|mengapa.*error)\b',
        r'\b(stack trace|exception|traceback)\b',
        r'\b(tidak.*bekerja|doesn\'t work|gak.*work)\b',
    ]
    
    HOMEWORK_KEYWORDS = [
        r'\b(tugas|homework|assignment|pr|pekerjaan rumah)\b',
        r'\b(ujian|exam|test|quiz|kuis|uts|uas)\b',
        r'\b(soal|latihan|exercise|problem set)\b',
        r'\b(deadline|dikumpulkan|submit|kumpul)\b',
        r'\b(nilai|grade|skor|point)\b',
        r'\b(tolong.*buatkan|bikinin|jawaban|solution)\b',
    ]
    
    SIMULATION_KEYWORDS = [
        r'\b(simulasi|simulate|trace|jalankan|run through)\b',
        r'\b(step.*by.*step|langkah.*demi.*langkah|tahap.*tahap)\b',
        r'\b(proses|eksekusi|execution|running)\b',
        r'\b(trace.*tabel|trace.*table|tabel.*trace)\b',
        r'\b(contoh.*proses|example.*process|show.*how)\b',
    ]
    
    # Indikator upload file kode
    CODE_UPLOAD_INDICATORS = [
        r'(file|kode|program|script).*(ini|itu|yang|uploaded)',
        r'(ini|itu).*kode',
        r'lihat.*kode',
        r'analisa.*kode',
        r'review.*kode',
    ]
    
    def __init__(self):
        """Initialize detector"""
        pass
    
    def detect(self, question: str, has_uploaded_file: bool = False) -> Dict[str, Any]:
        """
        Deteksi jenis pertanyaan
        
        Args:
            question: Pertanyaan dari user
            has_uploaded_file: Apakah user upload file kode
            
        Returns:
            Dict dengan:
            - type: QuestionType
            - confidence: float (0-1)
            - is_homework: bool
            - needs_code_analysis: bool
            - reasoning: str (penjelasan deteksi)
        """
        question_lower = question.lower()
        
        # Check homework first (highest priority)
        homework_score = self._calculate_score(question_lower, self.HOMEWORK_KEYWORDS)
        is_homework = homework_score > 0.3
        
        # Check other types
        concept_score = self._calculate_score(question_lower, self.CONCEPT_KEYWORDS)
        code_score = self._calculate_score(question_lower, self.CODE_KEYWORDS)
        debug_score = self._calculate_score(question_lower, self.DEBUGGING_KEYWORDS)
        simulation_score = self._calculate_score(question_lower, self.SIMULATION_KEYWORDS)
        
        # Boost debugging score if file uploaded
        if has_uploaded_file:
            debug_score += 0.3
            code_score += 0.2
        
        # Check if question mentions uploaded code
        needs_code_analysis = has_uploaded_file or self._check_code_upload_mention(question_lower)
        
        # Determine question type
        scores = {
            QuestionType.HOMEWORK: homework_score,
            QuestionType.DEBUGGING: debug_score,
            QuestionType.SIMULATION: simulation_score,
            QuestionType.CODE: code_score,
            QuestionType.CONCEPT: concept_score,
        }
        
        # Get highest score
        if max(scores.values()) < 0.2:
            question_type = QuestionType.GENERAL
            confidence = 0.5
        else:
            question_type = max(scores, key=scores.get)
            confidence = scores[question_type]
        
        # Build reasoning
        reasoning = self._build_reasoning(
            question_type, 
            scores, 
            has_uploaded_file, 
            needs_code_analysis
        )
        
        return {
            "type": question_type,
            "confidence": min(confidence, 1.0),
            "is_homework": is_homework,
            "needs_code_analysis": needs_code_analysis,
            "reasoning": reasoning,
            "scores": {k.value: v for k, v in scores.items()}
        }
    
    def _calculate_score(self, text: str, keyword_patterns: List[str]) -> float:
        """Calculate matching score for keyword patterns"""
        matches = 0
        for pattern in keyword_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
        
        # Normalize to 0-1
        if len(keyword_patterns) == 0:
            return 0.0
        return min(matches / len(keyword_patterns), 1.0)
    
    def _check_code_upload_mention(self, text: str) -> bool:
        """Check if question mentions uploaded code"""
        for pattern in self.CODE_UPLOAD_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _build_reasoning(
        self, 
        question_type: QuestionType, 
        scores: Dict[QuestionType, float],
        has_uploaded_file: bool,
        needs_code_analysis: bool
    ) -> str:
        """Build explanation for detection"""
        reasoning_parts = []
        
        # Main type
        reasoning_parts.append(f"Terdeteksi sebagai pertanyaan {question_type.value}")
        
        # Top scores
        top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
        if top_scores[0][1] > 0:
            score_str = ", ".join([f"{qt.value}: {score:.2f}" for qt, score in top_scores])
            reasoning_parts.append(f"Score: {score_str}")
        
        # File upload
        if has_uploaded_file:
            reasoning_parts.append("File kode telah diupload")
        
        if needs_code_analysis:
            reasoning_parts.append("Memerlukan analisis kode")
        
        return " | ".join(reasoning_parts)
    
    def get_response_strategy(self, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tentukan strategi respons berdasarkan deteksi
        
        Returns:
            Dict dengan:
            - approach: str (cara merespons)
            - should_reject: bool (apakah harus menolak)
            - guidance: str (panduan untuk LLM)
        """
        q_type = detection_result["type"]
        is_homework = detection_result["is_homework"]
        needs_code = detection_result["needs_code_analysis"]
        
        # Reject homework questions
        if is_homework:
            return {
                "approach": "reject_politely",
                "should_reject": True,
                "guidance": """TOLAK permintaan ini dengan sopan. 
Jelaskan bahwa chatbot tidak boleh memberikan jawaban langsung untuk tugas/ujian.
Tawarkan untuk menjelaskan KONSEP yang mendasari tugas tersebut.
Gunakan nada yang ramah dan supportif, bukan menghakimi."""
            }
        
        # Different approaches for different types
        strategies = {
            QuestionType.CONCEPT: {
                "approach": "guided_explanation",
                "should_reject": False,
                "guidance": """Jelaskan konsep dengan:
1. Definisi sederhana dengan analogi kehidupan sehari-hari
2. Bagaimana cara kerjanya step-by-step
3. Kapan digunakan dan kenapa
4. Berikan contoh kasus penggunaan (BUKAN kode lengkap)
5. Ajukan pertanyaan pemandu untuk memastikan pemahaman"""
            },
            QuestionType.CODE: {
                "approach": "guided_coding",
                "should_reject": False,
                "guidance": """Bimbing user untuk coding sendiri:
1. Tanyakan: apa yang sudah dicoba?
2. Pecah masalah menjadi langkah-langkah kecil
3. Berikan PSEUDOCODE atau struktur umum, BUKAN kode lengkap
4. Tunjukkan konsep penting yang perlu dipahami
5. Beri petunjuk untuk setiap langkah, bukan solusi langsung"""
            },
            QuestionType.DEBUGGING: {
                "approach": "guided_debugging",
                "should_reject": False,
                "guidance": """Bimbing debugging dengan Socratic method:
1. Tanyakan: apa error message yang muncul?
2. Tanyakan: apa yang diharapkan vs yang terjadi?
3. Tanyakan: sudah coba apa saja?
4. Bantu identifikasi AREA masalah, bukan perbaiki langsung
5. Ajarkan strategi debugging yang bisa digunakan lagi"""
            },
            QuestionType.SIMULATION: {
                "approach": "step_by_step_trace",
                "should_reject": False,
                "guidance": """Simulasikan algoritma step-by-step:
1. Jelaskan input dan kondisi awal
2. Trace SETIAP langkah dengan tabel atau deskripsi tekstual
3. Tunjukkan perubahan variabel di setiap iterasi
4. Jelaskan MENGAPA setiap langkah dilakukan
5. Kesimpulan: apa yang terjadi dan mengapa"""
            },
            QuestionType.GENERAL: {
                "approach": "open_conversation",
                "should_reject": False,
                "guidance": """Respons natural dan helpful:
1. Jawab pertanyaan dengan friendly
2. Jika relevan dengan algoritma, arahkan ke topik pembelajaran
3. Jika tidak jelas, tanyakan klarifikasi
4. Tetap dalam konteks pembelajaran algoritma"""
            }
        }
        
        strategy = strategies.get(q_type, strategies[QuestionType.GENERAL])
        
        # Add code analysis guidance if needed
        if needs_code:
            strategy["guidance"] += """

ANALISIS KODE:
- Baca kode yang diupload dengan teliti
- Identifikasi struktur, logika, dan algoritma yang digunakan
- Berikan feedback konstruktif dengan pertanyaan pemandu
- JANGAN langsung perbaiki, tapi arahkan user untuk menemukan masalah"""
        
        return strategy


# Example usage and testing
if __name__ == "__main__":
    detector = QuestionDetector()
    
    # Test cases
    test_questions = [
        ("Jelaskan apa itu binary search", False),
        ("Buatkan kode untuk sorting", False),
        ("Error di kode saya, kenapa ya?", True),
        ("Tolong kerjakan tugas saya tentang bubble sort", False),
        ("Simulasikan bubble sort dengan array [5,2,8,1]", False),
        ("Halo chatbot", False),
    ]
    
    print("=" * 60)
    print("QUESTION DETECTOR TEST")
    print("=" * 60)
    
    for question, has_file in test_questions:
        print(f"\nPertanyaan: {question}")
        print(f"Has file: {has_file}")
        
        result = detector.detect(question, has_file)
        strategy = detector.get_response_strategy(result)
        
        print(f"Type: {result['type'].value}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Is Homework: {result['is_homework']}")
        print(f"Needs Code Analysis: {result['needs_code_analysis']}")
        print(f"Approach: {strategy['approach']}")
        print(f"Should Reject: {strategy['should_reject']}")
        print("-" * 60)
