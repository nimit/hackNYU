import streamlit as st
from pages.landing_page import show_landing_page
from pages.login import show_login_page
from pages.signup import show_signup_page
from pages.add_obstacle import show_add_obstacle_page

# Set page configuration as the first command
st.set_page_config(
    page_title="Spotifind",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default menu and sidebar nav
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] > div {padding-top: 0rem;}
    .css-1d391kg {display: none;}  /* Hide default sidebar nav */
    .css-1q1n0ol {display: none;}  /* Hide additional sidebar elements */
</style>
""", unsafe_allow_html=True)

def add_custom_css():
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        
        /* Base styles and resets */
        * {
            font-family: 'Montserrat', sans-serif;
        }
        
        /* Spotify-like dark theme */
        .stApp {
            background: #000000;
        }
        
        /* Custom title styling */
        h1 {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 2.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Subheader styling */
        h2, h3 {
            color: #FFFFFF;
            font-weight: 600;
            font-size: 1.5rem !important;
        }
        
        /* Paragraph text */
        p {
            color: #A7A7A7;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Custom button styling - Spotify green */
        .stButton > button {
            width: 100%;
            background-color: #1ED760;
            border: none;
            border-radius: 500px;
            color: #000000;
            padding: 0.875rem 2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.875rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #1FDF64;
            transform: scale(1.04);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #000000;
            padding: 2rem 1rem;
        }
        
        /* Sidebar navigation styling */
        .sidebar-nav {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .sidebar-nav .stButton > button {
            background-color: transparent;
            color: #B3B3B3;
            text-align: left;
            text-transform: none;
            letter-spacing: normal;
            padding: 0.5rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 4px;
        }
        
        .sidebar-nav .stButton > button:hover {
            color: #FFFFFF;
            background-color: #282828;
            transform: none;
        }
        
        /* Content container styling */
        .content-container {
            background: #181818;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: background-color 0.3s ease;
        }
        
        .content-container:hover {
            background: #282828;
        }
        
        /* Input fields styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #121212;
            border: 1px solid #727272;
            border-radius: 4px;
            color: white;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #FFFFFF;
            box-shadow: none;
        }
        
        /* Login form styling */
        .login-container {
            max-width: 734px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #121212;
            border-radius: 8px;
        }
        
        .divider {
            text-align: center;
            position: relative;
            margin: 1.5rem 0;
        }
        
        .divider::before,
        .divider::after {
            content: "";
            position: absolute;
            top: 50%;
            width: 45%;
            height: 1px;
            background-color: #282828;
        }
        
        .divider::before {
            left: 0;
        }
        
        .divider::after {
            right: 0;
        }
        
        /* Link styling */
        a {
            color: #1ED760;
            text-decoration: underline;
            transition: color 0.3s ease;
        }
        
        a:hover {
            color: #1FDF64;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_custom_css()

def main():
    # Initialize session state for active page
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'landing_page'  # Ensure it starts on the landing page

    # Debugging output to check the active page
    st.write(f"Current active page: {st.session_state.active_page}")

    # Sidebar navigation
    with st.sidebar:
        st.title("Spotifind")
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

        # Home button
        if st.button("🏠 Home", key="home"):
            st.session_state.active_page = 'landing_page'
        
        # Login button
        if st.button("🔑 Login", key="login"):
            st.session_state.active_page = 'login'
        
        # Sign Up button
        if st.button("👤 Sign Up", key="signup"):
            st.session_state.active_page = 'signup'
        
        # Add Obstacle button
        if st.button("🛑 Add Obstacle", key="add_obstacle"):
            st.session_state.active_page = 'add_obstacle'
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Page navigation logic
    if st.session_state.active_page == 'landing_page':
        show_landing_page()
    elif st.session_state.active_page == 'login':
        show_login_page()
    elif st.session_state.active_page == 'signup':
        show_signup_page()
    elif st.session_state.active_page == 'add_obstacle':
        show_add_obstacle_page()

if __name__ == "__main__":
    main()

