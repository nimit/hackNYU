import streamlit as st
import folium
from streamlit_folium import st_folium
from pymongo import MongoClient

def show_view_obstacles_page(obstacles_collection):
    st.title("View Obstacles")

    # Fetch all obstacles from MongoDB
    obstacles = list(obstacles_collection.find())

    if not obstacles:
        st.write("No obstacles found.")
        return

    # Get the center location (you can modify this logic as needed)
    center_lat = obstacles[0]['location']['latitude']
    center_lon = obstacles[0]['location']['longitude']

    # Create a Folium map centered on the first obstacle
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add markers for each obstacle
    for obstacle in obstacles:
        folium.Marker(
            location=[obstacle['location']['latitude'], obstacle['location']['longitude']],
            popup=f"Description: {obstacle['description']}\nStatus: {obstacle['status']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500) 