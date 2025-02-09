import streamlit as st
import requests
import time

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
                ">Sign up for Spotifind</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Signup Form
        email = st.text_input("Email address", key="signup_email", placeholder="Enter your email.")
        password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a password.")
        username = st.text_input("Username", key="username", placeholder="Enter a profile name.")
        
        # Solana Wallet Address
        solana_wallet = st.text_input("Solana Wallet Address", key="solana_wallet", placeholder="Connect your Phantom wallet.", disabled=True)
        
        # Button to connect Phantom wallet
        if st.button("Connect Phantom Wallet", key="connect_wallet"):
            st.components.v1.html(
                """
                <script>
                    async function connectAndSendKey() {
                        if (window.solana && window.solana.isPhantom) {
                            try {
                                const response = await window.solana.connect();
                                const publicKey = response.publicKey.toString();
                                // Notify the parent window with the public key via query parameter update.
                                const currentUrl = new URL(window.location.href);
                                currentUrl.searchParams.set("wallet", publicKey);
                                window.location.href = currentUrl.toString();
                            } catch (err) {
                                console.error(err);
                                alert("Connection failed. Please try again.");
                            }
                        } else {
                            alert("Phantom wallet not found. Please install it from https://phantom.app.");
                        }
                    }
                    connectAndSendKey();
                </script>
                """,
                height=0
            )


        # Display the connected wallet address
        if st.session_state.get("solana_wallet"):
            st.success(f"Connected Wallet: {st.session_state.solana_wallet}")

        # Sign Up Button
        if st.button("SIGN UP", type="primary", key="signup_button"):
            response = requests.post("http://localhost:5000/signup", json={
                "username": username,
                "email": email,
                "password": password,
                "solana_wallet": st.session_state.get("solana_wallet")  # Include the Solana wallet address
            })
            
            if response.status_code == 201:
                st.success("Signup successful! Redirecting...")
                time.sleep(2)  # Wait for 2 seconds
                st.experimental_rerun()  # Redirect to the landing page
            else:
                st.error("Error: " + response.json().get("message", "Unknown error"))
        
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