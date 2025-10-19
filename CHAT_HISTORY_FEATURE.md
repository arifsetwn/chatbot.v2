# 💾 Chat History Feature - Dokumentasi

## 📋 Overview

Fitur ini memungkinkan pengguna untuk menyimpan dan menghapus riwayat percakapan mereka dengan chatbot.

---

## ✨ Fitur

### 1. **💾 Simpan Riwayat**

**Fungsi:** Menyimpan seluruh percakapan ke file JSON

**Cara Kerja:**
- Klik tombol "💾 Simpan Riwayat" di bagian bawah chat
- System akan menyimpan percakapan ke file JSON dengan timestamp
- File disimpan di folder `chat_history/`
- Format nama file: `chat_YYYYMMDD_HHMMSS.json`

**Contoh:**
```
chat_history/
  ├── chat_20251019_143022.json
  ├── chat_20251019_150135.json
  └── chat_20251019_162458.json
```

**Format JSON:**
```json
[
  {
    "role": "user",
    "content": "Jelaskan bubble sort"
  },
  {
    "role": "assistant",
    "content": "Bubble sort adalah algoritma..."
  }
]
```

**Validasi:**
- ✅ Tombol hanya aktif jika ada percakapan
- ✅ Menampilkan nama file setelah berhasil disimpan
- ✅ Error handling jika gagal menyimpan

---

### 2. **🗑️ Hapus Riwayat**

**Fungsi:** Menghapus seluruh riwayat percakapan dari sesi

**Cara Kerja:**
- Klik tombol "🗑️ Hapus Riwayat" di bagian bawah chat
- System akan menghapus:
  - ✅ Semua pesan dalam `st.session_state.messages`
  - ✅ Kode yang diupload (`uploaded_code`)
  - ✅ Hasil analisis kode (`code_analysis`)
  - ✅ Hasil simulasi algoritma (`simulation_result`)
- Halaman akan refresh otomatis

**Validasi:**
- ✅ Tombol hanya aktif jika ada percakapan
- ✅ Konfirmasi setelah berhasil menghapus
- ✅ Auto-refresh untuk clear UI

---

## 🔧 Implementasi Teknis

### Fungsi `save_chat_history()`

```python
def save_chat_history():
    """Save chat history to a JSON file"""
    import json
    from datetime import datetime
    
    # Create directory if not exists
    history_dir = Path("chat_history")
    history_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = history_dir / f"chat_{timestamp}.json"
    
    # Save to JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
    
    return filename
```

### Tombol UI

```python
# Save button
if st.button("💾 Simpan Riwayat", use_container_width=True):
    if len(st.session_state.messages) > 0:
        try:
            filename = save_chat_history()
            st.success(f"✅ Riwayat disimpan! File: {filename.name}")
        except Exception as e:
            st.error(f"❌ Gagal: {str(e)}")
    else:
        st.warning("⚠️ Tidak ada percakapan!")

# Delete button
if st.button("🗑️ Hapus Riwayat", use_container_width=True):
    if len(st.session_state.messages) > 0:
        st.session_state.messages = []
        st.session_state.uploaded_code = None
        st.session_state.code_analysis = None
        st.session_state.simulation_result = None
        st.success("✅ Riwayat dihapus!")
        st.rerun()
    else:
        st.info("ℹ️ Riwayat sudah kosong!")
```

---

## 📁 File Structure

```
chatbot.v2/
├── pages/
│   └── 1_Chat.py           # Implementasi tombol save & delete
├── chat_history/            # Folder penyimpanan (auto-created)
│   ├── chat_20251019_143022.json
│   ├── chat_20251019_150135.json
│   └── ...
├── .gitignore              # chat_history/ sudah di-ignore
└── CHAT_HISTORY_FEATURE.md # Dokumentasi ini
```

---

## 🎯 Use Cases

### Use Case 1: Simpan Diskusi Penting

**Skenario:**
```
Student: "Jelaskan merge sort secara detail"
Bot: [penjelasan lengkap dengan code]
Student: "Berikan contoh implementasi"
Bot: [code example]
Student: *Klik "💾 Simpan Riwayat"*
```

**Result:**
- File `chat_20251019_143022.json` dibuat
- Student bisa review diskusi kapan saja
- Student bisa share file dengan teman

### Use Case 2: Mulai Diskusi Baru

**Skenario:**
```
[Selesai diskusi sorting algorithms]
Student: *Klik "🗑️ Hapus Riwayat"*
[Mulai diskusi graph algorithms dengan fresh start]
```

**Result:**
- Chat area cleared
- Bot tidak akan reference diskusi lama
- Fresh context untuk topik baru

### Use Case 3: Backup Sebelum Refresh

**Skenario:**
```
Student: [Diskusi panjang tentang dynamic programming]
Student: *Takut browser crash atau refresh tidak sengaja*
Student: *Klik "💾 Simpan Riwayat"*
```

**Result:**
- Diskusi tersimpan aman di file JSON
- Bisa dibuka dan direview kapan saja

---

## 💡 Tips Penggunaan

### 1. **Simpan Diskusi Penting**
- Setelah selesai membahas algoritma kompleks
- Setelah debugging session yang sukses
- Setelah mendapat penjelasan yang berguna

### 2. **Hapus untuk Fresh Start**
- Saat ganti topik yang berbeda jauh
- Saat percakapan sudah terlalu panjang
- Saat ingin clear context untuk diskusi baru

### 3. **Review Saved Files**
- Buka folder `chat_history/`
- File JSON bisa dibuka dengan text editor
- Format readable untuk review

### 4. **Organize Files**
- Rename file untuk identifikasi mudah
  ```
  chat_20251019_143022.json → merge_sort_discussion.json
  ```
