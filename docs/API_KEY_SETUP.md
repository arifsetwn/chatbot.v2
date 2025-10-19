# API Key Setup Guide

## 🔑 Cara Mendapatkan API Keys

### 1. Google Gemini API Key

#### Langkah-langkah:

1. **Buka Google AI Studio**
   - Kunjungi: https://makersuite.google.com/app/apikey
   - Atau: https://aistudio.google.com/

2. **Login dengan Google Account**
   - Gunakan akun Google Anda
   - Setujui Terms of Service

3. **Create API Key**
   - Klik tombol "Create API Key"
   - Pilih project (atau buat project baru)
   - Copy API key yang dihasilkan

4. **Tambahkan ke .env**
   ```bash
   GEMINI_API_KEY=AIzaSy...
   ```

#### Quota & Pricing:
- **Free Tier**: 60 requests per minute
- **Paid Tier**: Custom quota
- Info lengkap: https://ai.google.dev/pricing

---

### 2. OpenAI API Key

#### Langkah-langkah:

1. **Buka OpenAI Platform**
   - Kunjungi: https://platform.openai.com/

2. **Sign Up / Login**
   - Buat account baru atau login
   - Verify email

3. **Add Payment Method** (diperlukan)
   - Klik "Settings" → "Billing"
   - Tambahkan credit card
   - Add credit ($5 minimum recommended)

4. **Create API Key**
   - Klik "API Keys" di sidebar
   - Klik "Create new secret key"
   - Beri nama (contoh: "Chatbot Algoritma")
   - Copy key (SIMPAN dengan aman, tidak bisa dilihat lagi!)

5. **Tambahkan ke .env**
   ```bash
   OPENAI_API_KEY=sk-proj-...
   ```

#### Quota & Pricing:
- **No Free Tier** (kecuali trial credit $5)
- **GPT-3.5-turbo**: $0.0015 / 1K tokens (~750 words)
- **GPT-4**: $0.03 / 1K tokens
- Info lengkap: https://openai.com/pricing

---

## 📝 Update Configuration

### File: `.env`

```bash
# API Keys
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here

# Model Selection
ACTIVE_MODEL=gemini              # Primary: 'gemini' or 'openai'
GEMINI_MODEL=gemini-pro
OPENAI_MODEL=gpt-3.5-turbo

# Rate Limits
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
GLOBAL_RATE_LIMIT=60
```

### Penjelasan:

- **ACTIVE_MODEL**: Model utama yang digunakan
  - `gemini`: Gunakan Google Gemini sebagai primary
  - `openai`: Gunakan OpenAI sebagai primary

- **GEMINI_API_KEY**: API key dari Google AI Studio
- **OPENAI_API_KEY**: API key dari OpenAI Platform

- **GEMINI_MODEL**: 
  - `gemini-pro`: Model standar (recommended)
  - `gemini-pro-vision`: Untuk image input

- **OPENAI_MODEL**:
  - `gpt-3.5-turbo`: Lebih murah, cepat (recommended)
  - `gpt-4`: Lebih akurat, mahal
  - `gpt-4-turbo`: Balance antara speed & accuracy

---

## 🔄 Fallback Mechanism

Sistem akan otomatis menggunakan fallback jika primary model gagal:

### Contoh 1: Primary = Gemini
```
User Request → Try Gemini
               ↓ (if fail)
               Try OpenAI (fallback)
               ↓ (if fail)
               Show error
```

### Contoh 2: Primary = OpenAI
```
User Request → Try OpenAI
               ↓ (if fail)
               Try Gemini (fallback)
               ↓ (if fail)
               Show error
```

---

## ⚠️ Troubleshooting

### Error: "Gemini API key not provided"

**Solusi:**
1. Pastikan `.env` file ada
2. Pastikan `GEMINI_API_KEY` atau `GOOGLE_API_KEY` diisi
3. Restart Streamlit app

---

### Error: "OpenAI API key not provided"

**Solusi:**
1. Pastikan `.env` file ada
2. Pastikan `OPENAI_API_KEY` diisi dengan key yang valid
3. Check format: harus diawali dengan `sk-`

---

### Error: "You exceeded your current quota"

**Penyebab:** Quota OpenAI habis atau billing issue

**Solusi:**
1. Check billing: https://platform.openai.com/account/billing
2. Add credit jika balance habis
3. Atau ubah `ACTIVE_MODEL=gemini` untuk gunakan Gemini
4. Sistem akan auto-fallback ke Gemini jika sudah dikonfigurasi

---

### Error: "Rate limit exceeded"

**Penyebab:** Terlalu banyak request dalam waktu singkat

**Solusi:**
1. Tunggu beberapa detik/menit
2. Turunkan `RATE_LIMIT_PER_MINUTE` di `.env`
3. Upgrade tier API (jika perlu)

---

### Warning: "Could not initialize ... client"

**Penyebab:** API key tidak valid atau tidak ada

**Solusi:**
1. Check API key di `.env`
2. Test connection:
   ```bash
   python -c "from utils.llm.llm_manager import LLMManager; print(LLMManager.from_env().test_all_providers())"
   ```
3. Regenerate API key jika perlu

---

## 💡 Best Practices

### 1. **Gunakan Gemini sebagai Primary** (Recommended)
- Lebih murah (Free tier available)
- Good performance untuk bahasa Indonesia
- Fallback ke OpenAI jika perlu

```bash
ACTIVE_MODEL=gemini
```

### 2. **Set Rate Limits yang Wajar**
```bash
RATE_LIMIT_PER_MINUTE=10      # 10 requests per menit per user
RATE_LIMIT_PER_HOUR=100       # 100 requests per jam per user
GLOBAL_RATE_LIMIT=60          # 60 requests per menit total
```

### 3. **Monitor API Usage**
- Google Gemini: https://makersuite.google.com/app/prompts
- OpenAI: https://platform.openai.com/usage

### 4. **Protect API Keys**
- ❌ NEVER commit `.env` to git
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables in production
- ✅ Rotate keys regularly

### 5. **Cost Optimization**
- Use Gemini for most queries (free)
- Use OpenAI only for complex reasoning
- Set appropriate rate limits
- Monitor usage dashboard

---

## 📊 Cost Estimation

### Gemini (Free Tier)
- **60 requests/minute**: FREE
- Suitable untuk 100-200 students

### OpenAI GPT-3.5-turbo
- **Average chat**: ~500 tokens = $0.00075
- **100 chats/day**: ~$0.075/day = $2.25/month
- **1000 chats/day**: ~$0.75/day = $22.5/month

### Recommendation
- Start dengan Gemini (free)
- Add OpenAI sebagai fallback ($5-10/month)
- Monitor usage dan adjust

---

## 🚀 Quick Start

1. **Get Gemini API Key** (5 menit)
   - https://makersuite.google.com/app/apikey
   - Copy key

2. **Update .env**
   ```bash
   GEMINI_API_KEY=paste_your_key_here
   ACTIVE_MODEL=gemini
   ```

3. **Restart Streamlit**
   ```bash
   streamlit run app.py
   ```

4. **Test**
   - Buka `/Chat`
   - Send message
   - Should work! 🎉

---

## 📚 Resources

- **Gemini Docs**: https://ai.google.dev/docs
- **OpenAI Docs**: https://platform.openai.com/docs
- **Pricing Gemini**: https://ai.google.dev/pricing
- **Pricing OpenAI**: https://openai.com/pricing
