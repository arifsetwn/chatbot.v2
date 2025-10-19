# Logika Chatbot - Dokumentasi Teknis

## Overview

Chatbot Pembelajaran Algoritma menggunakan sistem deteksi pertanyaan yang cerdas untuk memberikan respons yang sesuai dengan konteks dan kebutuhan mahasiswa. Sistem ini dirancang dengan pendekatan **Guided Learning** menggunakan **Socratic Method**.

## Arsitektur Sistem

```
User Question
     ↓
Question Detector (deteksi jenis pertanyaan)
     ↓
Response Strategy (tentukan pendekatan)
     ↓
Code Analyzer (jika ada kode)
     ↓
Enhanced System Prompt (prompt yang diperkaya)
     ↓
LLM Generation (Gemini/OpenAI)
     ↓
Response dengan guidance
```

## Komponen Utama

### 1. Question Detector (`utils/question_detector.py`)

**Fungsi**: Mendeteksi jenis pertanyaan dan menentukan strategi respons yang tepat.

**Tipe Pertanyaan yang Dideteksi**:
- `CONCEPT`: Pertanyaan tentang konsep/teori algoritma
- `CODE`: Permintaan implementasi kode
- `DEBUGGING`: Pertanyaan troubleshooting/error
- `HOMEWORK`: Pertanyaan tugas/ujian (DITOLAK)
- `SIMULATION`: Permintaan simulasi/trace algoritma
- `GENERAL`: Pertanyaan umum

**Cara Kerja**:
```python
from utils.question_detector import QuestionDetector

detector = QuestionDetector()

# Deteksi pertanyaan
result = detector.detect(
    question="Jelaskan cara kerja binary search",
    has_uploaded_file=False
)

# Result:
{
    "type": QuestionType.CONCEPT,
    "confidence": 0.85,
    "is_homework": False,
    "needs_code_analysis": False,
    "reasoning": "Terdeteksi sebagai pertanyaan concept | Score: concept: 0.85"
}
```

**Strategi Respons**:
```python
strategy = detector.get_response_strategy(result)

# Strategy:
{
    "approach": "guided_explanation",
    "should_reject": False,
    "guidance": "Jelaskan konsep dengan:\n1. Definisi sederhana...\n2. Cara kerja step-by-step..."
}
```

**Keyword Patterns**:
- **Concept**: "apa itu", "jelaskan", "pengertian", "cara kerja", "mengapa"
- **Code**: "kode", "implementasi", "buat", "tulis", "contoh kode"
- **Debugging**: "error", "bug", "salah", "tidak jalan", "perbaiki"
- **Homework**: "tugas", "ujian", "soal", "deadline", "tolong buatkan"
- **Simulation**: "simulasi", "trace", "step by step", "jalankan"

### 2. Code Analyzer (`utils/code_analyzer.py`)

**Fungsi**: Parsing dan analisis kode Python yang diupload mahasiswa.

**Analisis yang Dilakukan**:
1. **Syntax Validation**: Check apakah kode valid
2. **Structure Analysis**: Identifikasi fungsi, class, imports
3. **Algorithm Detection**: Deteksi algoritma yang digunakan
4. **Complexity Analysis**: Estimasi time/space complexity
5. **Learning Points**: Generate insights untuk pembelajaran
6. **Guided Questions**: Generate pertanyaan pemandu

**Contoh Penggunaan**:
```python
from utils.code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()

# Analyze code
code = """
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
"""

result = analyzer.analyze_code(code)
```

**Output Analisis**:
```python
{
    "success": True,
    "is_valid": True,
    "syntax_errors": [],
    "structure": {
        "functions": [
            {
                "name": "binary_search",
                "args": ["arr", "target"],
                "is_recursive": False,
                "line": 1
            }
        ],
        "classes": [],
        "imports": []
    },
    "algorithms": ["Binary Search"],
    "complexity_indicators": {
        "nested_loops": 0,
        "total_loops": 1,
        "estimated_time_complexity": "O(log n)"
    },
    "learning_points": [
        "✓ Kode terstruktur dengan 1 fungsi: binary_search",
        "✓ Mengimplementasikan: Binary Search",
        "📊 Estimasi kompleksitas: O(log n)"
    ],
    "suggestions": []
}
```

**Algoritma yang Dapat Dideteksi**:
- Binary Search
- Linear Search
- Bubble Sort
- Selection Sort
- Insertion Sort
- Quick Sort
- Merge Sort
- Recursion
- Dynamic Programming
- Stack/Queue operations

**Guided Questions Generation**:
```python
questions = analyzer.get_guided_questions(result)
# [
#     "Mengapa binary search harus menggunakan array yang sudah terurut?",
#     "Apa yang terjadi jika array tidak terurut?",
#     "Coba jelaskan dengan kata-kata sendiri, apa yang dilakukan setiap fungsi?"
# ]
```

