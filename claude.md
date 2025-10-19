# Claude Notes
## Chatbot Pembelajaran Algoritma – Internal Design Rationale

---

### 1. Konteks Pengembangan
Chatbot ini dikembangkan sebagai media pendukung pembelajaran bagi mahasiswa pemula pada mata kuliah **Algoritma dan Pemrograman**.  
Masalah utama yang ingin diatasi:
- Mahasiswa kesulitan memahami logika langkah demi langkah dalam menyusun algoritma.
- Banyak yang cenderung mencari jawaban instan, bukan proses berpikir.
- Dosen membutuhkan alat bantu yang bisa mendampingi mahasiswa secara mandiri di luar jam kuliah.

Chatbot akan berperan seperti **asisten belajar interaktif** yang menuntun cara berpikir, bukan memberi solusi langsung.

---

### 2. Prinsip Desain Utama

1. **Guided Learning over Solution Giving**  
   - Chatbot tidak memberikan kode siap pakai.  
   - Fokus pada *step-by-step reasoning* sesuai pendekatan *computational thinking*: dekomposisi, pengenalan pola, abstraksi, dan algoritma.  
   - Jawaban model diarahkan agar memancing mahasiswa berpikir, bukan menyalin.

2. **Simplicity for First-Year Students**  
   - Mahasiswa sasaran adalah pemula, sehingga antarmuka dan percakapan harus ringan dan tidak teknis berlebihan.  
   - Tidak perlu login agar mudah diakses.  

3. **Local Privacy by Design**  
   - Tidak menyimpan data mahasiswa di server (no user tracking).  
   - Riwayat percakapan hanya disimpan secara lokal (localStorage browser).  

4. **Low Dependency Infrastructure**  
   - Sistem dibangun dengan **Streamlit** karena mudah dikembangkan dan dideploy di server internal kampus tanpa framework berat.  
   - Backend dan frontend dijalankan dalam satu aplikasi Streamlit yang memiliki dua halaman:  
     - `/chat` → halaman mahasiswa  
     - `/admin` → halaman dosen/admin  

5. **Modular API Integration**  
   - Model LLM dapat diganti dari admin panel (Gemini atau OpenAI).  
   - Struktur kode backend memisahkan *API abstraction layer* sehingga mudah menambah model lain di masa depan.  

---

### 3. Asumsi Teknis

| Aspek | Asumsi |
|-------|---------|
| Framework | Streamlit (Python ≥ 3.10) |
| Model LLM | Gemini API dan OpenAI API |
| Deployment | Server kampus dengan akses terbatas (intranet atau VPN) |
| Storage | LocalStorage (client), SQLite (server logs) |
| User Data | Tidak ada data personal yang disimpan |
| File Upload | Maksimum 1 MB, format `.py` dan `.txt` |
| Logging | Hanya untuk admin: prompt, response, waktu, model |
| Auth | Username-password hanya untuk halaman admin |
| Fallback | Pesan: “Sistem sedang maintenance.” |
| Source Control | GitHub (private repo internal kampus) |

---

### 4. Alasan Tidak Menggunakan Login Mahasiswa
- Tujuan sistem bukan menilai kinerja individu, tapi memberikan akses terbuka untuk belajar.  
- Autentikasi hanya akan menambah kompleksitas deployment dan penyimpanan data pribadi.  
- Dengan localStorage, riwayat percakapan tetap tersedia selama sesi browser belum dihapus.  

---

### 5. Logika Percakapan Chatbot

**Struktur percakapan (pseudo flow):**
1. User bertanya → sistem deteksi jenis pertanyaan (konsep / kode / debugging).  
2. Jika pertanyaan berupa kode:
   - Chatbot membaca kode, menjelaskan logika tiap langkah tanpa menulis ulang kode.
3. Jika pertanyaan berupa konsep:
   - Chatbot menjelaskan konsep dengan contoh analogi sederhana.
4. Jika pertanyaan mengarah ke tugas atau ujian:
   - Bot merespons dengan petunjuk, bukan jawaban akhir.  
   Contoh:  
   > “Mari kita pikirkan langkah-langkahnya. Apa input dan output yang kamu harapkan?”  

**Nada komunikasi:**  
Santai, bersahabat, dan membantu mahasiswa memahami alur berpikir.

---

### 6. Pertimbangan Pemilihan Streamlit

Dipilih karena:
- Mudah dikembangkan cepat untuk keperluan MVP (1 minggu).  
- Tidak memerlukan frontend terpisah (HTML/CSS/JS minimal).  
- Mendukung multi-page structure (untuk admin dan user).  
- Integrasi Python-native untuk koneksi API dan visualisasi algoritma.  

Keterbatasan yang disadari:
- Bukan framework multi-user penuh (concurrency terbatas).  
- Tidak ideal untuk sistem berskala besar atau dengan autentikasi kompleks.  
Namun sesuai untuk pilot project berbasis kampus.

---

### 7. Visualisasi dan Simulasi Langkah Algoritma

Untuk simulasi, sistem akan:
- Mengonversi langkah algoritma menjadi teks naratif atau tabel (bukan grafik animasi).  
- Contoh output:
Step 1: Mulai dengan array [4, 2, 1]
Step 2: Bandingkan elemen pertama dan kedua → tukar
Step 3: Hasil sementara [2, 4, 1]
Step 4: Ulangi langkah hingga terurut
- Tujuannya agar mahasiswa memahami *logical trace* sebelum berpindah ke bentuk visual atau kode nyata.

