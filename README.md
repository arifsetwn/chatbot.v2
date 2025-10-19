# 🤖 Chatbot Pembelajaran Algoritma

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Chatbot interaktif berbasis web untuk membantu mahasiswa pemula memahami konsep algoritma dan cara berpikir komputasional. Dibangun dengan Streamlit dan terintegrasi dengan Google Gemini AI.

## 🌐 Demo

**Live Demo:** [https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/](https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/)

> **Note:** Demo menggunakan Google Gemini API. Klik langsung untuk mencoba!

## ✨ Fitur Lengkap

### 💬 Chat Interface
- **Percakapan Interaktif**: Chat real-time dengan AI chatbot
- **Guided Learning**: Panduan step-by-step, bukan jawaban langsung
- **Deteksi Jenis Pertanyaan**: Otomatis mendeteksi apakah pertanyaan tentang konsep, kode, atau debugging
- **Smart Response**: Response yang disesuaikan dengan jenis pertanyaan
- **Conversation Context**: Chatbot mengingat 5 pesan terakhir untuk konteks

### 🔬 Algorithm Simulator
- **7 Algoritma Terintegrasi:**
  - **Sorting:** Bubble Sort, Selection Sort, Insertion Sort
  - **Searching:** Binary Search, Linear Search
  - **Recursive:** Factorial, Fibonacci
- **Step-by-Step Execution**: Lihat setiap langkah algoritma secara detail
- **Visual Trace**: Visualisasi perubahan array per step
- **Complexity Analysis**: Time & space complexity untuk setiap algoritma
- **Interactive Widget**: Jalankan simulasi langsung dari sidebar

### 📤 Code Analysis
- **Upload File Python**: Support .py dan .txt (max 1MB)
- **Syntax Validation**: Deteksi error syntax otomatis
- **Algorithm Detection**: Identifikasi algoritma yang digunakan
- **Complexity Detection**: Deteksi time complexity (O(n), O(log n), dll)
- **Code Structure Analysis**: Functions, classes, loops, conditions
- **Security Check**: Validasi kode berbahaya (imports, file ops, dll)

### 📚 Learning Topics
- **Kategori Terstruktur:**
  - Dasar-dasar Algoritma
  - Sorting & Searching
  - Struktur Data Dasar
  - Rekursi & Dynamic Programming
  - Graph Algorithms
- **Quick Topic Selection**: Pilih topik dari sidebar untuk fokus pembelajaran

### 🔐 Admin Panel
- **Authentication**: Login aman dengan streamlit-authenticator v0.4.2
- **API Key Management**: Kelola Gemini dan OpenAI API keys
- **Model Selection**: Pilih model aktif dan fallback
- **Rate Limit Configuration**: Atur limit per menit/jam
- **System Prompt Editor**: Customize behavior chatbot
- **Analytics Dashboard**: 
  - Total chat messages
  - Average response time
  - Active users
  - Daily usage charts

### ⚡ Rate Limiting
- **Multi-Level Protection:**
  - Global: 60 requests/minute
  - Per-user per-minute: 10 requests
  - Per-user per-hour: 100 requests
- **Token Bucket Algorithm**: Smooth rate limiting
- **User-Friendly Messages**: Clear feedback saat limit tercapai

### 🎓 Educational Features
- **Socratic Method**: Chatbot bertanya balik untuk merangsang berpikir
- **No Direct Answers**: Tidak memberikan jawaban langsung untuk tugas/ujian
- **Ethical Guidelines**: Disclaimer etika pembelajaran di header
- **Progressive Learning**: Dari konsep dasar ke advanced

## 🚀 Quick Start

### Persyaratan Sistem

- Python 3.10 atau lebih baru
- pip (package manager Python)
- Git

### Setup Virtual Environment (Direkomendasikan)

Untuk menghindari konflik dependencies dengan proyek Python lainnya, gunakan virtual environment:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk macOS/Linux:
source venv/bin/activate
# Untuk Windows:
# venv\Scripts\activate

# Verifikasi virtual environment aktif
### Persyaratan Sistem

