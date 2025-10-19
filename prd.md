# Product Requirement Document (PRD)
## Chatbot Pembelajaran Algoritma Berbasis Website

---

## 1. Overview

**Nama Produk:** Chatbot Pembelajaran Algoritma  
**Platform:** Website (Streamlit)  
**Tujuan:**  
Membantu mahasiswa pemula memahami konsep algoritma dan cara berpikir komputasional. Chatbot tidak memberikan jawaban berupa kode, melainkan panduan dan penjelasan langkah demi langkah.

**Ruang Lingkup Versi MVP:**  
- Chatbot berbasis web dengan antarmuka percakapan.  
- Fitur utama:
  - Penjelasan konsep algoritma.
  - Simulasi langkah algoritma berdasarkan prinsip *computational thinking*.
  - Unggah kode Python untuk didiskusikan.
  - Visualisasi langkah eksekusi algoritma (step-by-step).
- Backend untuk admin/dosen:
  - Manajemen API key (Gemini / OpenAI).
  - Pemilihan model.
  - Rate limit konfigurasi.
  - Upload materi pembelajaran (PDF).
  - Dashboard aktivitas chatbot dan analitik sederhana.
- Sistem berdiri sendiri (tidak terintegrasi dengan LMS).
- Deploy di server kampus.

---

## 2. User Roles

| Role | Akses | Tujuan |
|------|--------|--------|
| Mahasiswa | Frontend Chatbot | Belajar konsep algoritma dan berlatih berpikir komputasional. Tidak memerlukan login. |
| Dosen | Frontend & Backend | Dapat berinteraksi dengan chatbot dan mengunggah materi pembelajaran. |
| Admin | Backend | Mengelola API, model, materi, dan monitoring aktivitas. |

---

## 3. System Architecture

**Framework:** Streamlit  
**Bahasa:** Python  
**Deployment:** Server kampus  
**API:** Gemini / OpenAI (dikonfigurasi di backend)

### Komponen Utama:
1. **Frontend (Chatbot Page)**
   - Chat interface (chat bubble, input bar, upload file).
   - Sidebar untuk topik algoritma.
   - Local storage untuk menyimpan riwayat percakapan di browser.
   - Mengirim permintaan ke backend via REST API.

2. **Backend (Admin Panel)**
   - Autentikasi sederhana (username/password).
   - Menu:
     - API Key Management.
     - Model Selection (Gemini / OpenAI).
     - Rate Limit Configuration.
     - Upload PDF Material.
     - Analytics Dashboard (log chat, waktu respon, jumlah chat harian).

     

3. **LLM Integration**
   - Wrapper API untuk Gemini dan OpenAI.
   - Admin dapat memilih model aktif.
   - Respons model dikirim ke frontend.

4. **Data Storage**
   - Chat history mahasiswa: disimpan secara lokal di browser (localStorage).
   - Log admin (prompt, response, timestamp): disimpan di server (SQLite/JSON).

---

## 4. Chatbot Interaction Design

- Mode percakapan **free-form tanya jawab**.
- Gaya komunikasi **santai, membimbing, tidak memberikan jawaban langsung**.
- Chatbot memberikan petunjuk langkah demi langkah untuk membantu mahasiswa memahami algoritma.
- Mahasiswa dapat mengunggah kode Python (.py / .txt) untuk dijelaskan alur eksekusinya.
- Menampilkan simulasi langkah-langkah algoritma secara tekstual atau tabel sederhana.
- Menolak menjawab tugas/ujian secara langsung.  
  **Pesan contoh:**  
  > “Aku tidak bisa memberikan jawabannya langsung, tapi kita bisa bahas langkah-langkah penyelesaiannya.”

---

## 5. User Interface Design

### a. Frontend (Halaman Chatbot)
**Komponen:**
- Header (judul + tagline chatbot)
- Sidebar (daftar topik algoritma: sorting, searching, rekursi, dll)
- Chat window (percakapan pengguna dan chatbot)
- Input area (kolom teks + tombol kirim)
- Upload file button (unggah kode Python)
- Local chat history notification:  
  > “Riwayat percakapan tersimpan di browser Anda.”