---

### 8. Keamanan dan Etika

- Chatbot harus menolak konten berbahaya, tidak pantas, atau tidak relevan dengan topik akademik.  
- Semua data API (Gemini/OpenAI) disimpan terenkripsi di sisi server.  
- Tidak diperbolehkan mengirim kode atau data sensitif ke API publik.  
- Disclaimer ditampilkan di halaman depan chatbot:  
> “Chatbot ini berfungsi sebagai pendamping belajar, bukan pengganti dosen.”

---

### 9. Monitoring & Evaluasi Awal

**Rencana pengujian:**
- AB testing selama satu minggu pada dua kelompok mahasiswa.  
- Tujuan: melihat dampak chatbot terhadap pemahaman konsep algoritma.  
- Data yang dikumpulkan:
- Jumlah percakapan
- Jenis pertanyaan
- Waktu respon rata-rata
- Feedback kualitatif dari mahasiswa

**Evaluasi keberhasilan:**  
Chatbot dianggap efektif jika ≥80% percakapan relevan dan mahasiswa menyatakan terbantu dalam memahami konsep.

---

### 10. Rencana Pengembangan Lanjutan

**Fase 2 (setelah MVP):**
- Integrasi dengan LMS (contoh: Moodle API).  
- Fitur autentikasi mahasiswa (opsional).  
- Evaluasi otomatis berdasarkan input kode.  
- Visualisasi algoritma interaktif (Flowchart / Trace Table).  
- Leaderboard pembelajaran (gamifikasi).  
- Ekspor log percakapan untuk analisis dosen.

---

### 11. Catatan Developer

- Pastikan API key tidak dikodekan secara langsung di repository publik.  
- Gunakan file `.env` untuk menyimpan konfigurasi rahasia.  
- Semua file yang diunggah user harus dibersihkan dari script injection (gunakan `ast` atau sandboxed parsing).  
- Pertimbangkan untuk menambahkan *rate limiter* sederhana agar API tidak boros.  
- Gunakan modul `st.session_state` untuk menjaga konteks percakapan dalam satu sesi.

---

### 12. Ringkasan Filosofi Produk

> **“Teach the process, not the answer.”**  
> Chatbot ini bukan alat untuk mempercepat jawaban, tetapi alat untuk memperlambat proses berpikir — agar mahasiswa memahami bagaimana algoritma bekerja dari dalam.

---

**Dokumen Terkait:**  
- [`prd.md`](./prd.md) – Deskripsi fitur dan kebutuhan produk.  
- `design_prompt.txt` – (opsional) panduan perilaku chatbot untuk fine-tuning prompt.  
- `system_prompt.txt` – pesan sistem untuk memastikan gaya komunikasi sesuai pedagogi.

---

**Penulis:**  
Tim Pengembang Chatbot PTI UMS  
**Tanggal:** Oktober 2025  
**Repository:** [GitHub - Chatbot Pembelajaran Algoritma](#)

# Claude Notes (Tambahan Fitur)
## Section: System Prompt Configuration (Admin)

---

### 1. Tujuan Fitur
Memberikan fleksibilitas kepada dosen atau admin untuk menyesuaikan karakter chatbot tanpa mengubah kode Python.

Chatbot perlu beradaptasi dengan konteks pembelajaran:
- Untuk mahasiswa baru: gaya komunikasi santai, banyak analogi.
- Untuk kelas lanjut: gaya lebih teknis dan formal.
Fitur ini memungkinkan admin mengatur “kepribadian” chatbot sesuai kebutuhan pembelajaran.

---

### 2. Desain Fungsional
**Komponen UI (Streamlit - Admin Page):**
- Judul: *System Prompt Setting*
- Komponen:
  - `st.text_area("System Prompt", value=current_prompt, height=300)`
  - Tombol `Save Prompt`
  - Tombol `Reset to Default`

**Fungsi Backend:**
- Prompt disimpan dalam file `system_prompt.txt` di direktori server.
- Saat chatbot dimulai atau setiap request baru, sistem membaca isi file prompt terbaru.
- Jika file tidak ditemukan, akan dibuat otomatis dengan default prompt.
- Tombol “Reset” akan menimpa isi file dengan template bawaan.

---

### 3. Contoh Struktur Kode (konseptual)
```python
import streamlit as st
from pathlib import Path

PROMPT_FILE = Path("system_prompt.txt")
DEFAULT_PROMPT = """Kamu adalah chatbot pembelajaran algoritma...
Jangan berikan kode, fokus pada langkah berpikir."""

def load_prompt():
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text()
    else:
        PROMPT_FILE.write_text(DEFAULT_PROMPT)
        return DEFAULT_PROMPT

def admin_prompt_page():
    st.header("System Prompt Setting")
    prompt_text = st.text_area("Edit System Prompt", value=load_prompt(), height=300)
    if st.button("Save Prompt"):
        PROMPT_FILE.write_text(prompt_text)
        st.success("Prompt saved successfully.")
    if st.button("Reset to Default"):
        PROMPT_FILE.write_text(DEFAULT_PROMPT)
        st.warning("Prompt reset to default.")