- Python 3.10 atau lebih baru
- pip (package manager Python)
- Git
- API Key Google Gemini (gratis dari [Google AI Studio](https://aistudio.google.com/app/apikey))

### Instalasi Lokal

1. **Clone repository**
   ```bash
   git clone https://github.com/arifsetwn/chatbot.v2.git
   cd chatbot.v2
   ```

2. **Setup virtual environment** (direkomendasikan)
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # atau
   # venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi environment**
   ```bash
   # Copy .env example (jika ada)
   cp .env.example .env
   
   # Atau buat file .env baru
   nano .env
   ```
   
   Minimal configuration:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=change_this_password
   ACTIVE_MODEL=gemini
   GEMINI_MODEL=gemini-2.0-flash
   ```

5. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

Aplikasi akan berjalan di `http://localhost:8501`

### Mendapatkan API Key

#### Google Gemini (Gratis)
1. Kunjungi [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in dengan Google account
3. Click "Create API Key" atau "Get API Key"
4. Copy API key dan paste ke `.env` file

#### OpenAI (Opsional)
1. Kunjungi [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account dan add billing
3. Generate new API key
4. Copy dan paste ke `.env` file

> **Note:** Untuk demo/development, cukup gunakan Gemini API (gratis).

## ⚙️ Konfigurasi

### Environment Variables

File `.env` konfigurasi lengkap:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here  # Alias untuk GEMINI_API_KEY

# Optional: OpenAI (untuk fallback)
# OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
APP_NAME=Chatbot Pembelajaran Algoritma
APP_VERSION=1.0.0

# Security Settings
SECRET_KEY=your_random_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_this_secure_password

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
GLOBAL_RATE_LIMIT=60

# Model Settings
ACTIVE_MODEL=gemini
DEFAULT_MODEL=gemini
GEMINI_MODEL=gemini-2.0-flash

# Optional: Fallback model
# FALLBACK_MODEL=openai
# OPENAI_MODEL=gpt-3.5-turbo

# File Upload Settings
MAX_FILE_SIZE_MB=1
ALLOWED_FILE_TYPES=py,txt

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/chatbot.log

# Server Settings
HOST=0.0.0.0
PORT=8501
```

### Admin Access

**Default credentials:**
- Username: `admin`
- Password: `admin123`

> ⚠️ **PENTING:** Segera ubah password default di file `.env` sebelum deployment!

## 📖 Cara Penggunaan

### 💬 Untuk Mahasiswa

1. **Buka halaman Chat**
   - Klik menu "Chat" di sidebar
   
2. **Pilih topik pembelajaran** (opsional)
   - Expand kategori di sidebar
   - Klik topik yang ingin dipelajari
   
3. **Mulai bertanya**
   - Ketik pertanyaan di chat input
   - Contoh: "Jelaskan cara kerja binary search"
   
4. **Upload kode untuk review** (opsional)
   - Klik "Upload Kode" di sidebar
   - Pilih file .py atau .txt (max 1MB)
   - Tanyakan tentang kode yang diupload
   
5. **Coba Algorithm Simulator**
   - Pilih algoritma di sidebar
   - Masukkan input data
   - Klik "Jalankan Simulasi"
   - Lihat step-by-step execution

### 🔧 Untuk Dosen/Admin

1. **Akses Admin Panel**
   - Klik menu "Admin" di sidebar
   - Login dengan credentials
   
2. **Kelola API Keys**
   - View/edit Gemini & OpenAI API keys
   - Test koneksi API
   
3. **Pilih Model**
   - Pilih model aktif (Gemini/OpenAI)
   - Set fallback model
   
4. **Atur Rate Limiting**
   - Set limit per menit/jam
   - Monitor usage
   
5. **Edit System Prompt**
   - Customize chatbot behavior
   - Set learning guidelines
   
6. **Monitor Analytics**
   - Lihat total messages
   - Average response time
   - Daily usage charts

## 🏗️ Struktur Proyek

```
chatbot.v2/
├── app.py                          # Entry point (redirects to Chat)
├── pages/
│   ├── 1_Chat.py                  # Chat interface with LLM
│   └── 2_Admin.py                 # Admin panel
├── utils/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── gemini_client.py       # Google Gemini wrapper
│   │   ├── openai_client.py       # OpenAI wrapper
│   │   └── llm_manager.py         # Unified LLM manager
│   ├── algorithm_simulator.py     # Algorithm step-by-step simulator
│   ├── question_detector.py       # Question type detection
│   ├── code_analyzer.py           # Python code analysis
│   └── rate_limiter.py            # Rate limiting (token bucket)
├── data/
│   └── system_prompt.txt          # Chatbot system prompt
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml.example       # Secrets template
├── docs/
│   ├── API_KEY_SETUP.md           # API key setup guide
│   ├── LLM_INTEGRATION.md         # LLM integration docs
│   ├── ALGORITHM_SIMULATOR_USAGE.md  # Simulator guide
│   ├── DEPLOYMENT_GUIDE.md        # Streamlit Cloud deployment
│   └── PRE_DEPLOYMENT_CHECKLIST.md   # Deployment checklist
├── requirements.txt               # Python dependencies
├── requirements-minimal.txt       # Minimal deps (for deployment)
├── packages.txt                   # System packages (for Streamlit Cloud)
├── .env                          # Environment variables (gitignored)
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🛠️ Tech Stack

### Frontend
- **Streamlit** v1.28+ - Web framework
- **Streamlit-authenticator** v0.4.2 - Authentication

### AI/LLM Integration
- **Google Gemini API** v0.3+ - Primary LLM (gemini-2.0-flash)
- **OpenAI API** v1.0+ - Fallback LLM (optional)

### Data Processing
- **Pandas** v2.0+ - Data manipulation
- **NumPy** v1.24+ - Numerical operations

### Security & Utilities
- **Cryptography** v41.0+ - Encryption
- **python-dotenv** v1.0+ - Environment management
- **PyYAML** v6.0+ - Configuration

### Code Analysis
- **AST (built-in)** - Python code parsing
- **Regular expressions** - Pattern matching

## 📚 Dokumentasi

Dokumentasi lengkap tersedia di folder `docs/`:

- **[API_KEY_SETUP.md](docs/API_KEY_SETUP.md)** - Panduan mendapatkan API keys
- **[LLM_INTEGRATION.md](docs/LLM_INTEGRATION.md)** - Technical docs LLM integration
- **[ALGORITHM_SIMULATOR_USAGE.md](ALGORITHM_SIMULATOR_USAGE.md)** - Cara menggunakan simulator
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy ke Streamlit Cloud
- **[PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)** - Checklist sebelum deploy
- **[FIX_DEPLOYMENT_ERROR.md](FIX_DEPLOYMENT_ERROR.md)** - Troubleshooting deployment

## 🔧 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/arifsetwn/chatbot.v2.git
cd chatbot.v2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run in development mode
streamlit run app.py
```

### Testing Locally

```bash
# Test algorithm simulator
python3 demo_algorithm_simulator.py

# Test LLM integration
python3 -c "from utils.llm.gemini_client import GeminiClient; print('OK')"

# Test imports
python3 -c "from utils.algorithm_simulator import AlgorithmSimulator; print('OK')"
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest tests/

# Code formatting
black .

# Linting
flake8 .
```

## 🚀 Deployment

### Deploy ke Streamlit Cloud

1. **Push ke GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy di Streamlit Cloud:**
   - Login ke [Streamlit Cloud](https://streamlit.io/cloud)
   - New app → Pilih repository
   - Main file: `app.py`
   - Add secrets di Advanced settings

3. **Verifikasi deployment:**
   - Check app URL
   - Test functionality
   - Monitor logs

**📖 Panduan lengkap:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Environment Variables di Streamlit Cloud

Tambahkan di Streamlit Cloud Settings → Secrets:

```toml
GEMINI_API_KEY = "your_api_key_here"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secure_password"
ACTIVE_MODEL = "gemini"
GEMINI_MODEL = "gemini-2.0-flash"
RATE_LIMIT_PER_MINUTE = "10"
RATE_LIMIT_PER_HOUR = "100"
```

## 🤝 Contributing

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings untuk functions/classes
- Update dokumentasi jika ada perubahan API
- Test perubahan sebelum commit
- Write clear commit messages

## 📝 Changelog

### v1.0.0 (Oktober 2025)
- ✅ Initial release
- ✅ Chat interface dengan Gemini AI
- ✅ Algorithm simulator (7 algoritma)
- ✅ Code analyzer & syntax checker
- ✅ Admin panel dengan authentication
- ✅ Rate limiting system
- ✅ Question type detection
- ✅ Deployment ke Streamlit Cloud

## 🐛 Known Issues

- Fibonacci simulator slow untuk n>15 (exponential recursion)
- Large array (>100 elements) generate banyak steps di simulator
- OpenAI fallback requires billing setup

## 🔮 Roadmap

### Phase 2 (Q1 2026)
- [ ] Add more algorithms (Quick Sort, Merge Sort, DFS/BFS)
- [ ] Graphical visualization (charts, flowcharts)
- [ ] User progress tracking
- [ ] Quiz & assessment feature
- [ ] Export simulation to PDF

### Phase 3 (Q2 2026)
- [ ] Multi-language support (EN/ID)
- [ ] LMS integration (Moodle API)
- [ ] Collaborative learning features
- [ ] Mobile app version
- [ ] Voice interaction

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Authors

- **Arif Setiawan** - Initial work - [@arifsetwn](https://github.com/arifsetwn)

## 🙏 Acknowledgments

- Streamlit team untuk amazing framework
- Google untuk Gemini API
- OpenAI untuk GPT models
- Open source community

## 📞 Support

- **Email:** [your-email@example.com]
- **GitHub Issues:** [Create an issue](https://github.com/arifsetwn/chatbot.v2/issues)
- **Demo:** [https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/](https://chatbotv2-jeu2cve8kghtl949f593rl.streamlit.app/)

## 🌟 Star History

Jika project ini membantu, berikan ⭐ di GitHub!

---

**Made with ❤️ for students learning algorithms**

**Last Updated:** 19 Oktober 2025
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API Key | - |
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `DEFAULT_MODEL` | Model AI default | gemini |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | Batas request per menit | 10 |
| `MAX_FILE_SIZE_MB` | Ukuran maksimal file upload | 1 |

## 📊 Monitoring

Aplikasi menyediakan:
- Log aktivitas chat
- Statistik penggunaan
- Response time monitoring
- Error tracking

## 🔒 Keamanan

- Tidak menyimpan data personal mahasiswa
- API keys dienkripsi
- Rate limiting untuk mencegah abuse
- Input validation untuk file upload
- Local storage untuk riwayat percakapan

## 🤝 Contributing

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

Untuk pertanyaan atau dukungan:
- Buat issue di repository
- Hubungi tim pengembang PTI UMS

---

**Dikembangkan oleh:** Tim Pengembang Chatbot PTI UMS
**Tanggal:** Oktober 2025
**Versi:** 1.0.0