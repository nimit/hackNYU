import streamlit as st
import requests

def show_signup_page():
    # Center the signup form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Container for the entire signup form
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
                ">Sign up for free to start listening</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Signup Form
        st.markdown("<p style='margin-bottom: 0.5rem; color: #FFFFFF; font-weight: 500;'>What's your email?</p>", unsafe_allow_html=True)
        email = st.text_input(
            "Email address",
            key="signup_email",
            label_visibility="collapsed",
            placeholder="Enter your email."
        )
        
        st.markdown("<p style='margin: 1rem 0 0.5rem 0; color: #FFFFFF; font-weight: 500;'>Create a password</p>", unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            key="signup_password",
            label_visibility="collapsed",
            placeholder="Create a password."
        )
        
        st.markdown("<p style='margin: 1rem 0 0.5rem 0; color: #FFFFFF; font-weight: 500;'>What should we call you?</p>", unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            key="username",
            label_visibility="collapsed",
            placeholder="Enter a profile name."
        )
        
        st.markdown("""
            <p style="color: #A7A7A7; font-size: 0.875rem; margin: 0.5rem 0;">
                This appears on your profile.
            </p>
        """, unsafe_allow_html=True)
        
        # Terms and Conditions
        st.markdown("""
            <div style="margin: 2rem 0; color: #A7A7A7; font-size: 0.875rem;">
                <p>By clicking on sign-up, you agree to Spotifind's 
                    <a href="#" style="color: #1ED760; text-decoration: none;">Terms and Conditions of Use</a>.
                </p>
                <p style="margin-top: 1rem;">
                    To learn more about how Spotifind collects, uses, shares and protects your personal data, 
                    please see <a href="#" style="color: #1ED760; text-decoration: none;">Spotifind's Privacy Policy</a>.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Sign Up Button
        if st.button("SIGN UP", type="primary", key="signup_button"):
            response = requests.post("http://localhost:5000/signup", json={"username": username, "email": email, "password": password})
            if response.status_code == 201:
                st.success("User created successfully!")
                # Redirect to login or another page
            else:
                st.error(response.json().get("message"))
        
        # Login Link
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <p style="color: #A7A7A7;">Have an account? 
                    <a href="?page=login" style="color: #1ED760; text-decoration: none; font-weight: 500;">
                        Log in
                    </a>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) 