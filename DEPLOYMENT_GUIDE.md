# Deployment Guide - Streamlit Cloud

## 🚨 Error Yang Diperbaiki

Error yang terjadi:
```
❗️ installer returned a non-zero exit code
❗️ Error during processing dependencies!
```

### Penyebab:
1. ❌ `sqlite3` di requirements.txt (ini built-in Python module)
2. ❌ `pathlib2` tidak diperlukan untuk Python 3.4+
3. ❌ Versi dependency yang tidak kompatibel

### Solusi:
✅ Hapus `sqlite3` dari requirements.txt
✅ Hapus `pathlib2` dari requirements.txt
✅ Pin versi `streamlit-authenticator` ke `0.4.2`
✅ Gunakan versi stable untuk semua dependencies

---

## 📋 Prerequisites

1. **GitHub Repository** dengan kode aplikasi
2. **Streamlit Cloud Account** (https://streamlit.io/cloud)
3. **API Keys:**
   - Gemini API Key (dari https://aistudio.google.com/app/apikey)
   - OpenAI API Key (opsional)

---

## 🚀 Step-by-Step Deployment

### 1. Persiapan File

Pastikan file-file berikut ada dan benar:

#### ✅ `requirements.txt`
```txt
streamlit==1.39.0
streamlit-authenticator==0.4.2
PyYAML==6.0.2
google-generativeai==0.8.3
openai==1.54.5
pandas==2.2.3
numpy==1.26.4
python-dotenv==1.0.1
cryptography==43.0.3
```

**PENTING:**
- ❌ JANGAN include `sqlite3` (sudah built-in)
- ❌ JANGAN include `pathlib2` (tidak diperlukan)
- ❌ JANGAN include dev dependencies (pytest, black, flake8)

#### ✅ `packages.txt` (kosong atau hapus jika tidak perlu)
```txt
# System packages (leave empty if none needed)
```

#### ✅ `.streamlit/config.toml`
```toml
[client]
showErrorDetails = true

[runner]
magicEnabled = true
fastReruns = true

[server]
headless = true
runOnSave = false
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

#### ✅ File structure:
```
chatbot.v2/
├── app.py                          # Entry point
├── requirements.txt                # Dependencies
├── packages.txt                    # System packages (optional)
├── .streamlit/
│   ├── config.toml                # Streamlit config
│   └── secrets.toml.example       # Secrets template
├── pages/
│   ├── 1_Chat.py
│   └── 2_Admin.py
├── utils/
│   ├── llm/
│   ├── algorithm_simulator.py
│   ├── question_detector.py
│   ├── code_analyzer.py
│   └── rate_limiter.py
└── data/
    └── system_prompt.txt
```

### 2. Push ke GitHub

```bash
# Add semua file
git add .

# Commit changes
git commit -m "Fix: Remove sqlite3 and pathlib2 from requirements.txt for Streamlit Cloud deployment"

# Push ke GitHub
git push origin main
```

### 3. Deploy ke Streamlit Cloud

1. **Login ke Streamlit Cloud:**
   - Buka https://streamlit.io/cloud
   - Sign in dengan GitHub account

2. **Create New App:**
   - Click "New app"
   - Repository: pilih repository Anda
   - Branch: `main` (atau branch yang Anda gunakan)
   - Main file path: `app.py`
   - App URL: pilih custom URL (optional)

3. **Add Secrets:**
   Click "Advanced settings" → "Secrets"
   
   Paste konfigurasi ini (sesuaikan dengan API key Anda):
   
   ```toml
   # API Keys
   GEMINI_API_KEY = "AIzaSy..."
   GOOGLE_API_KEY = "AIzaSy..."
   
   # Optional: OpenAI (jika ingin enable fallback)
   # OPENAI_API_KEY = "sk-proj-..."
   
   # Application Settings
   APP_NAME = "Chatbot Pembelajaran Algoritma"
   SECRET_KEY = "your_random_secret_key_here"
   ADMIN_USERNAME = "admin"
   ADMIN_PASSWORD = "change_this_password"
   
   # Rate Limiting
   RATE_LIMIT_PER_MINUTE = "10"
   RATE_LIMIT_PER_HOUR = "100"
   GLOBAL_RATE_LIMIT = "60"
   
   # Model Settings
   ACTIVE_MODEL = "gemini"
   GEMINI_MODEL = "gemini-2.0-flash"
   ```

4. **Deploy:**
   - Click "Deploy!"
   - Wait for deployment (biasanya 2-5 menit)

### 4. Verifikasi Deployment

Setelah deployment selesai:

1. ✅ Check app URL bisa diakses
2. ✅ Test halaman Chat - pastikan bisa load
3. ✅ Test halaman Admin - coba login
4. ✅ Test kirim message di Chat - pastikan LLM merespon
5. ✅ Test Algorithm Simulator di sidebar
6. ✅ Test upload file Python

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'sqlite3'"

**Penyebab:** `sqlite3` ada di requirements.txt

**Solusi:**
```bash
# Edit requirements.txt, hapus baris "sqlite3"
git add requirements.txt
git commit -m "Fix: Remove sqlite3 from requirements"
git push
```

Streamlit Cloud akan auto-redeploy.

### Error: "Could not find a version that satisfies the requirement..."

**Penyebab:** Versi package tidak kompatibel

**Solusi:** Gunakan `requirements-minimal.txt` yang sudah disediakan:
```bash
cp requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "Use minimal requirements for deployment"
git push
```

### Error: "Failed to load secrets"

**Penyebab:** Secrets tidak di-set atau format salah

**Solusi:**
1. Buka Streamlit Cloud dashboard
2. Pilih app Anda
3. Settings → Secrets
4. Paste secrets dengan format TOML yang benar
5. Save dan reboot app

### Error: "Import error" atau "Cannot import utils..."

**Penyebab:** File structure tidak sesuai atau file tidak ter-commit

**Solusi:**
```bash
# Check semua file utils/ sudah ter-commit
git status

# Add missing files
git add utils/
git add data/
git commit -m "Add missing utils and data files"
git push
```

### App stuck di "Running..."

**Penyebab:** Infinite loop atau long initialization

**Solusi:**
1. Check logs di Streamlit Cloud dashboard
2. Pastikan tidak ada blocking code di `app.py`
3. Restart app dari dashboard

---

## 📊 Monitoring

### Check Logs:
1. Buka Streamlit Cloud dashboard
2. Pilih app Anda
3. Klik "Manage app" → "Logs"
4. Monitor real-time logs untuk debug

### Check Resource Usage:
- Streamlit Cloud free tier: 1 GB RAM
- Jika app crash karena memory, optimize code atau upgrade plan

### Performance Tips:
1. Use `@st.cache_data` untuk caching
2. Use `@st.cache_resource` untuk LLM clients
3. Limit file upload size (sudah di-set 1MB)
4. Implement rate limiting (sudah di-implement)

---

## 🔒 Security Checklist

- ✅ `.env` file di-gitignore
- ✅ `.streamlit/secrets.toml` di-gitignore
- ✅ API keys di Streamlit Secrets (bukan di code)
- ✅ Admin password di-change dari default
- ✅ XSRF protection enabled
- ✅ Rate limiting implemented

---

## 🎉 Post-Deployment

Setelah app live:

1. **Share URL:** https://your-app.streamlit.app
2. **Monitor usage:** Check logs regularly
3. **Update secrets:** Rotate API keys secara berkala
4. **Backup data:** Download logs/data penting
5. **User feedback:** Gather feedback untuk improvements

---

## 📞 Support

Jika masih ada masalah:

1. **Streamlit Community:** https://discuss.streamlit.io/
2. **Documentation:** https://docs.streamlit.io/
3. **GitHub Issues:** Buat issue di repository Anda

---

## 🔄 Update Application

Untuk update code setelah deployment:

```bash
# 1. Make changes locally
# 2. Test locally: streamlit run app.py
# 3. Commit and push:
git add .
git commit -m "Update: description of changes"
git push

# 4. Streamlit Cloud will auto-deploy (takes ~2-5 minutes)
```

---

**Last Updated:** 19 Oktober 2025

**Status:** ✅ Ready for Production Deployment