### 3. Algorithm Simulator (`utils/algorithm_simulator.py`)

**Fungsi**: Simulasi eksekusi algoritma step-by-step untuk visualisasi pembelajaran.

**Algoritma yang Didukung**:
- `bubble_sort`
- `selection_sort`
- `insertion_sort`
- `binary_search`
- `linear_search`
- `factorial` (recursive)
- `fibonacci`

**Contoh Penggunaan**:
```python
from utils.algorithm_simulator import AlgorithmSimulator

sim = AlgorithmSimulator()

# Simulate bubble sort
result = sim.simulate("bubble_sort", [5, 2, 8, 1, 9])
```

**Output Simulasi**:
```python
{
    "success": True,
    "algorithm": "Bubble Sort",
    "steps": [
        {
            "step": 0,
            "description": "Array awal: [5, 2, 8, 1, 9]",
            "array": [5, 2, 8, 1, 9],
            "explanation": "Bubble sort akan membandingkan elemen bersebelahan..."
        },
        {
            "step": 1,
            "description": "Iterasi 1, Posisi 0: 2 < 5 → SWAP",
            "array": [2, 5, 8, 1, 9],
            "comparisons": 1,
            "swaps": 1,
            "action": "swap",
            "highlight": [0, 1]
        },
        # ... more steps
    ],
    "result": [1, 2, 5, 8, 9],
    "summary": "Selesai dalam 15 langkah, 10 perbandingan, 6 swap",
    "complexity": {
        "time": "O(n²)",
        "space": "O(1)"
    }
}
```

**Simulasi Binary Search**:
```python
result = sim.simulate("binary_search", [1, 3, 5, 7, 9, 11], target=7)

# Steps akan menunjukkan:
# - Iterasi 1: low=0, high=5, mid=2, arr[2]=5 < 7 → cari kanan
# - Iterasi 2: low=3, high=5, mid=4, arr[4]=9 > 7 → cari kiri
# - Iterasi 3: low=3, high=3, mid=3, arr[3]=7 → FOUND!
```

**Simulasi Rekursi (Factorial)**:
```python
result = sim.simulate("factorial", 5)

# Visualization:
# factorial(5) dipanggil
#   factorial(4) dipanggil
#     factorial(3) dipanggil
#       factorial(2) dipanggil
#         factorial(1) dipanggil
#         Base case: factorial(1) = 1
#       factorial(2) = 2 * 1 = 2
#     factorial(3) = 3 * 2 = 6
#   factorial(4) = 4 * 6 = 24
# factorial(5) = 5 * 24 = 120
```

## Integrasi di Chat Interface

### Flow Lengkap

1. **User Input**:
   ```
   User mengetik: "Tolong buatkan kode bubble sort untuk tugas saya"
   ```

2. **Question Detection**:
   ```python
   detection = question_detector.detect(prompt, has_uploaded_file)
   # Result: type=HOMEWORK, confidence=0.9, is_homework=True
   ```

3. **Strategy Determination**:
   ```python
   strategy = question_detector.get_response_strategy(detection)
   # Result: should_reject=True, approach="reject_politely"
   ```

4. **Response Generation**:
   - Jika `should_reject=True` → Tampilkan pesan penolakan yang ramah
   - Jika tidak → Enhance system prompt dengan guidance strategy
   - Jika ada kode → Tambahkan hasil analisis ke prompt
   - Generate response via LLM

5. **Display**:
   - Tampilkan response dengan typing effect
   - Tambahkan metadata (model, question type)

### Enhanced System Prompt

System prompt diperkaya dengan:

```
ORIGINAL SYSTEM PROMPT
+
STRATEGI RESPONS:
[Guidance dari question detector]
+
ANALISIS KODE USER: (jika ada)
[Hasil dari code analyzer]
+
PERTANYAAN PEMANDU:
[Guided questions untuk Socratic method]
```

### Penolakan Tugas/Ujian

Ketika terdeteksi homework:
```markdown
🚫 **Maaf, saya tidak bisa membantu mengerjakan tugas atau ujian secara langsung.**

Ini adalah chatbot pembelajaran yang dirancang untuk **membimbing proses berpikir**, 
bukan memberikan jawaban siap pakai.

**Yang bisa saya lakukan:**
- Menjelaskan **konsep** yang mendasari tugas kamu
- Membantu kamu **memahami algoritma** yang relevan
- Memberikan **pertanyaan pemandu** untuk arahkan cara berpikir
- Diskusi tentang **pendekatan** yang bisa dicoba

**Coba tanyakan seperti ini:**
- "Jelaskan konsep [topik] yang dipakai dalam tugas ini"
- "Bagaimana cara kerja algoritma [nama algoritma]?"
- "Apa pendekatan yang bisa saya pakai untuk soal seperti ini?"

Mari belajar bersama! 🎓
```

