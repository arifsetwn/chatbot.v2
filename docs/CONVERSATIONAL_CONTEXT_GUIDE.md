# 🧠 Conversational Context Memory - Documentation

## ✅ Status: Already Implemented!

Chatbot Anda **sudah memiliki kemampuan remember conversational context**. Fitur ini sudah aktif di `pages/1_Chat.py`.

---

## 🔍 Bagaimana Cara Kerjanya

### 1. **Message History Storage**

```python
# Di pages/1_Chat.py, line ~175
if 'messages' not in st.session_state:
    st.session_state.messages = []
```

**Fungsi:**
- Menyimpan semua pesan user dan assistant
- Tersimpan di `st.session_state` (in-memory per session)
- Bertahan selama browser tab tidak ditutup

### 2. **Context Passing ke LLM**

```python
# Di pages/1_Chat.py, line ~570-576
# Get conversation history for context (last 5 messages)
conversation_history = []
for msg in st.session_state.messages[-6:-1]:  # Exclude current prompt
    conversation_history.append({
        "role": msg["role"],
        "content": msg["content"]
    })

# Generate response with enhanced prompt
result = llm_manager.generate_response(
    prompt=prompt,
    system_prompt=enhanced_system_prompt,
    temperature=0.7,
    conversation_history=conversation_history  # ✅ CONTEXT PASSED HERE
)
```

**Cara Kerja:**
1. Ambil **5 pesan terakhir** (excluding pesan saat ini)
2. Format sebagai conversation history
3. Kirim ke LLM bersama prompt baru
4. LLM menggunakan context untuk response yang lebih relevan

### 3. **Display Message History**

```python
# Di pages/1_Chat.py, line ~478-480
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

**Fungsi:**
- Menampilkan semua pesan chat sebelumnya
- User bisa scroll dan lihat history lengkap
- Visual context untuk user

---

## 📊 Current Configuration

| Parameter | Value | Location |
|-----------|-------|----------|
| **History Length** | 5 messages | `pages/1_Chat.py` line 571 |
| **Storage Type** | Session State (in-memory) | `st.session_state.messages` |
| **Persistence** | Per browser session | Until tab closed |
| **Format** | List of dicts | `[{"role": "user/assistant", "content": "..."}]` |

---

## 🚀 Cara Meningkatkan Context Memory

### Option 1: Increase Context Window (Simple)

Ubah jumlah pesan yang diingat dari 5 menjadi lebih banyak:

```python
# BEFORE (line ~571)
for msg in st.session_state.messages[-6:-1]:  # Last 5 messages

# AFTER - Remember last 10 messages
for msg in st.session_state.messages[-11:-1]:  # Last 10 messages
```

**Trade-offs:**
- ✅ **Pro:** Lebih banyak konteks
- ❌ **Con:** Token usage lebih tinggi (biaya API)
- ❌ **Con:** Response time lebih lama

### Option 2: Persistent Storage (Advanced)

Simpan conversation history ke database/file untuk persistence antar sessions:

**A. SQLite Database:**

```python
import sqlite3
from datetime import datetime

