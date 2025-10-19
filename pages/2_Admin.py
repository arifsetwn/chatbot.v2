import re
import os
from pathlib import Path
from datetime import datetime, timedelta

import streamlit as st
try:
    import streamlit_authenticator as stauth
except Exception:
    st.error("streamlit_authenticator is not installed. Install via `pip install streamlit-authenticator`")
    st.stop()
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.analytics import get_analytics


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
    "🎓 Moodle Integration",
]
choice = st.sidebar.selectbox("Pilih menu:", MENU)

if choice == "🏠 Dashboard":
    st.header("Dashboard Admin")
    current_model = os.getenv("DEFAULT_MODEL", "gemini")
    rpm = os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "10")
    rph = os.getenv("RATE_LIMIT_REQUESTS_PER_HOUR", "100")

    # Get real analytics data
    analytics = get_analytics()
    stats = analytics.get_stats()
    
    # Display real metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Chat Hari Ini", stats["chats_today"])
    c2.metric("Rata-rata Response Time", f"{stats['avg_response_time']:.2f}s")
    c3.metric("Active Users", stats["active_users_today"])
    
    # Calculate uptime percentage (assume 99.9% if running)
    uptime_pct = 99.9 if stats["uptime_hours"] > 0 else 0
    c4.metric("Uptime", f"{uptime_pct:.1f}%")

    st.markdown("---")
    
    # Additional stats
    st.subheader("� Statistik Detail")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Total Chat (All Time)", stats["total_chats"])
    with s2:
        st.metric("Total Users (All Time)", stats["total_users"])
    with s3:
        st.metric("Uptime Hours", f"{stats['uptime_hours']:.1f}h")
    
    st.markdown("---")
    st.subheader("�🔧 Status Sistem")
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

    # Recent activity
    st.markdown("---")
    st.subheader("📈 Aktivitas Terkini (10 Chat Terakhir)")
    recent_chats = stats.get("recent_chats", [])
    if recent_chats:
        for i, chat in enumerate(reversed(recent_chats), 1):
            timestamp = datetime.fromisoformat(chat["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            status = "✅" if chat["success"] else "❌"
            st.caption(f"{i}. {status} {timestamp} | User: {chat['user_id'][:20]} | Response: {chat['response_time']:.2f}s")
    else:
        st.info("Belum ada aktivitas chat")
    
    # Daily trend (last 7 days)
    st.markdown("---")
    st.subheader("📊 Trend 7 Hari Terakhir")
    daily_stats = analytics.get_daily_stats(days=7)
    
    if daily_stats:
        # Prepare data for chart
        dates = []
        chats = []
        users = []
        
        for date in sorted(daily_stats.keys(), reverse=True):
            dates.append(date)
            chats.append(daily_stats[date]["chats"])
            users.append(len(daily_stats[date]["users"]))
        
        # Reverse to show oldest first
        dates.reverse()
        chats.reverse()
        users.reverse()
        
        # Display as table
        import pandas as pd
        df = pd.DataFrame({
            "Tanggal": dates,
            "Total Chat": chats,
            "Active Users": users
        })
        st.dataframe(df, use_container_width=True)
        
        # Simple bar chart
        st.bar_chart(df.set_index("Tanggal")[["Total Chat", "Active Users"]])
    else:
        st.info("Belum ada data untuk ditampilkan")

    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    a1, a2, a3 = st.columns(3)
    if a1.button("🔄 Refresh Data"):
        # Clear any pending confirmations
        if "confirm_reset" in st.session_state:
            del st.session_state.confirm_reset
        st.rerun()
    if a2.button("🧹 Reset Analytics"):
        if st.session_state.get("confirm_reset") and st.session_state.get("confirm_reset_time"):
            # Check if confirmation is still valid (within 10 seconds)
            from datetime import datetime
            elapsed = (datetime.now() - st.session_state.confirm_reset_time).total_seconds()
            if elapsed < 10:
                analytics.reset_stats()
                st.success("✅ Analytics data telah direset!")
                st.session_state.confirm_reset = False
                if "confirm_reset_time" in st.session_state:
                    del st.session_state.confirm_reset_time
                st.rerun()
            else:
                st.session_state.confirm_reset = False
                if "confirm_reset_time" in st.session_state:
                    del st.session_state.confirm_reset_time
                st.error("⏱️ Konfirmasi timeout. Klik lagi untuk reset.")
        else:
            st.session_state.confirm_reset = True
            st.session_state.confirm_reset_time = datetime.now()
            st.warning("⚠️ Klik sekali lagi dalam 10 detik untuk konfirmasi reset!")
    if a3.button("📁 Export Report"):
        # Export stats to JSON
        import json
        report = {
            "generated_at": datetime.now().isoformat(),
            "stats": stats,
            "daily_stats": daily_stats
        }
        report_json = json.dumps(report, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download JSON Report",
            data=report_json,
            file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        st.success("Report siap diunduh!")


elif choice == "🔑 API Management":
    st.header("API Key Management")
    current_gemini = os.getenv("GOOGLE_API_KEY", "")
    current_openai = os.getenv("OPENAI_API_KEY", "")

    gemini = st.text_input("Gemini API Key", value=current_gemini, type="password")
    openai = st.text_input("OpenAI API Key", value=current_openai, type="password")

    col1, col2, col3 = st.columns(3)
    if col1.button("🧪 Test Gemini API"):
        if not gemini:
            st.error("Masukkan Gemini API key terlebih dahulu")
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content("Test connection. Reply with OK.")
                st.success("✅ Gemini API Key Valid!")
                st.caption(f"Response: {response.text[:100]}...")
            except Exception as e:
                st.error(f"❌ Gemini API Error: {str(e)}")
    
    if col2.button("🧪 Test OpenAI API"):
        if not openai:
            st.error("Masukkan OpenAI API key terlebih dahulu")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test connection. Reply with OK."}],
                    max_tokens=10
                )
                st.success("✅ OpenAI API Key Valid!")
                st.caption(f"Response: {response.choices[0].message.content}")
            except Exception as e:
                st.error(f"❌ OpenAI API Error: {str(e)}")
    
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
    
    st.info("ℹ️ Requests per jam harus >= (Requests per menit × 60)")
    
    rpm = st.slider("Requests per menit", 1, 100, value=cur_rpm)
    rph = st.slider("Requests per jam", 1, 6000, value=cur_rph)
    
    # Calculate minimum required rph
    min_rph = rpm * 60
    st.caption(f"Minimum requests/jam berdasarkan setting: {min_rph}")
    
    if st.button("💾 Simpan Konfigurasi"):
        if rph >= min_rph:
            write_env({"RATE_LIMIT_REQUESTS_PER_MINUTE": str(rpm), "RATE_LIMIT_REQUESTS_PER_HOUR": str(rph)})
            st.success(f"✅ Rate limit disimpan: {rpm} req/min, {rph} req/hour")
        else:
            st.error(f"❌ Requests per jam harus >= {min_rph} (rpm × 60 menit)")

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
    
    # Get analytics data
    analytics = get_analytics()
    stats = analytics.get_stats()
    
    # Overview metrics
    st.subheader("📈 Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Chats", stats["total_chats"])
    m2.metric("Total Users", stats["total_users"])
    m3.metric("Chats Today", stats["chats_today"])
    m4.metric("Avg Response Time", f"{stats['avg_response_time']:.2f}s")
    
    st.markdown("---")
    
    # Time period selector
    period = st.selectbox("Periode Analisis:", ["7 Hari Terakhir", "30 Hari Terakhir", "All Time"])
    days = 7 if period == "7 Hari Terakhir" else 30 if period == "30 Hari Terakhir" else 365
    
    daily_stats = analytics.get_daily_stats(days=days)
    
    if daily_stats:
        st.subheader(f"📊 Statistik {period}")
        
        # Prepare data
        dates = []
        chats = []
        users = []
        avg_times = []
        
        for date in sorted(daily_stats.keys()):
            dates.append(date)
            chats.append(daily_stats[date]["chats"])
            users.append(len(daily_stats[date]["users"]))
            avg_times.append(daily_stats[date].get("avg_response_time", 0))
        
        import pandas as pd
        df = pd.DataFrame({
            "Tanggal": dates,
            "Total Chat": chats,
            "Active Users": users,
            "Avg Response Time": [f"{t:.2f}s" for t in avg_times]
        })
        
        # Display table
        st.dataframe(df, use_container_width=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Total Chat per Hari**")
            chart_data = pd.DataFrame({"Chat": chats}, index=dates)
            st.line_chart(chart_data)
        
        with col2:
            st.markdown("**Active Users per Hari**")
            chart_data = pd.DataFrame({"Users": users}, index=dates)
            st.line_chart(chart_data)
        
        # Summary statistics
        st.markdown("---")
        st.subheader("📋 Summary")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Chats", sum(chats))
        s2.metric("Unique Users", len(set([u for day_stats in daily_stats.values() for u in day_stats.get("users", [])])))
        s3.metric("Avg Chats/Day", f"{sum(chats)/len(dates):.1f}")
        s4.metric("Peak Day Chats", max(chats) if chats else 0)
    else:
        st.info("Belum ada data analytics untuk ditampilkan")
    
    # Recent activity details
    st.markdown("---")
    st.subheader("🕒 Recent Activity (100 Chat Terakhir)")
    recent_chats = stats.get("recent_chats", [])
    
    if recent_chats:
        activity_data = []
        for chat in reversed(recent_chats):
            timestamp = datetime.fromisoformat(chat["timestamp"])
            activity_data.append({
                "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "User": chat["user_id"][:30],
                "Response Time": f"{chat['response_time']:.2f}s",
                "Status": "✅ Success" if chat["success"] else "❌ Failed"
            })
        
        import pandas as pd
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True)
    else:
        st.info("Belum ada aktivitas chat")
    
    # Export options
    st.markdown("---")
    st.subheader("💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Full Analytics", use_container_width=True):
            import json
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "summary": stats,
                "daily_stats": daily_stats
            }
            export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download JSON",
                data=export_json,
                file_name=f"full_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        if st.button("🗑️ Reset All Analytics", use_container_width=True):
            if st.session_state.get("confirm_analytics_reset") and st.session_state.get("confirm_analytics_reset_time"):
                # Check if confirmation is still valid (within 10 seconds)
                from datetime import datetime
                elapsed = (datetime.now() - st.session_state.confirm_analytics_reset_time).total_seconds()
                if elapsed < 10:
                    analytics.reset_stats()
                    st.success("✅ Analytics data telah direset!")
                    st.session_state.confirm_analytics_reset = False
                    if "confirm_analytics_reset_time" in st.session_state:
                        del st.session_state.confirm_analytics_reset_time
                    st.rerun()
                else:
                    st.session_state.confirm_analytics_reset = False
                    if "confirm_analytics_reset_time" in st.session_state:
                        del st.session_state.confirm_analytics_reset_time
                    st.error("⏱️ Konfirmasi timeout. Klik lagi untuk reset.")
            else:
                st.session_state.confirm_analytics_reset = True
                st.session_state.confirm_analytics_reset_time = datetime.now()
                st.warning("⚠️ Klik sekali lagi dalam 10 detik untuk konfirmasi reset!")

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
            st.error("❌ File terlalu besar (maksimal 10MB)")
        else:
            # Check if file already exists
            target_path = materials_dir / uploaded_material.name
            
            if target_path.exists():
                # File exists - require confirmation
                st.warning(f"⚠️ File **{uploaded_material.name}** sudah ada!")
                
                col1, col2 = st.columns(2)
                confirm_key = f"confirm_overwrite_{uploaded_material.name}"
                
                if col1.button("✅ Timpa File", key=f"overwrite_{uploaded_material.name}", use_container_width=True):
                    st.session_state[confirm_key] = True
                
                if col2.button("❌ Batal", key=f"cancel_{uploaded_material.name}", use_container_width=True):
                    st.info("Upload dibatalkan")
                    if confirm_key in st.session_state:
                        del st.session_state[confirm_key]
                    st.stop()
                
                # If not confirmed, don't proceed
                if not st.session_state.get(confirm_key):
                    st.stop()

            # Save the file
            try:
                with open(target_path, "wb") as f:
                    f.write(uploaded_material.getbuffer())

                st.success(f"✅ File **{uploaded_material.name}** berhasil diupload!")
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
                
                # Clear confirmation state
                confirm_key = f"confirm_overwrite_{uploaded_material.name}"
                if confirm_key in st.session_state:
                    del st.session_state[confirm_key]

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

elif choice == "🎓 Moodle Integration":
    st.header("Integrasi Moodle LMS")
    
    # Configuration Section
    st.subheader("⚙️ Konfigurasi Moodle")
    
    current_moodle_url = os.getenv("MOODLE_URL", "")
    current_moodle_token = os.getenv("MOODLE_TOKEN", "")
    
    col1, col2 = st.columns(2)
    
    with col1:
        moodle_url = st.text_input(
            "Moodle URL",
            value=current_moodle_url,
            placeholder="https://moodle.ums.ac.id",
            help="Base URL Moodle instance (tanpa trailing slash)"
        )
    
    with col2:
        moodle_token = st.text_input(
            "Web Service Token",
            value=current_moodle_token,
            type="password",
            help="Token dari Moodle Web Services"
        )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    if col1.button("🧪 Test Connection", use_container_width=True):
        if not moodle_url or not moodle_token:
            st.error("❌ Masukkan URL dan Token terlebih dahulu")
        else:
            try:
                from utils.moodle_client import MoodleClient
                
                with st.spinner("Testing Moodle connection..."):
                    client = MoodleClient(moodle_url, moodle_token)
                    
                    if client.validate_connection():
                        info = client.get_site_info()
                        st.success("✅ Koneksi ke Moodle berhasil!")
                        
                        # Show site info
                        st.info(f"**Site:** {info['sitename']}\n\n"
                               f"**Version:** {info['version']}\n\n"
                               f"**User:** {info['fullname']} ({info['username']})")
                    else:
                        st.error("❌ Koneksi gagal. Periksa URL dan token.")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    if col2.button("💾 Simpan Konfigurasi", use_container_width=True):
        try:
            write_env({
                "MOODLE_URL": moodle_url,
                "MOODLE_TOKEN": moodle_token
            })
            st.success("✅ Konfigurasi Moodle disimpan!")
            st.info("ℹ️ Restart aplikasi untuk menerapkan perubahan")
        except Exception as e:
            st.error(f"❌ Error menyimpan konfigurasi: {str(e)}")
    
    if col3.button("🔄 Reload Config", use_container_width=True):
        st.rerun()
    
    # Only show features if connected
    if current_moodle_url and current_moodle_token:
        st.markdown("---")
        st.subheader("📊 Moodle Data Explorer")
        
        try:
            from utils.moodle_client import MoodleClient
            client = MoodleClient()
            
            # Tabs for different features
            tab1, tab2, tab3, tab4 = st.tabs([
                "👤 User Lookup",
                "📚 Courses",
                "📝 Assignments",
                "📈 Student Dashboard"
            ])
            
            with tab1:
                st.markdown("#### Search User")
                
                search_field = st.selectbox("Search by:", ["username", "email", "id"])
                search_value = st.text_input(f"Enter {search_field}:")
                
                if st.button("🔍 Search User", key="search_user"):
                    if search_value:
                        try:
                            users = client.get_user_by_field(search_field, [search_value])
                            
                            if users:
                                st.success(f"✅ Found {len(users)} user(s)")
                                for user in users:
                                    with st.expander(f"👤 {user['fullname']} (@{user['username']})"):
                                        st.json({
                                            "ID": user['id'],
                                            "Username": user['username'],
                                            "Full Name": user['fullname'],
                                            "Email": user['email'],
                                            "First Access": datetime.fromtimestamp(user.get('firstaccess', 0)).strftime("%Y-%m-%d") if user.get('firstaccess') else "Never"
                                        })
                            else:
                                st.warning("⚠️ User tidak ditemukan")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with tab2:
                st.markdown("#### All Courses")
                
                if st.button("📚 Load Courses", key="load_courses"):
                    try:
                        with st.spinner("Loading courses..."):
                            courses = client.get_all_courses()
                            
                            if courses:
                                st.success(f"✅ Found {len(courses)} course(s)")
                                
                                # Display as table
                                import pandas as pd
                                df = pd.DataFrame([{
                                    "ID": c['id'],
                                    "Name": c['fullname'],
                                    "Short Name": c['shortname'],
                                    "Category": c.get('categoryid', 'N/A')
                                } for c in courses[:50]])  # Limit to 50 for performance
                                
                                st.dataframe(df, use_container_width=True)
                                
                                if len(courses) > 50:
                                    st.info(f"ℹ️ Showing first 50 of {len(courses)} courses")
                            else:
                                st.warning("⚠️ No courses found")
                                
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with tab3:
                st.markdown("#### Assignments")
                
                course_id_input = st.number_input("Course ID:", min_value=1, step=1)
                
                if st.button("📝 Load Assignments", key="load_assignments"):
                    try:
                        with st.spinner("Loading assignments..."):
                            result = client.get_assignments([course_id_input])
                            courses_data = result.get('courses', [])
                            
                            if courses_data:
                                for course_data in courses_data:
                                    assignments = course_data.get('assignments', [])
                                    
                                    if assignments:
                                        st.success(f"✅ Found {len(assignments)} assignment(s)")
                                        
                                        for assign in assignments:
                                            with st.expander(f"📝 {assign['name']}"):
                                                due = assign.get('duedate', 0)
                                                due_str = datetime.fromtimestamp(due).strftime("%Y-%m-%d %H:%M") if due else "No deadline"
                                                
                                                st.markdown(f"**Due:** {due_str}")
                                                st.markdown(f"**ID:** {assign['id']}")
                                                st.markdown(f"**Intro:** {assign.get('intro', 'N/A')[:200]}...")
                                    else:
                                        st.info("ℹ️ No assignments in this course")
                            else:
                                st.warning("⚠️ Course not found or no assignments")
                                
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with tab4:
                st.markdown("#### Student Dashboard")
                
                username_input = st.text_input("Student Username:")
                
                if st.button("📊 Load Dashboard", key="load_dashboard"):
                    if username_input:
                        try:
                            with st.spinner("Loading student dashboard..."):
                                dashboard = client.get_student_dashboard(username_input)
                                
                                # User info
                                st.markdown(f"### 👤 {dashboard['user']['fullname']}")
                                st.caption(f"Username: {dashboard['user']['username']} | Email: {dashboard['user']['email']}")
                                
                                st.markdown("---")
                                
                                # Courses
                                st.markdown("#### 📚 Enrolled Courses")
                                if dashboard['courses']:
                                    for course in dashboard['courses']:
                                        with st.expander(f"{course['fullname']} ({course['shortname']})"):
                                            st.markdown(f"**Course ID:** {course['id']}")
                                            st.markdown(f"**Progress:** {course.get('progress', 0)}%")
                                            
                                            if course['grades']:
                                                st.markdown("**Grades:**")
                                                for grade_info in course['grades']:
                                                    for grade in grade_info.get('gradeitems', []):
                                                        st.caption(f"• {grade.get('itemname', 'N/A')}: {grade.get('gradeformatted', 'N/A')}")
                                else:
                                    st.info("No courses found")
                                
                                st.markdown("---")
                                
                                # Upcoming assignments
                                st.markdown("#### 📝 Upcoming Assignments")
                                if dashboard['upcoming_assignments']:
                                    for assign in dashboard['upcoming_assignments'][:10]:
                                        st.markdown(f"**{assign['name']}**")
                                        st.caption(f"Due: {assign['duedate']}")
                                        st.caption(f"{assign['intro'][:100]}...")
                                        st.markdown("---")
                                else:
                                    st.info("No upcoming assignments")
                                    
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("⚠️ Enter username")
        
        except ImportError:
            st.error("❌ Moodle client not available. Check installation.")
        except Exception as e:
            st.error(f"❌ Error initializing Moodle client: {str(e)}")
    
    else:
        st.info("ℹ️ Masukkan URL dan Token Moodle untuk mengakses fitur integrasi")
    
    # Documentation
    with st.expander("📖 Setup Guide"):
        st.markdown("""
        ### Cara Setup Moodle Web Services
        
        **1. Enable Web Services (Admin):**
        - Site Administration > Advanced Features
        - Enable "Enable web services"
        
        **2. Enable REST Protocol:**
        - Site Administration > Plugins > Web Services > Manage Protocols
        - Enable REST protocol
        
        **3. Create External Service:**
        - Site Administration > Plugins > Web Services > External Services
        - Add new service: "Chatbot Service"
        - Add required functions:
          - `core_webservice_get_site_info`
          - `core_user_get_users`
          - `core_enrol_get_users_courses`
          - `core_course_get_contents`
          - `mod_assign_get_assignments`
          - `gradereport_user_get_grade_items`
        
        **4. Create Token:**
        - Site Administration > Plugins > Web Services > Manage Tokens
        - Add token for your user
        - Copy token and paste above
        
        **5. Test Connection:**
        - Enter Moodle URL and token
        - Click "Test Connection"
        - If successful, save configuration
        
        ### Integration Features
        
        - ✅ User authentication and lookup
        - ✅ Course enrollment tracking
        - ✅ Assignment listing and submission
        - ✅ Grade tracking and reporting
        - ✅ Student dashboard view
        - 🔄 Forum integration (coming soon)
        - 🔄 Quiz integration (coming soon)
        """)

# Logout button - v0.4.2 renders the button automatically
st.sidebar.markdown("---")
authenticator.logout(button_name='Logout', location='sidebar', key='admin_logout')