import streamlit as st
from pages.landing_page import show_landing_page
from pages.login import show_login_page
from pages.signup import show_signup_page
from pages.add_obstacle import show_add_obstacle_page
from pages.view_obstacles import show_view_obstacles_page
from pymongo import MongoClient
import jwt
import datetime
import bcrypt
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Get secret key from .env

# MongoDB Atlas connection
client = MongoClient(os.getenv('MONGO_URI'))  # Get MongoDB URI from .env
db = client['your_database_name']  # Replace with your database name
users_collection = db['users']
obstacles_collection = db['obstacles']

# Set page configuration as the first command
st.set_page_config(
    page_title="SpotiFind",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide default menu and sidebar nav
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] > div {padding-top: 0rem;}
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
            color: #FFFFFF;
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

        /* Hide sidebar completely */
        [data-testid="stSidebarNavItems"] {
            display: none;  /* Hide sidebar navigation items */
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #000000;
            padding: 2rem 1rem;
            display: hidden;
        }
        
        /* Sidebar navigation styling */
        .sidebar-nav {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .sidebar-nav .stButton > button {
            background-color: transparent;
            color: #000000;
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
            background: #000000;
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
        
        /* Change button font color to black */
        .stButton > button {
            color: black !important;  /* Set button text color to black */
        }
        
        /* Change sidebar button font color to black */
        .sidebar .stButton > button {
            color: black !important;  /* Set sidebar button text color to black */
        }
        /* Change the hover color for buttons to ensure visibility */
        .stButton > button:hover {
            color: black !important;  /* Ensure hover color is also black */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_custom_css()

def main():
    # Initialize session state for active page
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'landing_page'  # Default to landing page
    if 'user' not in st.session_state:
        st.session_state.user = None  # No user logged in


    # Sidebar navigation
    with st.sidebar:
        st.title("SpotiFind")
        
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

        # View Obstacles button
        if st.button("View Obstacles", key="view_obstacles"):
            st.session_state.active_page = 'view_obstacles'

    # Call the function to display the active page
    active_page = st.session_state.get('active_page', 'landing_page')
    if active_page == 'landing_page':
        print("Landing Page Active")
        show_landing_page()
    elif active_page == 'login':
        print("Login Page Active")
        show_login_page(users_collection)
    elif active_page == 'signup':
        print("Sign Up Page Active")
        show_signup_page(users_collection)
    elif active_page == 'add_obstacle':
        print("Add Obstacle Page Active")
        show_add_obstacle_page(obstacles_collection)
    elif active_page == 'view_obstacles':
        print("View Obstacles Page Active")
        show_view_obstacles_page(obstacles_collection)
    else:
        st.session_state.active_page = 'landing_page'  # Default to landing page if not set

if __name__ == "__main__":
    main()

