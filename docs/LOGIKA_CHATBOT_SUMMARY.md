# Implementasi Logika Chatbot - Summary

## ✅ Tasks Completed

Semua 6 tasks di bagian "Logika Chatbot" telah selesai diimplementasikan:

### 1. ✅ Deteksi Jenis Pertanyaan
**File**: `utils/question_detector.py`

**Implementasi**:
- Deteksi 6 tipe pertanyaan: CONCEPT, CODE, DEBUGGING, HOMEWORK, SIMULATION, GENERAL
- Keyword pattern matching dengan regex
- Confidence scoring (0-1)
- Response strategy generation

**Features**:
- Deteksi homework/tugas untuk rejection
- Boost score jika ada file upload
- Reasoning explanation untuk debugging

**Example**:
```python
detector.detect("Jelaskan binary search", False)
# → type=CONCEPT, confidence=0.85
```

---

### 2. ✅ Guided Learning Approach
**File**: `data/system_prompt.txt` (updated)

**Implementasi**:
- Socratic method - ajukan pertanyaan pemandu
- Jangan berikan jawaban langsung
- Pecah masalah kompleks jadi langkah kecil
- Analogi dari kehidupan sehari-hari

**Strategi per Tipe**:
- **CONCEPT**: Guided explanation (definisi → cara kerja → contoh → pertanyaan)
- **CODE**: Guided coding (pseudocode, bukan kode lengkap)
- **DEBUGGING**: Guided debugging (bantu identifikasi area, bukan perbaiki)
- **SIMULATION**: Step-by-step trace dengan penjelasan

**Example System Guidance**:
```
"Bimbing user untuk coding sendiri:
1. Tanyakan: apa yang sudah dicoba?
2. Pecah masalah menjadi langkah-langkah kecil
3. Berikan PSEUDOCODE, BUKAN kode lengkap"
```

---

### 3. ✅ Simulasi Langkah Algoritma
**File**: `utils/algorithm_simulator.py`

**Implementasi**:
- Simulator untuk 7 algoritma umum
- Step-by-step execution trace
- Textual visualization
- Complexity information

**Supported Algorithms**:
1. **Bubble Sort** - dengan comparisons & swaps count
2. **Selection Sort** - dengan min_idx tracking
3. **Insertion Sort** - dengan key insertion process
4. **Binary Search** - dengan low/mid/high visualization
5. **Linear Search** - dengan sequential check
6. **Factorial** - recursive call stack visualization
7. **Fibonacci** - iterative sequence building

**Output Format**:
```python
{
    "steps": [
        {
            "step": 1,
            "description": "Iterasi 1, Posisi 0: 2 < 5 → SWAP",
            "array": [2, 5, 8, 1, 9],
            "explanation": "Menukar karena 2 lebih kecil",
            "highlight": [0, 1]
        }
    ],
    "result": [1, 2, 5, 8, 9],
    "summary": "Selesai dalam 15 langkah",
    "complexity": {"time": "O(n²)", "space": "O(1)"}
}
```

**Usage in Chat**:
- User bisa request: "Simulasikan bubble sort untuk [5,2,8,1]"
- Bot akan trace setiap langkah dengan penjelasan

---

### 4. ✅ Penolakan Tugas/Ujian
**File**: `pages/1_Chat.py` (homework rejection logic)

**Implementasi**:
- Automatic detection via keyword patterns
- Polite rejection message
- Redirect ke pembelajaran konsep
- Suggest alternative questions

**Keywords yang Memicu Rejection**:
- "tugas", "homework", "assignment"
- "ujian", "exam", "test", "quiz", "UTS", "UAS"
- "deadline", "dikumpulkan", "submit"
- "tolong buatkan", "bikinin", "jawaban"

**Rejection Message**:
```markdown
🚫 Maaf, saya tidak bisa membantu mengerjakan tugas atau ujian.

**Yang bisa saya lakukan:**
- Menjelaskan KONSEP yang mendasari tugas
- Membantu MEMAHAMI algoritma yang relevan
- Memberikan PERTANYAAN PEMANDU
- Diskusi tentang PENDEKATAN

**Coba tanyakan seperti ini:**
- "Jelaskan konsep [topik] yang dipakai dalam tugas ini"
- "Bagaimana cara kerja algoritma [nama algoritma]?"
```

**Confidence Threshold**: > 0.3 untuk homework detection

---

### 5. ✅ Parsing & Analisis Kode
**File**: `utils/code_analyzer.py`

**Implementasi**:
- Python AST (Abstract Syntax Tree) parsing
- Syntax validation
- Structure analysis (functions, classes, imports)
- Algorithm detection via patterns
- Complexity estimation
- Learning points generation
- Guided questions generation