## File Upload & Code Analysis Flow

1. **User Upload File**:
   - Validate: format (.py, .txt), size (< 1MB)
   - Save to `uploads/` directory
   - Read content

2. **Automatic Analysis**:
   ```python
   code_content = uploaded_file.getvalue().decode("utf-8")
   analysis = code_analyzer.analyze_code(code_content)
   st.session_state.code_analysis = analysis
   ```

3. **Display Analysis Summary** (sidebar):
   - ✓ Kode valid / ❌ Syntax error
   - Algoritma yang terdeteksi
   - Kompleksitas
   - Learning points

4. **Enhance Chat Context**:
   - Setiap chat setelah upload akan include code analysis
   - LLM mendapat informasi tentang kode user
   - Dapat memberikan feedback spesifik

## Gaya Komunikasi Santai

System prompt dirancang untuk gaya komunikasi santai:

**Prinsip**:
- Gunakan "kamu" bukan "Anda"
- Bahasa sehari-hari, hindari formal berlebihan
- Emoji secukupnya untuk friendly
- Analogi dari kehidupan nyata
- Pertanyaan terbuka untuk engage

**Contoh Buruk**:
```
"Binary search adalah algoritma pencarian yang bekerja pada array terurut 
dengan kompleksitas waktu O(log n) melalui pendekatan divide and conquer."
```

**Contoh Bagus**:
```
"Binary search itu mirip kayak kamu nyari kata di kamus. 
Gak mungkin kan buka dari halaman 1? Pasti langsung buka tengah, 
terus kalau kata yang dicari 'sebelum' tengah, fokus ke kiri. 
Kalau 'setelah' tengah, fokus ke kanan. Gitu terus sampai ketemu! 🎯

Nah, konsep 'bagi dua' ini yang bikin binary search super cepet. 
Coba bayangin, kalau ada 1000 data, paling cuma butuh 10 langkah! 
Keren kan? 

Udah paham konsepnya? Mau coba trace dengan contoh sederhana?"
```

## Testing & Validation

### Test Question Detector
```bash
python utils/question_detector.py
```

Output: Test berbagai jenis pertanyaan dengan skor deteksi

### Test Code Analyzer
```bash
python utils/code_analyzer.py
```

Output: Analisis sample code binary search

### Test Algorithm Simulator
```bash
python utils/algorithm_simulator.py
```

Output: Simulasi bubble sort, binary search, factorial

## Error Handling

### Syntax Error in Uploaded Code
```python
if not analysis["is_valid"]:
    st.sidebar.error("❌ Kode memiliki syntax error")
    for err in analysis["syntax_errors"]:
        st.sidebar.error(f"Line {err['line']}: {err['message']}")
```

### Question Detection Failure
- Fallback ke `QuestionType.GENERAL`
- Confidence rendah → respons open conversation

### Simulation Error
```python
if not result["success"]:
    # Tampilkan error message
    # Suggest supported algorithms
```

## Performance Optimization

1. **Caching**:
   ```python
   @st.cache_resource
   def init_question_detector():
       return QuestionDetector()
   ```

2. **Session State**:
   - Code analysis disimpan di session state
   - Tidak perlu re-analyze setiap chat

3. **Lazy Loading**:
   - Simulator hanya dipanggil saat diminta simulasi

## Future Enhancements

### Fase 2 (Planned)
- [ ] Visual algorithm simulation (animated)
- [ ] More algorithms support
- [ ] Code improvement suggestions
- [ ] Performance benchmarking
- [ ] Multi-language support (Java, C++)

### Fase 3 (Future)
- [ ] Interactive code editor
- [ ] Real-time collaboration
- [ ] Peer review system
- [ ] Gamification (badges, leaderboard)

## Troubleshooting

**Problem**: Question detector salah klasifikasi
- **Solution**: Update keyword patterns di `question_detector.py`
- Tambah training examples
- Adjust confidence threshold

**Problem**: Code analyzer tidak detect algorithm
- **Solution**: Tambah pattern di `_detect_algorithms()`
- Improve regex patterns
- Add more algorithm signatures

**Problem**: Simulation terlalu lambat
- **Solution**: Limit steps untuk array besar
- Add early termination
- Optimize loop logic

## Kesimpulan

Sistem Logika Chatbot ini mengimplementasikan:
✅ Deteksi jenis pertanyaan otomatis
✅ Guided learning dengan Socratic method
✅ Code parsing dan analisis
✅ Algorithm simulation step-by-step
✅ Penolakan tugas/ujian secara sopan
✅ Gaya komunikasi santai dan membimbing

Semua komponen terintegrasi untuk memberikan pengalaman pembelajaran yang efektif dan engaging! 🎓
