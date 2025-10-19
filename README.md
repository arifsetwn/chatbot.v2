# 🤖 Chatbot Pembelajaran Algoritma

Chatbot interaktif berbasis web untuk membantu mahasiswa pemula memahami konsep algoritma dan cara berpikir komputasional. Dibangun dengan Streamlit dan terintegrasi dengan model AI (Google Gemini & OpenAI).

## ✨ Fitur Utama

- **💬 Chat Interface**: Percakapan interaktif dengan chatbot
- **📚 Guided Learning**: Panduan langkah demi langkah, bukan jawaban langsung
- **📤 Upload Kode**: Unggah file Python untuk didiskusikan
- **🔐 Admin Panel**: Manajemen API, model, dan monitoring
- **📊 Analytics**: Dashboard aktivitas dan performa
- **🔒 Local Storage**: Riwayat percakapan tersimpan di browser
- **⚡ Rate Limiting**: Kontrol penggunaan API

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
which python  # Harus menunjukkan path ke venv
```

### Instalasi

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd chatbot.v2
   ```

2. **Setup virtual environment** (jika belum)
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
   cp .env.example .env
   # Edit file .env dengan API keys yang valid
   ```

5. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

Aplikasi akan berjalan di `http://localhost:8501`

### Menonaktifkan Virtual Environment

```bash
deactivate
```

## ⚙️ Konfigurasi

### API Keys

Edit file `.env` dan isi dengan API keys yang valid:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Admin Access

Default credentials untuk admin:
- Username: `admin`
- Password: `admin123`

### Rate Limiting

Konfigurasi di file `.env`:
```env
RATE_LIMIT_REQUESTS_PER_MINUTE=10
RATE_LIMIT_REQUESTS_PER_HOUR=100
```

## 📖 Cara Penggunaan

### Untuk Mahasiswa

1. Buka halaman **Chat**
2. Pilih topik algoritma di sidebar
3. Tanyakan pertanyaan atau upload kode Python
4. Diskusikan langkah demi langkah dengan chatbot

### Untuk Dosen/Admin

1. Buka halaman **Admin**
2. Login dengan credentials admin
3. Kelola API keys dan model AI
4. Monitor aktivitas pengguna
5. Upload materi pembelajaran

## 🏗️ Struktur Proyek

```
chatbot.v2/
├── app.py                 # Main application
├── pages/
│   ├── 1_💬_Chat.py      # Chat interface
│   └── 2_⚙️_Admin.py     # Admin panel
├── config/                # Configuration files
├── data/                  # Application data
├── logs/                  # Log files
├── uploads/               # Uploaded files
├── utils/                 # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Development

### Menjalankan dalam mode development

```bash
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