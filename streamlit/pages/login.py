import streamlit as st
import requests

def show_login_page():
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Container for the entire login form
        st.markdown("""
        <div style="
            background-color: #121212;
            border-radius: 8px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 734px;
        ">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="
                    color: #FFFFFF;
                    font-size: 2rem !important;
                    font-weight: 700;
                    margin-bottom: 2rem;
                ">Log in to Spotifind</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Login Form
        st.markdown("<p style='margin-bottom: 0.5rem; color: #FFFFFF; font-weight: 500;'>Email or username</p>", unsafe_allow_html=True)
        email = st.text_input(
            "Email or username",
            key="email",
            label_visibility="collapsed",
            placeholder="Enter your email or username"
        )
        
        st.markdown("<p style='margin: 1rem 0 0.5rem 0; color: #FFFFFF; font-weight: 500;'>Password</p>", unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            key="password",
            label_visibility="collapsed",
            placeholder="Enter your password"
        )
        
        # Remember Me and Forgot Password
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me", key="remember_me")
        with col2:
            st.markdown("""
                <div style="text-align: right;">
                    <a href="#" style="color: #1ED760; text-decoration: none;">Forgot your password?</a>
                </div>
            """, unsafe_allow_html=True)
        
        # Login Button
        st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
        if st.button("LOG IN", type="primary", key="login_button"):
            response = requests.post("http://localhost:5000/login", json={"email": email, "password": password})
            print("Response Status Code:", response.status_code)  # Debugging line
            print("Response Content:", response.content)  # Debugging line
            
            if response.status_code == 200:
                token = response.json().get("token")
                st.session_state["token"] = token
                st.success("Logged in successfully!")
                # Redirect to another page or perform actions
            else:
                st.error("Error: " + response.text)  # Show the raw response text
        
        # Sign Up Link
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <p style="color: #A7A7A7;">Don't have an account? 
                    <a href="?page=signup" style="color: #1ED760; text-decoration: none; font-weight: 500;">
                        Sign up for Spotifind
                    </a>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) 