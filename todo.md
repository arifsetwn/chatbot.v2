# Todo List - Chatbot Pembelajaran Algoritma

## Setup Proyek
- [x] Inisialisasi proyek Streamlit dengan struktur multi-page (/chat dan /admin)
- [x] Setup environment dan dependencies (requirements.txt)
- [x] Konfigurasi .env untuk API keys dan settings rahasia
- [x] Setup Git repository dan struktur folder

## Frontend - Halaman Chatbot (/chat)
- [x] Desain UI chat interface dengan chat bubbles dan input area
- [x] Implementasi sidebar dengan daftar topik algoritma
- [x] Fitur upload file kode Python (.py/.txt) dengan validasi
- [x] Integrasi localStorage untuk menyimpan riwayat percakapan
- [x] Responsif design untuk desktop dan mobile
- [x] Implementasi disclaimer etika di header

## Backend - Halaman Admin (/admin)
- [x] Sistem autentikasi sederhana (username/password) - FIXED: Multi-version fallback
- [x] API Key Management untuk Gemini dan OpenAI
- [x] Model Selection (pemilihan model aktif)
- [x] Rate Limit Configuration
- [x] Upload PDF Material dengan storage
- [x] System Prompt Setting dengan editor teks
- [x] Analytics Dashboard (log chat, waktu respon, jumlah chat harian)

## Integrasi LLM
- [x] Wrapper API untuk Gemini API
- [x] Wrapper API untuk OpenAI API
- [x] Modular API abstraction layer untuk mudah menambah model
- [x] Error handling dan fallback messages
- [x] Rate limiting implementation

## Logika Chatbot
- [x] Deteksi jenis pertanyaan (konsep/kode/debugging)
- [x] Guided learning approach - step-by-step reasoning
- [x] Simulasi langkah algoritma secara tekstual/tabel
- [x] Penolakan jawaban langsung untuk tugas/ujian
- [x] Parsing dan analisis kode Python yang diupload
- [x] Gaya komunikasi santai dan membimbing

## Keamanan dan Privacy
- [ ] Validasi input untuk mencegah script injection
- [ ] Enkripsi data API di server
- [ ] Rate limiter untuk mencegah abuse
- [ ] File upload security (maks 1MB, format terbatas)
- [ ] Tidak menyimpan data personal mahasiswa

## Logging dan Monitoring
- [ ] Sistem logging untuk admin (prompt, response, timestamp, model)
- [ ] Storage log menggunakan SQLite/JSON
- [ ] Dashboard analitik dengan metrics dasar
- [ ] Monitoring uptime dan performance

## Testing dan Evaluasi
- [ ] Unit testing untuk komponen utama
- [ ] Integration testing untuk API calls
- [ ] User acceptance testing dengan mahasiswa
- [ ] Performance testing (response time <2 detik)
- [ ] AB testing preparation

## Deployment
- [ ] Setup deployment di server kampus
- [ ] Konfigurasi untuk intranet/VPN access
- [ ] Environment setup (Python 3.10+, dependencies)
- [ ] Backup dan recovery procedures

## Dokumentasi
- [ ] README.md dengan setup instructions
- [ ] Dokumentasi API dan konfigurasi
- [ ] User guide untuk mahasiswa dan admin
- [ ] Developer documentation

## Future Enhancements (Fase 2)
- [ ] Integrasi dengan LMS (Moodle API)
- [ ] Visualisasi algoritma interaktif (flowchart/trace table)
- [ ] Penilaian otomatis kode mahasiswa
- [ ] Leaderboard dan gamifikasi
- [ ] Ekspansi materi algoritma