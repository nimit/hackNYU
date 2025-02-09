import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import st_folium
import base64
import os

def show_add_obstacle_page(obstacles_collection):
    st.title("Add an Obstacle")

    # Initialize session state variables
    if 'user_location' not in st.session_state:
        st.session_state.user_location = None
    if 'map_visible' not in st.session_state:
        st.session_state.map_visible = False
    if 'tagged_location' not in st.session_state:
        st.session_state.tagged_location = None

    # JavaScript to get user's location
    st.components.v1.html("""
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const location = lat + ',' + lon;
                    // Send the location back to Streamlit
                    const streamlit = window.parent.document.querySelector('iframe').contentWindow;
                    streamlit.postMessage({type: 'set_location', location: location}, '*');
                }, function() {
                    alert("Unable to retrieve your location. Please check your browser settings.");
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    </script>
    """, height=0)

    initial_location = [37.7749, -122.4194]

    # Button to access the map and get user's location
    if st.button("Access Map"):
        st.session_state.map_visible = True
        st.components.v1.html("<script>getLocation();</script>", height=0)
        #take the location and store it as the initial location
        if st.session_state.user_location:
            user_lat, user_lon = map(float, st.session_state.user_location.split(','))
            initial_location = [user_lat, user_lon]

    # Create a Folium map
    if st.session_state.map_visible:
        if st.session_state.user_location:
            user_lat, user_lon = map(float, st.session_state.user_location.split(','))
            initial_location = [user_lat, user_lon]

        m = folium.Map(location=initial_location, zoom_start=15)

        # Add a marker for the user's location if available
        if st.session_state.user_location:
            folium.Marker(
                location=[user_lat, user_lon],
                popup="Your Location",
                icon=folium.Icon(color="blue")
            ).add_to(m)

        # Display the map in Streamlit
        selected_location = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])

        # Check if a location was tagged
        if selected_location and selected_location['last_clicked']:
          st.session_state.tagged_location = selected_location['last_clicked']
          st.write(f"Tagged Location: Lat {st.session_state.tagged_location['lat']}, Lng {st.session_state.tagged_location['lng']}")

    # Form for adding an obstacle
    with st.form(key='obstacle_form'):
        email = st.text_input("Your Email", key="email")
        description = st.text_area("Obstacle Description", key="description")
        status = st.selectbox("Status", options=["Active", "Inactive"], key="status")
        
        # Optional photo upload
        photo = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])

        # Submit button
        submit_button = st.form_submit_button("Add Obstacle")

        if submit_button:
            if email and description and st.session_state.tagged_location:
                # Prepare the data to send to the backend
                obstacle_data = {
                    "email": email,
                    "description": description,
                    "status": status,
                    "location": {
                        "latitude": st.session_state.tagged_location['lat'],
                        "longitude": st.session_state.tagged_location['lng']
                    },
                    "timestamp": datetime.now().isoformat()
                }

                # Handle photo upload
                if photo is not None:
                    # Decode the base64 photo
                    photo_bytes = base64.b64decode(photo)
                    photo_filename = f"obstacle_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                    
                    # Save the photo to the filesystem (optional)
                    with open(os.path.join("uploads", photo_filename), "wb") as f:
                        f.write(photo_bytes)

                    # Add the filename to the document
                    obstacle_data["photo"] = photo_filename

                # Insert the document into MongoDB
                obstacles_collection.insert_one(obstacle_data)

                st.success("Obstacle added successfully!")
            else:
                st.error("Please fill in all fields and tag a location on the map.")

    # Listen for messages from the JavaScript
    st.components.v1.html("""
    <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'set_location') {
                const location = event.data.location;
                const streamlit = window.parent.document.querySelector('iframe').contentWindow;
                streamlit.setComponentValue({user_location: location});
            }
        });
    </script>
    """, height=0)
