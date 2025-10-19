# Quick Reference Card

## 🚀 Getting Started

### Live Demo
**URL:** https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/

### Local Setup
```bash
git clone https://github.com/arifsetwn/chatbot.v2.git
cd chatbot.v2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 💬 Chat Commands

### Basic Usage
```
Jelaskan binary search
Apa perbedaan bubble sort dan selection sort?
Bagaimana cara implementasi recursive fibonacci?
```

### Code Review
```
# Upload file Python, lalu tanya:
Apakah kode saya efisien?
Apa kompleksitas kode ini?
Bagaimana cara optimize kode ini?
```

---

## 🔬 Algorithm Simulator

### Available Algorithms

| Algorithm | Input Example | Use Case |
|-----------|---------------|----------|
| **Bubble Sort** | `64, 34, 25, 12, 22` | Learn sorting basics |
| **Selection Sort** | `29, 10, 14, 37, 13` | Compare sorting algorithms |
| **Insertion Sort** | `12, 11, 13, 5, 6` | Small dataset sorting |
| **Binary Search** | Array: `1,3,5,7,9` Target: `5` | Search in sorted data |
| **Linear Search** | Array: `64,34,25` Target: `25` | Search in unsorted data |
| **Factorial** | `5` | Learn recursion |
| **Fibonacci** | `7` | Understand recursive patterns |

### How to Use
1. Select algorithm from sidebar dropdown
2. Enter input data (comma-separated for arrays)
3. Click "Jalankan Simulasi"
4. View step-by-step execution

---

## 📤 File Upload

### Supported Formats
- `.py` - Python source code
- `.txt` - Text files with code

### File Size Limit
- Maximum: 1 MB

### What Gets Analyzed
✅ Syntax validation
✅ Algorithm detection
✅ Complexity analysis (O(n), O(log n), etc.)
✅ Code structure (functions, classes, loops)
✅ Security check (imports, file operations)

---

## 🔐 Admin Access

### Default Login
- **Username:** `admin`
- **Password:** `admin123`

⚠️ Change default password immediately!

### Admin Features
- ⚙️ API Key Management
- 🤖 Model Selection
- 📊 Analytics Dashboard
- 📝 System Prompt Editor
- 🔧 Rate Limit Configuration

---

## ⚡ Rate Limits

### Default Limits
- **Global:** 60 requests/minute
- **Per User (Minute):** 10 requests
- **Per User (Hour):** 100 requests

### When Limit Reached
```
⏳ Rate limit tercapai!
Tunggu 30 detik sebelum mencoba lagi.
```

---

## 🎓 Learning Topics

### Available Categories

#### 1. Dasar-dasar Algoritma
- Apa itu algoritma?
- Cara membaca pseudocode
- Big O notation
- Best/Worst/Average case

#### 2. Sorting & Searching
- Bubble Sort, Selection Sort, Insertion Sort
- Binary Search, Linear Search
- Perbandingan algoritma

#### 3. Struktur Data Dasar
- Array & List
- Stack & Queue
- Linked List
- Hash Table

#### 4. Rekursi & DP
- Konsep rekursi
- Base case & recursive case
- Dynamic Programming intro
- Memoization

#### 5. Graph Algorithms
- Graph representation
- DFS & BFS
- Shortest path
- Tree traversal

---

## 🐛 Troubleshooting

### Common Issues

**Q: Chat tidak merespon?**
```
A: Check API key di .env atau Streamlit Secrets
   Verify GEMINI_API_KEY sudah benar
```

**Q: File upload gagal?**
```
A: Check file size < 1MB
   Verify format .py atau .txt
   Check file permissions
```

**Q: Algorithm simulator error?**
```
A: Verify input format correct
   For arrays: comma-separated numbers
   For factorial/fibonacci: single number 0-20
```

**Q: Rate limit tercapai?**
```
A: Tunggu beberapa detik
   Adjust limit di Admin panel
   Check RATE_LIMIT_* di .env
```

---

## 📱 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl/Cmd + K` | Clear chat history |
| `Esc` | Close sidebar |

---

## 🔗 Quick Links

- **Demo:** https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/
- **GitHub:** https://github.com/arifsetwn/chatbot.v2
- **Docs:** [README.md](README.md)
- **Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Setup:** [docs/API_KEY_SETUP.md](docs/API_KEY_SETUP.md)

---

## 💡 Tips & Best Practices

### For Students
1. ✅ Start with simple questions
2. ✅ Try algorithm simulator before asking
3. ✅ Upload code for specific reviews
4. ✅ Ask "why" and "how", not just "what"
5. ✅ Read step-by-step explanations carefully

### For Instructors
1. ✅ Change default admin password
2. ✅ Customize system prompt for your course
3. ✅ Monitor analytics regularly
4. ✅ Set appropriate rate limits
5. ✅ Keep API keys secure

---

**Print this card for quick reference!**

Last Updated: 19 Oktober 2025