**Analysis Output**:
```python
{
    "is_valid": True,
    "structure": {
        "functions": [{
            "name": "binary_search",
            "args": ["arr", "target"],
            "is_recursive": False
        }],
        "classes": [],
        "imports": []
    },
    "algorithms": ["Binary Search"],
    "complexity_indicators": {
        "nested_loops": 0,
        "estimated_time_complexity": "O(log n)"
    },
    "learning_points": [
        "✓ Kode terstruktur dengan 1 fungsi",
        "✓ Mengimplementasikan: Binary Search",
        "📊 Estimasi kompleksitas: O(log n)"
    ],
    "suggestions": [
        "Pertimbangkan menambahkan docstring",
        "Gunakan nama variabel lebih deskriptif"
    ]
}
```

**Algorithms yang Dapat Dideteksi**:
- Sorting: Bubble, Selection, Insertion, Quick, Merge
- Searching: Binary, Linear
- Recursion, Dynamic Programming
- Stack, Queue operations

**Guided Questions**:
```python
[
    "Mengapa binary search harus menggunakan array terurut?",
    "Berapa kali perbandingan untuk n elemen?",
    "Coba jelaskan apa yang dilakukan setiap fungsi?"
]
```

**Integration**:
- Auto-analyze saat file diupload
- Hasil disimpan di `st.session_state.code_analysis`
- Ditampilkan di sidebar dengan expandable details
- Digunakan untuk enhance system prompt

---

### 6. ✅ Gaya Komunikasi Santai
**File**: `data/system_prompt.txt`

**Implementasi**:
- Bahasa Indonesia informal (kamu, bukan Anda)
- Analogi kehidupan sehari-hari
- Emoji secukupnya untuk friendly
- Pertanyaan terbuka untuk engage
- Supportive tone

**Karakteristik**:
```
✅ DO:
- "Coba kamu pikirkan dulu..."
- "Kira-kira kenapa ya..."
- "Apa yang terjadi kalau..."
- "Udah coba cara ini belum?"

❌ DON'T:
- "Jawabannya adalah..."
- "Ini karena..."
- "Yang terjadi adalah..."
- "Kamu harus..."
```

**Example Response Style**:
```
"Binary search itu mirip kayak kamu nyari kata di kamus. 
Gak mungkin kan buka dari halaman 1? Pasti langsung buka tengah, 
terus kalau kata yang dicari 'sebelum' tengah, fokus ke kiri. 

Nah, konsep 'bagi dua' ini yang bikin binary search super cepet! 
Coba bayangin, kalau ada 1000 data, paling cuma butuh 10 langkah. 
Keren kan? 🎯

Udah paham konsepnya? Mau coba trace dengan contoh sederhana?"
```

**Responsif terhadap Konteks**:
- Frustasi → lebih supportif, hint lebih jelas
- Paham dasar → challenge dengan pertanyaan lebih dalam
- Stuck lama → pecah jadi langkah lebih kecil
- Hampir benar → positive reinforcement + hint kecil

---

## 📁 Files Created/Modified

### New Files Created:
1. `utils/question_detector.py` (278 lines)
   - QuestionType enum
   - QuestionDetector class
   - Response strategy generation

2. `utils/code_analyzer.py` (424 lines)
   - CodeAnalyzer class
   - AST parsing logic
   - Algorithm detection
   - Guided questions generator

3. `utils/algorithm_simulator.py` (570 lines)
   - AlgorithmSimulator class
   - 7 algorithm simulators
   - Step-by-step trace
   - Visualization helpers

4. `docs/LOGIKA_CHATBOT.md` (450+ lines)
   - Complete technical documentation
   - Usage examples
   - Integration guide

### Modified Files:
1. `pages/1_Chat.py`
   - Import new utilities
   - Initialize detectors & analyzers
   - File upload with auto-analysis
   - Enhanced prompt building
   - Homework rejection logic
   - Question type in response metadata

2. `data/system_prompt.txt`
   - Complete rewrite dengan Socratic method
   - Detailed guidance per scenario
   - Communication style guide
   - Examples of good vs bad responses

3. `todo.md`
   - Mark all 6 tasks as completed ✅

---

## 🔄 Integration Flow

