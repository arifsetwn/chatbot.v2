import streamlit as st
import time
from pathlib import Path
import json
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.llm.llm_manager import LLMManager, ModelProvider
from utils.rate_limiter import RateLimiter
from utils.question_detector import QuestionDetector, QuestionType
from utils.code_analyzer import CodeAnalyzer
from utils.algorithm_simulator import AlgorithmSimulator
from dotenv import load_dotenv

st.set_page_config(
    page_title="Alprobot - Chatbot Algoritma",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sidebar-topic {
        background-color: #f0f8ff;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
    }
    .disclaimer-box {
        background-color: #fff9e6;
        border: 2px solid #ff9800;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #333;
        font-size: 1.05em;
    }
    .disclaimer-box strong {
        color: #ff6f00;
    }
    /* Chat message styling */
    .stChatMessage {
        margin-bottom: 1rem;
        padding: 0.8rem;
        border-radius: 8px;
    }
    /* Chat input area */
    .stChatInput {
        border-radius: 10px;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💬 Alprobot - Chatbot Pembelajaran Algoritma</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2em;">Mari belajar algoritma bersama-sama!</p>', unsafe_allow_html=True)

# Disclaimer with better styling
st.markdown("""
<div class="disclaimer-box">
    <div style="margin-bottom: 0.5rem;">
        <strong>⚠️ Penting:</strong>
    </div>
    <div style="line-height: 1.6;">
        Chatbot ini memberikan <strong>panduan berpikir</strong>, bukan jawaban langsung.
        Untuk tugas atau ujian, diskusikan dengan dosen Anda.
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_code" not in st.session_state:
    st.session_state.uploaded_code = None

if "code_analysis" not in st.session_state:
    st.session_state.code_analysis = None

# Initialize LLM Manager and Rate Limiter
@st.cache_resource
def init_llm_manager():
    """Initialize LLM Manager (cached to avoid re-initialization)"""
    try:
        load_dotenv()
        return LLMManager.from_env()
    except Exception as e:
        st.error(f"⚠️ Error initializing LLM: {e}")
        return None

@st.cache_resource
def init_rate_limiter():
    """Initialize Rate Limiter (cached)"""
    try:
        return RateLimiter.from_env()
    except Exception as e:
        st.warning(f"Rate limiter initialization failed: {e}")
        return RateLimiter()  # Use defaults

@st.cache_resource
def init_question_detector():
    """Initialize Question Detector"""
    return QuestionDetector()

@st.cache_resource
def init_code_analyzer():
    """Initialize Code Analyzer"""
    return CodeAnalyzer()

@st.cache_resource
def init_algorithm_simulator():
    """Initialize Algorithm Simulator"""
    return AlgorithmSimulator()

# Load system prompt
def load_system_prompt():
    """Load system prompt from file"""
    prompt_file = Path("data/system_prompt.txt")
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return """Kamu adalah asisten pembelajaran algoritma yang membantu mahasiswa memahami konsep algoritma dan pemrograman.

Tugas utamamu:
- Membimbing mahasiswa untuk berpikir sendiri, BUKAN memberikan jawaban langsung
- Menggunakan pendekatan Socratic method dengan pertanyaan pemandu
- Menjelaskan konsep dengan analogi sederhana dan contoh konkret
- Membantu debugging dengan mengarahkan mahasiswa menemukan error sendiri
- Menggunakan bahasa santai namun profesional

Yang TIDAK boleh kamu lakukan:
- Memberikan kode lengkap untuk tugas/ujian
- Menyelesaikan tugas mahasiswa secara langsung
- Memberikan jawaban tanpa proses berpikir

Gaya komunikasi:
- Santai dan bersahabat
- Gunakan emoji sesekali untuk membuat percakapan lebih hidup
- Dorong mahasiswa dengan pujian ketika mereka berpikir dengan benar
- Sabar dan suportif"""

llm_manager = init_llm_manager()
rate_limiter = init_rate_limiter()
question_detector = init_question_detector()
code_analyzer = init_code_analyzer()
algorithm_simulator = init_algorithm_simulator()
system_prompt = load_system_prompt()

# Load chat history from localStorage (simulated via session state)
def load_chat_history():
    """Load chat history from browser localStorage"""
    # Use session state to persist during the session
    # In a real implementation, this could use JavaScript + localStorage
    pass

def save_chat_history():
    """Save chat history to a JSON file"""
    try:
        import json
        from datetime import datetime
        
        # Create a history directory if it doesn't exist
        history_dir = Path("chat_history")
        history_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = history_dir / f"chat_{timestamp}.json"
        
        # Save messages to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
        
        return filename
    except Exception as e:
        raise Exception(f"Error saving chat history: {str(e)}")

# Load history on startup
load_chat_history()

# ============================================
# SIDEBAR - Organized Structure
# ============================================

# 1. UPLOAD KODE
st.sidebar.markdown("### 📤 Upload Kode")
uploaded_file = st.sidebar.file_uploader(
    "Upload file Python (.py atau .txt)",
    type=["py", "txt"],
    help="Maksimal 1MB, format .py atau .txt"
)

# File validation and analysis
if uploaded_file is not None:
    file_size = len(uploaded_file.getbuffer())
    max_size = 1024 * 1024  # 1MB

    if file_size > max_size:
        st.sidebar.error(f"File terlalu besar! Maksimal 1MB. Ukuran file: {file_size/1024/1024:.2f}MB")
    else:
        st.sidebar.success(f"✅ File {uploaded_file.name} berhasil diupload! ({file_size/1024:.1f} KB)")

        # Save uploaded file
        file_path = Path("uploads") / uploaded_file.name
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Read and analyze code
            code_content = uploaded_file.getvalue().decode("utf-8")
            st.session_state.uploaded_code = code_content
            
            # Analyze code
            with st.spinner("🔍 Menganalisis kode..."):
                analysis = code_analyzer.analyze_code(code_content)
                st.session_state.code_analysis = analysis
            
            # Show analysis summary in sidebar
            if analysis["success"] and analysis["is_valid"]:
                st.sidebar.success("✓ Kode valid")
                
                if analysis["algorithms"]:
                    st.sidebar.info(f"🎯 Algoritma: {', '.join(analysis['algorithms'][:3])}")
                
                with st.sidebar.expander("📊 Detail Analisis"):
                    st.write("**Struktur:**")
                    if analysis["structure"]["functions"]:
                        st.write(f"- {len(analysis['structure']['functions'])} fungsi")
                    if analysis["structure"]["classes"]:
                        st.write(f"- {len(analysis['structure']['classes'])} class")
                    
                    st.write(f"\n**Kompleksitas:** {analysis['complexity_indicators']['estimated_time_complexity']}")
                    
                    if analysis["learning_points"]:
                        st.write("\n**Learning Points:**")
                        for point in analysis["learning_points"][:3]:
                            st.write(f"- {point}")
            else:
                st.sidebar.error("❌ Kode memiliki syntax error")
                if analysis.get("syntax_errors"):
                    for err in analysis["syntax_errors"][:2]:
                        st.sidebar.error(f"Line {err['line']}: {err['message']}")
            
            st.sidebar.info("💭 Tanyakan tentang kode ini dalam percakapan!")
            
        except Exception as e:
            st.sidebar.error(f"Error menyimpan file: {str(e)}")
elif st.session_state.uploaded_code:
    # Show that there's uploaded code in session
    st.sidebar.info("📄 Ada kode yang sudah diupload sebelumnya")
    if st.sidebar.button("🗑️ Hapus kode"):
        st.session_state.uploaded_code = None
        st.session_state.code_analysis = None
        st.rerun()

# 2. ALGORITHM SIMULATOR
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔬 Algorithm Simulator")

algorithm_choice = st.sidebar.selectbox(
    "Pilih Algoritma:",
    ["(Pilih algoritma)", "Bubble Sort", "Selection Sort", "Insertion Sort", 
     "Binary Search", "Linear Search", "Factorial", "Fibonacci"],
    key="algo_select"
)

if algorithm_choice != "(Pilih algoritma)":
    algorithm_map = {
        "Bubble Sort": "bubble_sort",
        "Selection Sort": "selection_sort",
        "Insertion Sort": "insertion_sort",
        "Binary Search": "binary_search",
        "Linear Search": "linear_search",
        "Factorial": "factorial",
        "Fibonacci": "fibonacci"
    }
    
    algo_key = algorithm_map[algorithm_choice]
    
    # Input based on algorithm type
    if algo_key.endswith("_sort"):
        data_input = st.sidebar.text_input(
            "Array (pisahkan dengan koma):",
            "64, 34, 25, 12, 22",
            key="sort_input"
        )
        
        if st.sidebar.button("🚀 Jalankan Simulasi", key="run_sort"):
            try:
                data = [int(x.strip()) for x in data_input.split(",")]
                result = algorithm_simulator.simulate(algo_key, data)
                
                if result["success"]:
                    # Store in session state for display in main area
                    st.session_state.simulation_result = result
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ {result.get('error', 'Simulasi gagal')}")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    
    elif algo_key.endswith("_search"):
        data_input = st.sidebar.text_input(
            "Array:",
            "1, 3, 5, 7, 9, 11, 13",
            key="search_array"
        )
        target = st.sidebar.number_input("Target:", value=7, key="search_target")
        
        if st.sidebar.button("🚀 Jalankan Simulasi", key="run_search"):
            try:
                data = [int(x.strip()) for x in data_input.split(",")]
                result = algorithm_simulator.simulate(algo_key, data, target=target)
                
                if result["success"]:
                    st.session_state.simulation_result = result
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ {result.get('error', 'Simulasi gagal')}")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    
    else:  # factorial or fibonacci
        n = st.sidebar.number_input("Input (n):", min_value=0, max_value=20, value=5, key="recursive_input")
        
        if st.sidebar.button("🚀 Jalankan Simulasi", key="run_recursive"):
            try:
                result = algorithm_simulator.simulate(algo_key, n)
                
                if result["success"]:
                    st.session_state.simulation_result = result
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ {result.get('error', 'Simulasi gagal')}")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")

# 3. PERCAKAPAN
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Percakapan")

# Show conversation stats
message_count = len(st.session_state.messages)
if message_count > 0:
    st.sidebar.caption(f"📊 {message_count} pesan dalam sesi ini")
    
    # Context info
    max_context = 10
    context_count = min(message_count, max_context)
    st.sidebar.caption(f"🧠 Mengingat {context_count} pesan terakhir")

# Clear conversation button
if st.sidebar.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.uploaded_code = None
    st.session_state.code_analysis = None
    st.sidebar.success("✅ Riwayat percakapan dihapus!")
    st.rerun()

# ============================================
# MAIN AREA
# ============================================

# Initialize simulation result in session state
if 'simulation_result' not in st.session_state:
    st.session_state.simulation_result = None

# Display Simulation Result (if exists)
if st.session_state.simulation_result:
    result = st.session_state.simulation_result
    
    st.markdown("---")
    st.subheader(f"🔬 Hasil Simulasi: {result['algorithm']}")
    
    # Result summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Result", str(result['result']))
    with col2:
        if 'found' in result:
            st.metric("🔍 Found", "✅ Yes" if result['found'] else "❌ No")
            if result['found']:
                st.metric("📍 Index", result['index'])
    with col3:
        if 'comparisons' in result:
            st.metric("🔢 Comparisons", result.get('comparisons', 'N/A'))
    
    st.info(f"**Summary:** {result['summary']}")
    
    # Complexity Analysis
    if 'complexity' in result:
        with st.expander("📈 Complexity Analysis"):
            complexity = result['complexity']
            st.write(f"**Time Complexity:** {complexity.get('time', 'N/A')}")
            st.write(f"**Space Complexity:** {complexity.get('space', 'N/A')}")
            if 'best_case' in complexity:
                st.write(f"**Best Case:** {complexity['best_case']}")
            if 'worst_case' in complexity:
                st.write(f"**Worst Case:** {complexity['worst_case']}")
    
    # Detailed Steps
    with st.expander("📝 Lihat Langkah-Langkah Detail", expanded=True):
        for step in result['steps']:
            step_num = step.get('step', 0)
            description = step.get('description', '')
            
            st.write(f"**Step {step_num}:** {description}")
            
            # Display array state (for sorting/searching)
            if 'array' in step:
                st.code(str(step['array']), language='python')
            
            # Display explanation
            if 'explanation' in step:
                st.caption(f"💡 {step['explanation']}")
            
            # Display stats
            stats = []
            if 'comparisons' in step:
                stats.append(f"Comparisons: {step['comparisons']}")
            if 'swaps' in step:
                stats.append(f"Swaps: {step['swaps']}")
            if stats:
                st.caption(" | ".join(stats))
            
            if step_num < len(result['steps']) - 1:
                st.markdown("---")
    
    # Visualization
    if 'visualization' in result and result['visualization']:
        with st.expander("🎨 Visualisasi"):
            st.text(result['visualization'])
    
    # Button to clear simulation
    if st.button("🗑️ Tutup Hasil Simulasi"):
        st.session_state.simulation_result = None
        st.rerun()
    
    st.markdown("---")

# Main chat interface
st.markdown("### 💭 Percakapan")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tanyakan tentang algoritma..."):
    # Check rate limit
    user_id = st.session_state.get("user_id", "anonymous")
    rate_check = rate_limiter.check_limit(user_id)
    
    if not rate_check["allowed"]:
        wait_time = int(rate_check["wait_time"])
        st.error(f"⚠️ {rate_check['reason']}. Silakan tunggu {wait_time} detik.")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if llm_manager is None:
            full_response = "⚠️ Maaf, sistem LLM belum tersedia. Pastikan API key sudah dikonfigurasi di halaman Admin."
            message_placeholder.markdown(full_response)
        else:
            try:
                # Show loading indicator
                message_placeholder.markdown("💭 Sedang berpikir...")
                
                # DETECT QUESTION TYPE
                has_uploaded_code = st.session_state.uploaded_code is not None
                detection = question_detector.detect(prompt, has_uploaded_code)
                response_strategy = question_detector.get_response_strategy(detection)
                
                # BUILD ENHANCED PROMPT
                enhanced_system_prompt = system_prompt
                
                # Add response strategy guidance
                enhanced_system_prompt += f"\n\n---\nSTRATEGI RESPONS:\n{response_strategy['guidance']}\n"
                
                # Add code analysis if available
                if st.session_state.code_analysis:
                    analysis = st.session_state.code_analysis
                    enhanced_system_prompt += f"\n\n---\nANALISIS KODE USER:\n"
                    enhanced_system_prompt += f"Kode: {st.session_state.uploaded_code[:500]}...\n"
                    enhanced_system_prompt += f"Valid: {analysis['is_valid']}\n"
                    enhanced_system_prompt += f"Algoritma: {', '.join(analysis.get('algorithms', []))}\n"
                    enhanced_system_prompt += f"Kompleksitas: {analysis['complexity_indicators'].get('estimated_time_complexity', 'N/A')}\n"
                    
                    if analysis.get('learning_points'):
                        enhanced_system_prompt += f"Learning Points:\n"
                        for point in analysis['learning_points'][:3]:
                            enhanced_system_prompt += f"- {point}\n"
                    
                    # Add guided questions
                    guided_q = code_analyzer.get_guided_questions(analysis)
                    if guided_q:
                        enhanced_system_prompt += f"\nPertanyaan Pemandu:\n"
                        for q in guided_q[:3]:
                            enhanced_system_prompt += f"- {q}\n"
                
                # HANDLE HOMEWORK REJECTION
                if response_strategy["should_reject"]:
                    full_response = """
🚫 **Maaf, saya tidak bisa membantu mengerjakan tugas atau ujian secara langsung.**

Ini adalah chatbot pembelajaran yang dirancang untuk **membimbing proses berpikir**, bukan memberikan jawaban siap pakai.

**Yang bisa saya lakukan:**
- Menjelaskan **konsep** yang mendasari tugas kamu
- Membantu kamu **memahami algoritma** yang relevan
- Memberikan **pertanyaan pemandu** untuk arahkan cara berpikir
- Diskusi tentang **pendekatan** yang bisa dicoba

**Coba tanyakan seperti ini:**
- "Jelaskan konsep [topik] yang dipakai dalam tugas ini"
- "Bagaimana cara kerja algoritma [nama algoritma]?"
- "Apa pendekatan yang bisa saya pakai untuk soal seperti ini?"

Mari belajar bersama! 🎓
"""
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.stop()
                
                # Get conversation history for context (last 10 messages for better context)
                conversation_history = []
                max_context_messages = 10  # Increased from 5 to 10 for better learning experience
                for msg in st.session_state.messages[-max_context_messages-1:-1]:  # Exclude current prompt
                    conversation_history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Generate response with enhanced prompt
                result = llm_manager.generate_response(
                    prompt=prompt,
                    system_prompt=enhanced_system_prompt,
                    temperature=0.7,
                    conversation_history=conversation_history
                )
                
                if result["error"]:
                    # Show user-friendly error message based on error type
                    error_msg = result['error_message']
                    if 'quota' in error_msg.lower() or 'insufficient_quota' in error_msg.lower():
                        full_response = "⚠️ **Quota API habis**\n\n"
                        full_response += "Model yang dipilih sudah mencapai batas quota. "
                        full_response += "Silakan:\n"
                        full_response += "- Coba lagi nanti\n"
                        full_response += "- Hubungi admin untuk mengatur ulang API key\n"
                        full_response += "- Atau admin bisa mengubah model di halaman Admin"
                    elif 'rate limit' in error_msg.lower():
                        full_response = "⚠️ **Rate limit tercapai**\n\n"
                        full_response += "Terlalu banyak request dalam waktu singkat. Tunggu beberapa saat dan coba lagi."
                    else:
                        full_response = f"⚠️ **Terjadi kesalahan**\n\n{error_msg}\n\n"
                        full_response += "Silakan coba lagi atau hubungi admin."
                else:
                    # Success - show response
                    full_response = result["response"]
                    
                    # Show provider info with fallback indicator
                    if result.get("used_fallback"):
                        provider_info = f"\n\n<sub>*⚠️ Primary model error, menggunakan fallback: {result.get('model', 'N/A')} ({result.get('provider', 'N/A')})*</sub>"
                    else:
                        provider_info = f"\n\n<sub>*Model: {result.get('model', 'N/A')} | Type: {detection['type'].value}*</sub>"
                    full_response += provider_info
                
                # Display with typing effect (simulated)
                words = full_response.split()
                displayed_text = ""
                for i, word in enumerate(words):
                    displayed_text += word + " "
                    if i % 3 == 0:  # Update every 3 words for smooth effect
                        message_placeholder.markdown(displayed_text + "▌")
                        time.sleep(0.05)
                
                message_placeholder.markdown(full_response)
            
            except Exception as e:
                full_response = f"⚠️ Terjadi kesalahan tidak terduga: {str(e)}"
                message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# File upload handling
if uploaded_file is not None:
    st.sidebar.success(f"File {uploaded_file.name} berhasil diupload!")

    # Save uploaded file
    file_path = Path("uploads") / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.info("File siap untuk didiskusikan dalam percakapan.")

# Save chat history to localStorage
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Simpan Riwayat", use_container_width=True):
        if len(st.session_state.messages) > 0:
            try:
                filename = save_chat_history()
                st.success(f"✅ Riwayat percakapan disimpan!\n\nFile: `{filename.name}`")
            except Exception as e:
                st.error(f"❌ Gagal menyimpan: {str(e)}")
        else:
            st.warning("⚠️ Tidak ada percakapan untuk disimpan!")

with col2:
    if st.button("🗑️ Hapus Riwayat", use_container_width=True):
        if len(st.session_state.messages) > 0:
            st.session_state.messages = []
            if "uploaded_code" in st.session_state:
                st.session_state.uploaded_code = None
            if "code_analysis" in st.session_state:
                st.session_state.code_analysis = None
            if "simulation_result" in st.session_state:
                st.session_state.simulation_result = None
            st.success("✅ Riwayat percakapan dihapus!")
            st.rerun()
        else:
            st.info("ℹ️ Riwayat sudah kosong!")

# Footer
st.markdown("---")
st.markdown("*Chatbot ini menggunakan AI untuk membantu pemahaman algoritma*")