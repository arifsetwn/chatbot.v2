import re
import os
from pathlib import Path

import streamlit as st
try:
    import streamlit_authenticator as stauth
except Exception:
    st.error("streamlit_authenticator is not installed. Install via `pip install streamlit-authenticator`")
    st.stop()
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv


st.set_page_config(
    page_title="Admin - Chatbot Algoritma",
    page_icon="⚙️",
    layout="wide",
)


def ensure_auth_config(path: Path):
    """
    Ensure the auth config file exists with default values.
    """
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        default_cfg = {
            "credentials": {
                "usernames": {
                    "admin": {
                        "email": "admin@ums.ac.id",
                        "name": "Administrator",
                        "password": "$2b$12$placeholderhash"
                    }
                }
            },
            "cookie": {"expiry_days": 30, "key": "chatbot_admin_session", "name": "chatbot_admin"},
            "preauthorized": {"emails": ["admin@ums.ac.id"]},
        }
        with open(path, "w") as f:
            yaml.dump(default_cfg, f)


# Load/create auth config
CONFIG = Path("config/auth_config.yaml")
ensure_auth_config(CONFIG)
with open(CONFIG) as f:
    cfg = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    cfg.get("credentials", {}),
    cfg.get("cookie", {}).get("name", "chatbot_admin"),
    cfg.get("cookie", {}).get("key", "chatbot_admin_session"),
    cfg.get("cookie", {}).get("expiry_days", 30),
)


def login_flow():
    """
    Handle login for streamlit-authenticator v0.4.2
    """
    try:
        # v0.4.2 API: call login() without parameters (uses session_state automatically)
        authenticator.login()
    except Exception as e:
        st.error(f"Authentication initialization failed: {e}")
        st.stop()


# Run login
login_flow()

# Check authentication status from session_state (v0.4.2 standard)
if st.session_state.get('authentication_status') is False:
    st.error("Username/password salah")
    st.stop()
elif st.session_state.get('authentication_status') is None:
    st.warning("Masukkan username dan password")
    st.stop()

# Load environment variables
load_dotenv()


def write_env(updates: dict):
    """
    Update .env file with new key-value pairs.
    """
    env = Path(".env")
    content = env.read_text() if env.exists() else ""
    for k, v in updates.items():
        pattern = rf"^{k}=.*$"
        if re.search(pattern, content, flags=re.MULTILINE):
            content = re.sub(pattern, f"{k}={v}", content, flags=re.MULTILINE)
        else:
            if content and not content.endswith("\n"):
                content += "\n"
            content += f"{k}={v}\n"
    env.write_text(content.strip() + "\n")


# Main UI
st.title("⚙️ Admin Panel - Chatbot Algoritma")
st.markdown(f"Selamat datang, *{st.session_state.get('name', 'Admin')}*!")

st.sidebar.title("📋 Menu Admin")
MENU = [
    "🏠 Dashboard",
    "🔑 API Management",
    "🤖 Model Selection",
    "⚡ Rate Limit",
    "📄 System Prompt",
    "📊 Analytics",
    "📚 Upload Materi",
]
choice = st.sidebar.selectbox("Pilih menu:", MENU)

if choice == "🏠 Dashboard":
    st.header("Dashboard Admin")
    current_model = os.getenv("DEFAULT_MODEL", "gemini")
    rpm = os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "10")
    rph = os.getenv("RATE_LIMIT_REQUESTS_PER_HOUR", "100")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Chat Hari Ini", "0")
    c2.metric("Rata-rata Response Time", "0s")
    c3.metric("Active Users", "0")
    c4.metric("Uptime", "99.9%")

    st.markdown("---")
    st.subheader("🔧 Status Sistem")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("**🤖 Model AI Aktif:**")
        st.success("Gemini" if current_model == "gemini" else "OpenAI" if current_model == "openai" else "Auto")
    with s2:
        st.markdown("**⚡ Rate Limiting:**")
        st.info(f"{rpm} req/min, {rph} req/hour")
    with s3:
        st.markdown("**📚 Materi:**")
        cnt = len(list(Path("data/materials").glob("*.pdf"))) if Path("data/materials").exists() else 0
        st.info(f"{cnt} file PDF")

    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    a1, a2, a3 = st.columns(3)
    if a1.button("🔄 Restart Services"):
        st.info("Restarting services... (placeholder)")
        st.success("Services restarted")
    if a2.button("🧹 Clear Cache"):
        st.info("Clearing cache... (placeholder)")
        st.success("Cache cleared")
    if a3.button("📊 Generate Report"):
        st.info("Generating report... (placeholder)")
        st.success("Report generated")

elif choice == "🔑 API Management":
    st.header("API Key Management")
    current_gemini = os.getenv("GOOGLE_API_KEY", "")
    current_openai = os.getenv("OPENAI_API_KEY", "")

    gemini = st.text_input("Gemini API Key", value=current_gemini, type="password")
    openai = st.text_input("OpenAI API Key", value=current_openai, type="password")

    col1, col2, col3 = st.columns(3)
    if col1.button("🧪 Test Gemini API"):
        st.info("Testing Gemini... (placeholder)")
        st.success("Gemini OK") if gemini else st.error("Masukkan Gemini API key terlebih dahulu")
    if col2.button("🧪 Test OpenAI API"):
        st.info("Testing OpenAI... (placeholder)")
        st.success("OpenAI OK") if openai else st.error("Masukkan OpenAI API key terlebih dahulu")
    if col3.button("💾 Simpan API Keys"):
        try:
            write_env({"GOOGLE_API_KEY": gemini, "OPENAI_API_KEY": openai})
            st.success("API keys disimpan ke .env")
            st.info("Restart aplikasi untuk menerapkan perubahan")
        except Exception as e:
            st.error(f"Error menyimpan API keys: {e}")

