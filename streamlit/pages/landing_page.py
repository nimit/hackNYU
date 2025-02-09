import streamlit as st

def show_landing_page():
    # Main hero section
    st.title("Welcome to Spotifind")
    
    # Project description
    st.markdown("""
    <div style="background-color: #121212; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <h2 style="color: #FFFFFF;">About Spotifind</h2>
        <p style="color: #A7A7A7;">
            Spotifind is an innovative project designed to assist visually impaired individuals in finding objects and navigating their environment safely. 
            By leveraging advanced computer vision (CV) and artificial intelligence (AI) technologies, Spotifind helps users locate items and guides them to their destinations while avoiding obstacles.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("""
    <div style="background-color: #181818; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <h2 style="color: #FFFFFF;">Key Features</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="background-color: #282828; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #1ED760;">🎯 Object Detection</h3>
                <p style="color: #A7A7A7;">Utilizes computer vision to identify and locate objects in real-time.</p>
            </div>
            <div style="background-color: #282828; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #1ED760;">🛡️ Obstacle Avoidance</h3>
                <p style="color: #A7A7A7;">Guides users around obstacles using AI algorithms to ensure safe navigation.</p>
            </div>
            <div style="background-color: #282828; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #1ED760;">🤖 Generative AI Communication</h3>
                <p style="color: #A7A7A7;">Facilitates easy communication and transcribes conversations for better understanding.</p>
            </div>
            <div style="background-color: #282828; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #1ED760;">📊 MongoDB Integration</h3>
                <p style="color: #A7A7A7;">Stores obstacle data for efficient warning systems and precise item identification.</p>
            </div>
            <div style="background-color: #282828; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #1ED760;">⚡ Real-time Feedback</h3>
                <p style="color: #A7A7A7;">Provides users with immediate feedback on their surroundings and guidance.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Demo section
    st.markdown("""
    <div style="background-color: #121212; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <h2 style="color: #FFFFFF;">Demo Videos</h2>
        <p style="color: #A7A7A7;">Watch the following demo videos to see Spotifind in action:</p>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="margin: 1rem; width: 300px; background-color: #282828; border-radius: 8px; padding: 1rem;">
                <h3 style="color: #1ED760;">Demo Video 1</h3>
                <video width="100%" controls>
                    <source src="path_to_demo_video_1.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <div style="margin: 1rem; width: 300px; background-color: #282828; border-radius: 8px; padding: 1rem;">
                <h3 style="color: #1ED760;">Demo Video 2</h3>
                <video width="100%" controls>
                    <source src="path_to_demo_video_2.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Infographics section
    st.markdown("""
    <div style="background-color: #181818; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <h2 style="color: #FFFFFF;">Infographics</h2>
        <p style="color: #A7A7A7;">Here are some infographics that illustrate how Spotifind works:</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="margin: 1rem; background-color: #282828; border-radius: 8px; padding: 1rem;">
                <h3 style="color: #1ED760;">How Spotifind Works</h3>
                <img src="path_to_infographic_1.png" alt="How Spotifind Works" style="width: 100%; border-radius: 8px;">
            </div>
            <div style="margin: 1rem; background-color: #282828; border-radius: 8px; padding: 1rem;">
                <h3 style="color: #1ED760;">User Journey</h3>
                <img src="path_to_infographic_2.png" alt="User Journey" style="width: 100%; border-radius: 8px;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #FFFFFF;">Get Started with Spotifind</h2>
        <p style="color: #A7A7A7;">Join us in making the world more accessible for visually impaired individuals.</p>
        <a href="?page=signup" style="
            background-color: #1ED760; 
            color: #000000; 
            padding: 0.75rem 2rem; 
            border-radius: 500px; 
            text-decoration: none; 
            font-weight: 700;">Sign Up Now</a>
    </div>
    """, unsafe_allow_html=True)