```
User Input
    ↓
[Question Detector]
    ├─ Type: CONCEPT/CODE/DEBUGGING/HOMEWORK/SIMULATION/GENERAL
    ├─ Confidence score
    └─ Response strategy
    ↓
[Homework Check]
    ├─ If homework → REJECT with guidance
    └─ If not → Continue
    ↓
[Code Analysis] (if file uploaded)
    ├─ Parse AST
    ├─ Detect algorithms
    ├─ Calculate complexity
    └─ Generate guided questions
    ↓
[Enhanced System Prompt]
    ├─ Base system prompt
    ├─ + Response strategy guidance
    ├─ + Code analysis (if available)
    └─ + Guided questions
    ↓
[LLM Generation]
    ↓
[Response Display]
    ├─ Typing effect
    ├─ Model info
    └─ Question type metadata
```

---

## 🧪 Testing

All utilities have built-in test cases:

```bash
# Test question detector
python utils/question_detector.py

# Test code analyzer
python utils/code_analyzer.py

# Test algorithm simulator
python utils/algorithm_simulator.py
```

**Test Coverage**:
- ✅ Question detection for all 6 types
- ✅ Code analysis for valid/invalid syntax
- ✅ Algorithm detection (10+ algorithms)
- ✅ Simulation for 7 algorithms
- ✅ Homework rejection keywords
- ✅ Guided questions generation

---

## 📊 Key Features Summary

| Feature | Status | Implementation |
|---------|--------|----------------|
| Question Type Detection | ✅ | Regex patterns, confidence scoring |
| Guided Learning | ✅ | Socratic method in system prompt |
| Algorithm Simulation | ✅ | Step-by-step trace for 7 algorithms |
| Homework Rejection | ✅ | Keyword detection + polite message |
| Code Parsing | ✅ | AST analysis, algorithm detection |
| Friendly Communication | ✅ | Informal bahasa, analogies, emoji |
| Code Analysis Auto | ✅ | On file upload, session state |
| Enhanced Prompts | ✅ | Strategy + analysis + questions |
| Error Handling | ✅ | Syntax errors, invalid code |
| Documentation | ✅ | Complete technical docs |

---

## 🎯 Impact on Learning Experience

### Before:
- Generic responses tanpa mempertimbangkan context
- Bisa memberikan kode lengkap untuk tugas
- Tidak ada analisis kode yang diupload
- Komunikasi terlalu formal

### After:
- ✅ **Smart detection** - respons sesuai jenis pertanyaan
- ✅ **Homework protection** - tolak tugas dengan sopan, arahkan ke konsep
- ✅ **Code insights** - analisis otomatis dengan learning points
- ✅ **Guided learning** - Socratic method, bukan spoon-feeding
- ✅ **Step-by-step simulation** - visualisasi algoritma
- ✅ **Friendly tone** - komunikasi santai seperti teman

### Example Interaction:

**User**: "Tolong buatkan kode bubble sort untuk tugas saya"

**Before**: *[Memberikan kode lengkap]*

**After**: 
```
🚫 Maaf, saya tidak bisa membantu mengerjakan tugas secara langsung.

Tapi yuk kita belajar konsepnya! Bubble sort itu kayak ngurutin 
kartu yang kamu pegang...

[Penjelasan konsep dengan analogi]

Coba tanyakan:
- "Jelaskan cara kerja bubble sort"
- "Simulasikan bubble sort untuk array [5,2,8,1]"
```

---

## 🚀 Next Steps

Logika Chatbot sudah complete! Untuk testing:

1. **Run the app**:
   ```bash
   streamlit run app.py
   ```

2. **Test scenarios**:
   - Ask conceptual question
   - Request code implementation
   - Upload Python file
   - Ask for homework help (should reject)
   - Request algorithm simulation

3. **Verify**:
   - Question type detection working
   - Code analysis appears in sidebar
   - Homework requests rejected politely
   - Responses follow guided learning approach

---

## 📝 Notes

- All code tested with sample inputs
- Documentation comprehensive dengan examples
- Integration seamless dengan existing LLM system
- No breaking changes to previous features
- Performance optimized dengan caching

**Total Lines of Code**: ~1,700 lines (new utilities + modifications)

**Time to Implement**: Full implementation completed in single session

**Code Quality**: 
- ✅ Type hints
- ✅ Docstrings
- ✅ Error handling
- ✅ Example usage in __main__
- ✅ Modular design

---

## ✨ Conclusion

Semua task "Logika Chatbot" berhasil diimplementasikan dengan:
- **Question Detection** yang akurat
- **Guided Learning** via Socratic method
- **Algorithm Simulation** yang detail
- **Homework Rejection** yang sopan
- **Code Analysis** yang comprehensive
- **Friendly Communication** yang natural

Chatbot sekarang siap memberikan pengalaman pembelajaran yang **engaging**, **effective**, dan **ethical**! 🎓✨
