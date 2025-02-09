import streamlit as st
import requests
import time
import jwt
import bcrypt

def show_signup_page(users_collection):

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
                ">Sign up for SpotiFind</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Signup Form
        email = st.text_input("Email address", key="signup_email", placeholder="Enter your email.")
        password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a password.")
        username = st.text_input("Username", key="username", placeholder="Enter a profile name.")
        wallet_address = st.text_input("Solana Wallet Address")  # New field for wallet address
    
        # Sign Up Button
        if st.button("SIGN UP", type="primary", key="signup_button"):
            if users_collection.find_one({"email": email}):
                st.error("Email address already exists!")
                return
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            new_user = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "wallet_address": wallet_address
            }
            users_collection.insert_one(new_user)
            
            st.success("User created successfully!")
            # Redirect to landing page after 2 seconds
            time.sleep(2)
            st.session_state.active_page = 'landing_page'
        
        # Sign In Link
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <p style="color: #A7A7A7;">Have an account? 
                    <a href="login" target="_blank" style="color: #1ED760; text-decoration: none; font-weight: 500;">
                        Log in
                    </a>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) 