def save_conversation_to_db(user_id, messages):
    """Save conversation to SQLite database"""
    conn = sqlite3.connect('data/conversations.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp TEXT,
            messages TEXT
        )
    ''')
    
    # Save messages as JSON
    import json
    cursor.execute(
        'INSERT INTO conversations (user_id, timestamp, messages) VALUES (?, ?, ?)',
        (user_id, datetime.now().isoformat(), json.dumps(messages))
    )
    
    conn.commit()
    conn.close()

def load_conversation_from_db(user_id, limit=1):
    """Load last N conversations from database"""
    conn = sqlite3.connect('data/conversations.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT messages FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        import json
        return json.loads(results[0][0])
    return []
```

**Usage:**

```python
# At app start - Load previous conversation
if 'messages' not in st.session_state:
    user_id = st.session_state.get('user_id', 'anonymous')
    st.session_state.messages = load_conversation_from_db(user_id)

# When saving (on certain events)
if st.sidebar.button("💾 Save Conversation"):
    user_id = st.session_state.get('user_id', 'anonymous')
    save_conversation_to_db(user_id, st.session_state.messages)
    st.success("✅ Conversation saved!")
```

**B. JSON File Storage (Simpler):**

```python
import json
from datetime import datetime

def save_conversation_to_file(user_id, messages):
    """Save conversation to JSON file"""
    filename = f"data/conversations/{user_id}_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'messages': messages
        }, f, indent=2)

def load_latest_conversation(user_id):
    """Load latest conversation for user"""
    import os
    import glob
    
    pattern = f"data/conversations/{user_id}_*.json"
    files = glob.glob(pattern)
    
    if not files:
        return []
    
    latest_file = max(files, key=os.path.getctime)
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
        return data['messages']
```

### Option 3: Smart Context Selection (AI-Powered)

Pilih pesan paling relevan berdasarkan similarity, bukan hanya yang terbaru:

```python
def get_relevant_context(current_prompt, all_messages, top_k=5):
    """Get most relevant messages for current prompt"""
    from sentence_transformers import SentenceTransformer
    import numpy as np
    
    # Load model (cache this in production)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Encode current prompt
    prompt_embedding = model.encode([current_prompt])
    
    # Encode all messages
    message_texts = [msg['content'] for msg in all_messages]
    message_embeddings = model.encode(message_texts)
    
    # Calculate similarities
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity(prompt_embedding, message_embeddings)[0]
    
    # Get top-k most similar messages
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    relevant_messages = [all_messages[i] for i in top_indices]
    
    return relevant_messages
```

**Usage:**

```python
# Instead of last N messages
conversation_history = get_relevant_context(
    prompt, 
    st.session_state.messages[:-1],  # Exclude current
    top_k=5
)
```

### Option 4: Summarization (For Long Conversations)

Ringkas conversation lama untuk menghemat tokens:

```python
def summarize_old_conversations(messages, threshold=20):
    """Summarize old messages if conversation is too long"""
    if len(messages) <= threshold:
        return messages
    
    # Keep recent messages as-is
    recent_messages = messages[-10:]
    
    # Summarize older messages
    old_messages = messages[:-10]
    old_text = "\n".join([f"{m['role']}: {m['content']}" for m in old_messages])
    
    # Use LLM to summarize
    summary_result = llm_manager.generate_response(
        prompt=f"Ringkas percakapan berikut dalam 2-3 kalimat:\n\n{old_text}",
        system_prompt="Kamu adalah asisten yang meringkas percakapan.",
        temperature=0.3
    )
    
    summary_message = {
        "role": "system",
        "content": f"[Ringkasan percakapan sebelumnya: {summary_result['response']}]"
    }
    
    return [summary_message] + recent_messages
```

---

## 🔧 Implementation Guide

### Quick Win: Increase Context Window

**File:** `pages/1_Chat.py`

**Location:** Line ~570-576

**Change:**

```python
# CURRENT (remembers 5 messages)
for msg in st.session_state.messages[-6:-1]:

# OPTION 1: Remember 10 messages
for msg in st.session_state.messages[-11:-1]:

# OPTION 2: Remember 20 messages (careful with tokens!)
for msg in st.session_state.messages[-21:-1]:

# OPTION 3: Remember ALL messages (not recommended for long chats)
for msg in st.session_state.messages[:-1]:
```

### Medium: Add Conversation Save/Load

**1. Create utility file:**

Create `utils/conversation_storage.py`:

```python
import json
import os
from datetime import datetime
from pathlib import Path

class ConversationStorage:
    """Manage conversation storage"""
    
    def __init__(self, storage_dir="data/conversations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_conversation(self, user_id, messages):
        """Save conversation to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.storage_dir / f"{user_id}_{timestamp}.json"
        
        data = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'message_count': len(messages),
            'messages': messages
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filename)
    
    def load_latest_conversation(self, user_id):
        """Load latest conversation for user"""
        pattern = f"{user_id}_*.json"
        files = list(self.storage_dir.glob(pattern))
        
        if not files:
            return []
        
        latest_file = max(files, key=lambda f: f.stat().st_ctime)
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
            return data['messages']
    
    def list_conversations(self, user_id):
        """List all conversations for user"""
        pattern = f"{user_id}_*.json"
        files = list(self.storage_dir.glob(pattern))
        
        conversations = []
        for file in sorted(files, key=lambda f: f.stat().st_ctime, reverse=True):
            with open(file, 'r') as f:
                data = json.load(f)
                conversations.append({
                    'filename': file.name,
                    'timestamp': data['timestamp'],
                    'message_count': data['message_count']
                })
        
        return conversations
```

**2. Integrate in Chat.py:**

```python
# At top
from utils.conversation_storage import ConversationStorage

# Initialize
conversation_storage = ConversationStorage()

# Add save button in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Conversation")

if st.sidebar.button("Save Conversation"):
    user_id = st.session_state.get('user_id', 'anonymous')
    filename = conversation_storage.save_conversation(user_id, st.session_state.messages)
    st.sidebar.success(f"✅ Saved!")

if st.sidebar.button("Load Last Conversation"):
    user_id = st.session_state.get('user_id', 'anonymous')
    messages = conversation_storage.load_latest_conversation(user_id)
    if messages:
        st.session_state.messages = messages
        st.rerun()
    else:
        st.sidebar.warning("No saved conversations found")

# Show conversation history
conversations = conversation_storage.list_conversations('anonymous')
if conversations:
    st.sidebar.markdown("**Recent Conversations:**")
    for conv in conversations[:5]:
        st.sidebar.text(f"📝 {conv['message_count']} msgs - {conv['timestamp'][:10]}")
```

---

## 📈 Recommended Configuration

### For Your Use Case (Educational Chatbot):

```python
# Good balance of context vs cost
CONTEXT_WINDOW = 10  # Last 10 messages (5 exchanges)
MAX_TOKENS = 4000    # Limit total tokens
SAVE_FREQUENCY = "manual"  # User clicks save button
```

**Reasoning:**
- ✅ 10 messages = 5 Q&A pairs (good for algorithm discussions)
- ✅ Manageable token usage
- ✅ Good enough for most learning scenarios
- ✅ Manual save gives user control

---

## 🎯 Action Items

### Immediate (5 minutes):

1. **Increase context window to 10 messages:**
   ```python
   # pages/1_Chat.py, line ~571
   for msg in st.session_state.messages[-11:-1]:  # Was -6:-1
   ```

### Short-term (30 minutes):

2. **Add conversation save/load:**
   - Create `utils/conversation_storage.py`
   - Add save/load buttons to sidebar
   - Test functionality

### Long-term (2-3 hours):

3. **Implement smart context selection:**
   - Add sentence-transformers
   - Implement similarity-based selection
   - A/B test with users

---

## 🧪 Testing Context Memory

Test apakah context memory bekerja:

```
User: Jelaskan bubble sort
Bot: [explains bubble sort]

User: Bagaimana kompleksitasnya?
Bot: [should remember we're talking about bubble sort]

User: Bandingkan dengan yang tadi
Bot: [should compare with bubble sort without being told explicitly]

User: Implementasikan itu
Bot: [should know "itu" = bubble sort]
```

Jika bot bisa menjawab tanpa user mengulang context, **memory works!** ✅

---

## 📊 Monitoring Context Usage

Add to Admin dashboard:

```python
# Show context stats
st.metric("Avg Messages per Session", avg_messages)
st.metric("Avg Context Window Used", avg_context_tokens)
st.metric("Total Conversations Saved", total_saved)
```

---

**Status:** ✅ Context memory sudah aktif (5 messages)
**Recommendation:** Tingkatkan ke 10-15 messages untuk learning experience yang lebih baik
**Next Step:** Test dengan real conversations

Last Updated: 19 Oktober 2025