elif choice == "🤖 Model Selection":
    st.header("Model Selection")
    cur = os.getenv("DEFAULT_MODEL", "gemini")
    opts = ["gemini", "openai", "auto"]
    disp = {"gemini": "Google Gemini", "openai": "OpenAI GPT", "auto": "Auto (Fallback)"}
    sel = st.selectbox("Pilih model aktif:", opts, index=opts.index(cur))
    st.info(disp[sel])
    if st.button("✅ Terapkan Model"):
        write_env({"DEFAULT_MODEL": sel})
        st.success("Model disimpan. Restart aplikasi untuk menerapkan.")

elif choice == "⚡ Rate Limit":
    st.header("Rate Limit Configuration")
    cur_rpm = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "10"))
    cur_rph = int(os.getenv("RATE_LIMIT_REQUESTS_PER_HOUR", "100"))
    rpm = st.slider("Requests per menit", 1, 100, value=cur_rpm)
    rph = st.slider("Requests per jam", 1, 1000, value=cur_rph)
    if st.button("💾 Simpan Konfigurasi"):
        if rph >= rpm:
            write_env({"RATE_LIMIT_REQUESTS_PER_MINUTE": str(rpm), "RATE_LIMIT_REQUESTS_PER_HOUR": str(rph)})
            st.success("Rate limit disimpan")
        else:
            st.error("Requests per jam harus >= requests per menit")

elif choice == "📄 System Prompt":
    st.header("System Prompt Setting")
    pf = Path("data/system_prompt.txt")
    if not pf.exists():
        pf.parent.mkdir(parents=True, exist_ok=True)
        pf.write_text("Kamu adalah chatbot pembelajaran algoritma...\n")
    cur = pf.read_text()
    new = st.text_area("Edit System Prompt", value=cur, height=300)
    c1, c2 = st.columns(2)
    if c1.button("💾 Simpan Prompt"):
        pf.write_text(new)
        st.success("Prompt disimpan")
    if c2.button("🔄 Reset ke Default"):
        default = "Kamu adalah chatbot pembelajaran algoritma untuk mahasiswa pemula."
        pf.write_text(default)
        st.warning("Prompt direset ke default")

elif choice == "📊 Analytics":
    st.header("Analytics Dashboard")
    st.write("(Placeholder analytics — integrasikan log parsing & storage untuk data nyata.)")
    st.info("Tidak ada data saat ini")

elif choice == "📚 Upload Materi":
    st.header("Upload Materi Pembelajaran")
    materials_dir = Path("data/materials")
    materials_dir.mkdir(parents=True, exist_ok=True)
    existing_files = list(materials_dir.glob("*.pdf"))
    if existing_files:
        st.subheader("Materi yang ada")
        for p in existing_files:
            st.write(p.name)
            if st.button(f"Hapus {p.name}", key=f"del_{p.name}"):
                p.unlink()
                st.success(f"{p.name} dihapus")
                st.rerun()

    uploaded_material = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_material:
        file_size = len(uploaded_material.getbuffer())
        if file_size > 10 * 1024 * 1024:
            st.error("File terlalu besar (maksimal 10MB)")
        else:
            # Check if file already exists
            target_path = materials_dir / uploaded_material.name
            if target_path.exists():
                st.warning(f"⚠️ File {uploaded_material.name} sudah ada. Akan ditimpa.")

            # Save the file
            try:
                with open(target_path, "wb") as f:
                    f.write(uploaded_material.getbuffer())

                st.success(f"✅ File {uploaded_material.name} berhasil diupload!")
                st.info(f"📊 Ukuran file: {file_size/1024/1024:.2f} MB")
                st.info("📚 File tersimpan di folder data/materials/")

                # Show file info
                st.markdown("**Informasi File:**")
                st.json({
                    "nama_file": uploaded_material.name,
                    "ukuran": f"{file_size/1024/1024:.2f} MB",
                    "lokasi": str(target_path),
                    "tipe": uploaded_material.type
                })

            except Exception as e:
                st.error(f"❌ Error menyimpan file: {str(e)}")

    # Instructions
    with st.expander("ℹ️ Instruksi Upload Materi"):
        st.markdown("""
        **Panduan upload materi:**

        1. **Format**: Hanya file PDF yang diterima
        2. **Ukuran**: Maksimal 10MB per file
        3. **Penamaan**: Gunakan nama yang deskriptif
        4. **Isi**: Materi pembelajaran algoritma dan pemrograman

        **File akan disimpan di:** `data/materials/`
        """)

# Logout button - v0.4.2 renders the button automatically
st.sidebar.markdown("---")
authenticator.logout(button_name='Logout', location='sidebar', key='admin_logout')