**Desain:**  
- Responsif untuk desktop dan mobile.  
- Target waktu respon: <2 detik.  

### b. Backend (Halaman Admin)
**Fitur:**
1. Login (username & password)
2. API Key Management
3. Model Selection (Gemini / OpenAI)
4. Rate Limit Configuration
5. Upload PDF Material
6. Analytics Dashboard
7. **System Prompt Setting**
   - Admin dapat menulis, mengedit, dan menyimpan *system prompt* yang digunakan chatbot.
   - Disediakan editor teks (multiline) di halaman admin untuk menyesuaikan gaya bicara dan batasan chatbot.
   - Tombol **Save Prompt** untuk menyimpan ke file `system_prompt.txt` di server.
   - Tombol **Reset to Default** untuk mengembalikan ke prompt bawaan.


---

## 6. Technical Requirements

| Aspek | Spesifikasi |
|-------|--------------|
| Framework | Streamlit |
| Bahasa | Python |
| Deployment | Server kampus |
| Storage | LocalStorage (client) + SQLite / JSON (server logs) + `system_prompt.txt` |
| API | Gemini / OpenAI |
| Response Time | <2 detik |
| Pengguna simultan | ±20 |
| Uptime | ≥90% |
| Source control | GitHub |

---

## 7. Security and Privacy

- Tidak menyimpan data pribadi mahasiswa.
- Tidak ada login untuk mahasiswa.
- Autentikasi hanya di sisi admin.
- File `system_prompt.txt` hanya dapat diakses dan diubah oleh admin.
- Tidak mengirim data sensitif ke model LLM.
- **Disclaimer:**  
  > “Chatbot ini hanya memberikan panduan pemahaman, bukan jawaban langsung atas tugas atau ujian.”


---

## 8. Logging and Monitoring

- Data yang dicatat:
  - Prompt
  - Response
  - Timestamp
  - Model yang digunakan
  - User ID (anonymized)
- Dashboard analitik menampilkan:
  - Jumlah percakapan per hari
  - Rata-rata waktu respon
  - Status uptime
- Pesan fallback jika API gagal:  
  > “Sistem sedang maintenance, silakan coba beberapa saat lagi.”

---

## 9. Testing and Evaluation

**Metode:**  
- AB Testing dengan dua kelompok mahasiswa:
  - Kelompok A: menggunakan chatbot.
  - Kelompok B: belajar tanpa chatbot.

**Metrik:**  
- Relevansi jawaban.  
- Waktu respon chatbot.  
- Kepuasan pengguna (melalui survei sederhana).  

**Kriteria Penerimaan:**  
- Uptime ≥ 90%.  
- Jawaban relevan ≥ 80% menurut penilaian dosen.

---

## 10. Timeline and Resources

| Aktivitas | Durasi | Penanggung Jawab |
|------------|---------|------------------|
| Desain arsitektur & UI | 2 hari | Developer |
| Implementasi chatbot Streamlit | 3 hari | Developer |
| Uji coba internal & debugging | 1 hari | Developer |
| Deployment ke server kampus | 1 hari | Developer |
| **Total waktu** | **±1 minggu** | **1 Developer** |

---

## 11. Future Enhancements

- Integrasi dengan LMS (fase 2).
- Penilaian otomatis terhadap kode mahasiswa.
- Leaderboard dan sistem poin.
- Ekspansi materi algoritma interaktif.
- Visualisasi grafis untuk langkah algoritma.

---

## 12. Appendix

**Pesan Etika Sistem:**  
> “Chatbot ini berfungsi sebagai pendamping belajar yang memberikan panduan berpikir.  
> Ia tidak menggantikan peran dosen, dan tidak memberikan jawaban langsung atas soal atau tugas.”

**Repository:** [GitHub - Chatbot Pembelajaran Algoritma](#)