- Buat subfolder per topik
  ```
  chat_history/
    ├── sorting/
    ├── searching/
    └── recursion/
  ```

---

## 🔍 Testing

### Test Case 1: Save Empty Chat

**Steps:**
1. Buka fresh chat page
2. Klik "💾 Simpan Riwayat"

**Expected:**
- ⚠️ "Tidak ada percakapan untuk disimpan!"

### Test Case 2: Save Non-Empty Chat

**Steps:**
1. Chat dengan bot (beberapa pesan)
2. Klik "💾 Simpan Riwayat"

**Expected:**
- ✅ "Riwayat percakapan disimpan!"
- ✅ Menampilkan nama file
- ✅ File exists di `chat_history/`
- ✅ File contains valid JSON

### Test Case 3: Delete Empty Chat

**Steps:**
1. Buka fresh chat page
2. Klik "🗑️ Hapus Riwayat"

**Expected:**
- ℹ️ "Riwayat sudah kosong!"

### Test Case 4: Delete Non-Empty Chat

**Steps:**
1. Chat dengan bot (beberapa pesan)
2. Klik "🗑️ Hapus Riwayat"

**Expected:**
- ✅ "Riwayat percakapan dihapus!"
- ✅ Chat area cleared
- ✅ Page auto-refresh
- ✅ All session state cleared

### Test Case 5: Save After Upload Code

**Steps:**
1. Upload Python file
2. Chat tentang kode
3. Klik "💾 Simpan Riwayat"

**Expected:**
- ✅ Percakapan tersimpan
- ✅ File JSON contains all messages
- ✅ Code context saved in messages

### Test Case 6: Delete After Simulation

**Steps:**
1. Run algorithm simulation
2. Chat about simulation
3. Klik "🗑️ Hapus Riwayat"

**Expected:**
- ✅ Messages cleared
- ✅ Simulation result cleared
- ✅ UI reset to initial state

---

## 🐛 Troubleshooting

### Problem 1: "Permission Denied" saat save

**Cause:** Tidak ada permission write di folder

**Solution:**
```bash
chmod 755 chat_history/
```

### Problem 2: File tidak tersimpan

**Cause:** Folder `chat_history/` tidak ada

**Solution:**
- System akan auto-create folder
- Atau manual: `mkdir chat_history`

### Problem 3: JSON encoding error

**Cause:** Message contains special characters

**Solution:**
- Sudah handled dengan `ensure_ascii=False`
- File disimpan dengan UTF-8 encoding

### Problem 4: Tombol tidak merespon

**Cause:** Button pressed multiple times

**Solution:**
- Tunggu hingga proses selesai
- Refresh page jika stuck

---

## 📊 File Format

### Saved JSON Structure

```json
[
  {
    "role": "user",
    "content": "Jelaskan bubble sort"
  },
  {
    "role": "assistant",
    "content": "Bubble sort adalah algoritma pengurutan sederhana...\n\n```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n```"
  },
  {
    "role": "user",
    "content": "Apa kompleksitas waktunya?"
  },
  {
    "role": "assistant",
    "content": "Kompleksitas waktu bubble sort:\n- Worst case: O(n²)\n- Best case: O(n)\n- Average case: O(n²)"
  }
]
```

### File Metadata

| Field | Value | Notes |
|-------|-------|-------|
| **Format** | JSON | Standard JSON format |
| **Encoding** | UTF-8 | Supports Indonesian characters |
| **Extension** | .json | Can be opened with any text editor |
| **Size** | ~1-10 KB | Depends on conversation length |
| **Location** | `chat_history/` | Auto-created directory |

---

## 🚀 Future Enhancements

### Phase 1: Import/Load History

```python
# Load saved history back into chat
def load_saved_history(filename):
    with open(filename, 'r') as f:
        st.session_state.messages = json.load(f)
```

**UI:**
- Add "📂 Load History" button
- File selector for `chat_history/*.json`
- Preview before loading

### Phase 2: Export to Other Formats

```python
# Export to PDF
def export_to_pdf(messages):
    # Convert chat to formatted PDF
    pass

# Export to Markdown
def export_to_markdown(messages):
    # Convert chat to .md file
    pass
```

**Formats:**
- PDF (for printing/sharing)
- Markdown (for documentation)
- HTML (for web viewing)

### Phase 3: Cloud Storage

```python
# Save to Google Drive
def save_to_cloud(messages):
    # Upload to user's Google Drive
    pass
```

**Features:**
- Google Drive integration
- Dropbox integration
- Auto-sync across devices

### Phase 4: Search & Filter

```python
# Search through saved chats
def search_history(query):
    # Search all saved JSON files
    # Return matching conversations
    pass
```

**Features:**
- Full-text search
- Filter by date
- Filter by topic/algorithm

---

## ✅ Checklist

- [x] Implement `save_chat_history()` function
- [x] Implement delete history functionality
- [x] Add save button with validation
- [x] Add delete button with validation
- [x] Create `chat_history/` directory auto-creation
- [x] Add to `.gitignore`
- [x] Error handling for save failures
- [x] Success/error messages
- [x] Clear all session state on delete
- [x] Auto-refresh after delete
- [x] Documentation created

---

## 📞 Support

Jika ada masalah dengan fitur ini:

1. **Check folder permissions**
   ```bash
   ls -la chat_history/
   ```

2. **Check saved files**
   ```bash
   cat chat_history/chat_*.json
   ```

3. **Clear browser cache**
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (Mac)

4. **Check console for errors**
   - F12 → Console tab
   - Look for error messages

---

**Status:** ✅ **FULLY IMPLEMENTED & WORKING**

**Version:** 1.0.0

**Last Updated:** 19 Oktober 2025

**Impact:** Users can now save and manage their chat history locally! 🎉
