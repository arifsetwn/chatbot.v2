"""
Theme Manager for Dark/Light Mode Switching
Provides theme colors and CSS for Streamlit app
"""

import streamlit as st


class ThemeManager:
    """Manage dark/light theme switching"""
    
    @staticmethod
    def initialize():
        """Initialize theme in session state"""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'  # Default theme
    
    @staticmethod
    def toggle_theme():
        """Toggle between dark and light theme"""
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'
    
    @staticmethod
    def get_theme():
        """Get current theme"""
        ThemeManager.initialize()
        return st.session_state.theme
    
    @staticmethod
    def is_dark():
        """Check if current theme is dark"""
        return ThemeManager.get_theme() == 'dark'
    
    @staticmethod
    def get_theme_colors():
        """Get color palette based on current theme"""
        theme = ThemeManager.get_theme()
        
        if theme == 'dark':
            return {
                'background': '#0e1117',
                'secondary_bg': '#262730',
                'card_bg': '#1e1e1e',
                'text': '#fafafa',
                'text_secondary': '#b0b0b0',
                'border': '#3a3a3a',
                'accent': '#ff4b4b',
                'accent_secondary': '#0068c9',
                'success': '#21c354',
                'warning': '#ffa500',
                'error': '#ff4b4b',
                'code_bg': '#1e1e1e',
                'hover': '#3a3a3a',
                'disclaimer_bg': '#2d2d2d',
                'disclaimer_border': '#ff9800',
                'shadow': 'rgba(0, 0, 0, 0.5)',
            }
        else:  # light theme
            return {
                'background': '#ffffff',
                'secondary_bg': '#f0f2f6',
                'card_bg': '#ffffff',
                'text': '#262730',
                'text_secondary': '#6c757d',
                'border': '#e0e0e0',
                'accent': '#ff4b4b',
                'accent_secondary': '#1f77b4',
                'success': '#21c354',
                'warning': '#ffa500',
                'error': '#ff4b4b',
                'code_bg': '#f5f5f5',
                'hover': '#e8e8e8',
                'disclaimer_bg': '#fff9e6',
                'disclaimer_border': '#ff9800',
                'shadow': 'rgba(0, 0, 0, 0.1)',
            }
    
    @staticmethod
    def get_css():
        """Get CSS based on current theme"""
        colors = ThemeManager.get_theme_colors()
        
        return f"""
        <style>
            /* Main app background */
            .stApp {{
                background-color: {colors['background']};
                color: {colors['text']};
            }}
            
            /* App Header - Top bar with navigation */
            header[data-testid="stHeader"] {{
                background-color: {colors['secondary_bg']} !important;
                border-bottom: 1px solid {colors['border']};
            }}
            
            /* App Header - Navigation links text */
            header[data-testid="stHeader"] a {{
                color: {colors['text']} !important;
            }}
            
            header[data-testid="stHeader"] svg {{
                fill: {colors['text']} !important;
            }}
            
            /* Bottom container */
            .stBottom {{
                background-color: {colors['background']} !important;
            }}
            
            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {colors['secondary_bg']};
            }}
            
            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] label {{
                color: {colors['text']} !important;
            }}
            
            /* Sidebar Navigation */
            [data-testid="stSidebarNav"] {{
                background-color: {colors['secondary_bg']} !important;
            }}
            
            [data-testid="stSidebarNav"] a {{
                color: {colors['text']} !important;
            }}
            
            [data-testid="stSidebarNav"] a:hover {{
                background-color: {colors['hover']} !important;
            }}
            
            [data-testid="stSidebarNav"] svg {{
                fill: {colors['text']} !important;
            }}
            
            /* Sidebar navigation - text links (App, Chat, Admin) */
            [data-testid="stSidebarNav"] span {{
                color: {colors['text']} !important;
            }}
            
            /* Sidebar navigation - ALL text elements */
            [data-testid="stSidebarNav"] * {{
                color: {colors['text']} !important;
            }}
            
            /* Sidebar navigation items - force text color */
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a {{
                color: {colors['text']} !important;
            }}
            
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a span {{
                color: {colors['text']} !important;
            }}
            
            /* Fix emotion cache classes - Navigation menu text */
            .st-emotion-cache-ysg2um {{
                color: {colors['text']} !important;
            }}
            
            .st-emotion-cache-hzygls {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Base input styling */
            .base-input {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
                border-color: {colors['border']} !important;
            }}
            
            /* All emotion cache input elements */
            [class*="st-emotion-cache"] input {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
                border-color: {colors['border']} !important;
            }}
            
            [class*="st-emotion-cache"] textarea {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
                border-color: {colors['border']} !important;
            }}
            
            /* All emotion cache text elements */
            [class*="st-emotion-cache"] {{
                color: {colors['text']};
            }}
            
            /* Fix any white text in light mode */
            [class*="st-emotion-cache"] span,
            [class*="st-emotion-cache"] p,
            [class*="st-emotion-cache"] div,
            [class*="st-emotion-cache"] label {{
                color: {colors['text']} !important;
            }}
            
            /* Navigation menu items specific fix */
            nav[aria-label="Main menu"] a {{
                color: {colors['text']} !important;
            }}
            
            nav[aria-label="Main menu"] span {{
                color: {colors['text']} !important;
            }}
            
            /* Header */
            h1, h2, h3, h4, h5, h6 {{
                color: {colors['text']} !important;
            }}
            
            /* Text */
            p, span, div {{
                color: {colors['text']};
            }}
            
            /* Disclaimer box */
            .disclaimer-box {{
                background-color: {colors['disclaimer_bg']};
                border: 2px solid {colors['disclaimer_border']};
                border-radius: 10px;
                padding: 1.2rem;
                margin: 1.5rem 0;
                box-shadow: 0 2px 8px {colors['shadow']};
                color: #000000 !important;
            }}
            
            .disclaimer-box h4 {{
                color: {colors['warning']} !important;
                margin-bottom: 0.8rem;
            }}
            
            .disclaimer-box div {{
                color: #000000 !important;
            }}
            
            .disclaimer-box strong {{
                color: #000000 !important;
            }}
            
            /* Chat messages */
            .stChatMessage {{
                background-color: {colors['card_bg']} !important;
                border: 1px solid {colors['border']};
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 4px {colors['shadow']};
            }}
            
            .stChatMessage p {{
                color: {colors['text']} !important;
            }}
            
            /* Chat input */
            .stChatInput > div {{
                background-color: {colors['secondary_bg']} !important;
                border-color: {colors['border']} !important;
            }}
            
            .stChatInput input {{
                color: {colors['text']} !important;
                background-color: {colors['secondary_bg']} !important;
            }}
            
            /* Buttons */
            .stButton > button {{
                background-color: {colors['secondary_bg']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background-color: {colors['hover']};
                transform: translateY(-2px);
                box-shadow: 0 4px 8px {colors['shadow']};
            }}
            
            /* Primary button */
            .stButton > button[kind="primary"] {{
                background-color: {colors['accent_secondary']};
                color: white;
                border: none;
            }}
            
            .stButton > button[kind="primary"]:hover {{
                background-color: {colors['accent']};
            }}
            
            /* Text input */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
                border-color: {colors['border']} !important;
            }}
            
            .stTextInput label,
            .stTextArea label {{
                color: {colors['text']} !important;
            }}
            
            /* Force text input placeholder color */
            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {{
                color: {colors['text_secondary']} !important;
            }}
            
            /* Input wrapper */
            [data-baseweb="input"] {{
                background-color: {colors['secondary_bg']} !important;
            }}
            
            [data-baseweb="input"] input {{
                color: {colors['text']} !important;
            }}
            
            [data-baseweb="textarea"] {{
                background-color: {colors['secondary_bg']} !important;
            }}
            
            [data-baseweb="textarea"] textarea {{
                color: {colors['text']} !important;
            }}
            
            /* File uploader - Complete styling */
            [data-testid="stFileUploader"] {{
                background-color: {colors['secondary_bg']} !important;
                border: 2px dashed {colors['border']} !important;
                border-radius: 10px;
                padding: 1rem;
            }}
            
            [data-testid="stFileUploader"] section {{
                background-color: {colors['secondary_bg']} !important;
                border-color: {colors['border']} !important;
            }}
            
            [data-testid="stFileUploader"] label {{
                color: {colors['text']} !important;
            }}
            
            [data-testid="stFileUploader"] button {{
                background-color: {colors['card_bg']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['border']} !important;
            }}
            
            [data-testid="stFileUploader"] small {{
                color: {colors['text_secondary']} !important;
            }}
            
            /* File uploader - Drop zone */
            .stFileUploader {{
                background-color: {colors['secondary_bg']} !important;
                border: 2px dashed {colors['border']} !important;
                border-radius: 10px;
            }}
            
            .stFileUploader label {{
                color: {colors['text']} !important;
            }}
            
            .stFileUploader [data-testid="stMarkdownContainer"] {{
                color: {colors['text']} !important;
            }}
            
            /* Code blocks */
            pre, code {{
                background-color: {colors['code_bg']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['border']};
                border-radius: 5px;
            }}
            
            /* Expander */
            .streamlit-expanderHeader {{
                background-color: {colors['secondary_bg']};
                color: {colors['text']} !important;
                border-radius: 5px;
                border: 1px solid {colors['border']};
            }}
            
            .streamlit-expanderHeader:hover {{
                background-color: {colors['hover']};
            }}
            
            /* Metrics */
            [data-testid="stMetricValue"] {{
                color: {colors['text']} !important;
            }}
            
            [data-testid="stMetricLabel"] {{
                color: {colors['text_secondary']} !important;
            }}
            
            /* Dataframe */
            .stDataFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                border-radius: 5px;
            }}
            
            /* Success/Warning/Error boxes */
            .stSuccess, .stWarning, .stError, .stInfo {{
                background-color: {colors['card_bg']};
                border-radius: 8px;
                border-left: 4px solid;
            }}
            
            .stSuccess {{
                border-left-color: {colors['success']};
            }}
            
            .stWarning {{
                border-left-color: {colors['warning']};
            }}
            
            .stError {{
                border-left-color: {colors['error']};
            }}
            
            .stInfo {{
                border-left-color: {colors['accent_secondary']};
            }}
            
            /* Select box */
            .stSelectbox > div > div {{
                background-color: {colors['secondary_bg']};
                color: {colors['text']};
                border-color: {colors['border']};
            }}
            
            .stSelectbox label {{
                color: {colors['text']} !important;
            }}
            
            /* Slider */
            .stSlider > div > div > div {{
                background-color: {colors['secondary_bg']};
            }}
            
            .stSlider label {{
                color: {colors['text']} !important;
            }}
            
            /* Radio buttons */
            .stRadio > label {{
                color: {colors['text']} !important;
            }}
            
            /* Checkbox */
            .stCheckbox > label {{
                color: {colors['text']} !important;
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: {colors['secondary_bg']};
                border-radius: 5px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                color: {colors['text']};
            }}
            
            .stTabs [aria-selected="true"] {{
                background-color: {colors['accent_secondary']};
                color: white;
            }}
            
            /* Number input */
            .stNumberInput > div > div > input {{
                background-color: {colors['secondary_bg']};
                color: {colors['text']};
                border-color: {colors['border']};
            }}
            
            .stNumberInput label {{
                color: {colors['text']} !important;
            }}
            
            /* Download button */
            .stDownloadButton > button {{
                background-color: {colors['accent_secondary']};
                color: white;
                border: none;
            }}
            
            .stDownloadButton > button:hover {{
                background-color: {colors['accent']};
            }}
            
            /* Markdown containers */
            [data-testid="stMarkdownContainer"] {{
                color: {colors['text']} !important;
            }}
            
            /* Theme toggle button in sidebar - Special styling */
            .theme-toggle-sidebar {{
                width: 100%;
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid {colors['border']};
            }}
            
            .theme-toggle-sidebar button {{
                width: 100%;
                background: linear-gradient(135deg, {colors['accent_secondary']}, {colors['accent']});
                color: white !important;
                border: none !important;
                border-radius: 25px;
                padding: 0.8rem 1.2rem;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 15px {colors['shadow']};
                transition: all 0.3s ease;
            }}
            
            .theme-toggle-sidebar button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px {colors['shadow']};
            }}
            
            /* Animation for theme transition */
            * {{
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
            }}
            
            /* Global override for all Streamlit emotion-cache components */
            [class^="st-emotion-cache-"],
            [class*=" st-emotion-cache-"] {{
                color: {colors['text']} !important;
            }}
            
            /* Ensure all nested text elements follow theme */
            [class^="st-emotion-cache-"] span,
            [class*=" st-emotion-cache-"] span,
            [class^="st-emotion-cache-"] p,
            [class*=" st-emotion-cache-"] p,
            [class^="st-emotion-cache-"] div,
            [class*=" st-emotion-cache-"] div,
            [class^="st-emotion-cache-"] label,
            [class*=" st-emotion-cache-"] label,
            [class^="st-emotion-cache-"] a,
            [class*=" st-emotion-cache-"] a {{
                color: {colors['text']} !important;
            }}
            
            /* Force background for emotion cache containers */
            [class^="st-emotion-cache-"][class*="container"],
            [class*=" st-emotion-cache-"][class*="container"] {{
                background-color: {colors['secondary_bg']} !important;
            }}
            
            /* Specific fix for e4man113 class */
            .e4man113,
            [class*="e4man113"] {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Scrollbar */
            ::-webkit-scrollbar {{
                width: 10px;
                height: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: {colors['secondary_bg']};
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {colors['border']};
                border-radius: 5px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: {colors['hover']};
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .theme-toggle-sidebar button {{
                    padding: 0.6rem 1rem;
                    font-size: 0.9rem;
                }}
            }}
            
            /* ==============================================
               CRITICAL OVERRIDES - Prevent white text in light mode
               ============================================== */
            
            /* Force all text elements to follow theme color */
            body, body * {{
                color: {colors['text']};
            }}
            
            /* Specifically target sidebar menu items */
            section[data-testid="stSidebar"] nav {{
                background-color: {colors['secondary_bg']} !important;
            }}
            
            section[data-testid="stSidebar"] nav * {{
                color: {colors['text']} !important;
            }}
            
            /* Target all links in sidebar */
            section[data-testid="stSidebar"] a,
            section[data-testid="stSidebar"] a *,
            section[data-testid="stSidebar"] a span {{
                color: {colors['text']} !important;
            }}
            
            /* Override Streamlit default white text */
            .st-emotion-cache-ysg2um,
            .st-emotion-cache-ysg2um *,
            .st-emotion-cache-hzygls,
            .st-emotion-cache-hzygls *,
            [class*="st-emotion-cache"] a,
            [class*="st-emotion-cache"] a span {{
                color: {colors['text']} !important;
            }}
            
            /* Input elements - complete override */
            input, textarea, select {{
                background-color: {colors['secondary_bg']} !important;
                color: {colors['text']} !important;
                border-color: {colors['border']} !important;
            }}
            
            /* Buttons text */
            button, button * {{
                color: {colors['text']};
            }}
            
            /* Exception for primary buttons */
            [data-testid="stButton"] button[kind="primary"],
            [data-testid="stButton"] button[kind="primary"] * {{
                color: white !important;
            }}
            
            /* Download button text */
            .stDownloadButton button,
            .stDownloadButton button * {{
                color: white !important;
            }}
            
            /* Theme toggle button text */
            .theme-toggle-sidebar button,
            .theme-toggle-sidebar button * {{
                color: white !important;
            }}
        </style>
        """
    
    @staticmethod
    def render_toggle_button():
        """Render theme toggle button"""
        current_theme = ThemeManager.get_theme()
        
        if current_theme == 'light':
            icon = "🌙"
            label = "Dark Mode"
        else:
            icon = "☀️"
            label = "Light Mode"
        
        # Use columns to position button at top right
        cols = st.columns([6, 1])
        with cols[1]:
            if st.button(f"{icon} {label}", key="theme_toggle_btn", use_container_width=True):
                ThemeManager.toggle_theme()
                st.rerun()


def get_theme_manager():
    """Get theme manager singleton"""
    return ThemeManager
