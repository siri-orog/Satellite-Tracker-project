import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from PIL import Image
import os
import urllib.request
import time

# ----------------------------------------------------
# 🌍 Step 1: Setup Streamlit Page
# ----------------------------------------------------
st.set_page_config(page_title="Live ISS Tracker 🌎", page_icon="🛰️", layout="wide")

st.title("🛰️ Real-Time ISS Tracker on 3D Earth Globe")
st.markdown("""
This app shows the **live position of the International Space Station (ISS)** with its country, state, and local time.  
The red trail shows the ISS path around the Earth.
""")

# ----------------------------------------------------
# 🌐 Step 2: Earth Image with Borders

# ----------------------------------------------------
earth_img = "earth_with_borders.jpg"
earth_url = "https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74218/world.topo.bathy.200412.3x21600x10800.jpg"

if not os.path.exists(earth_img):
    st.info("🌍 Downloading Earth texture with borders...")
    urllib.request.urlretrieve(earth_url, earth_img)
    st.success("✅ Earth texture image ready!")

# ----------------------------------------------------
# 🧮 Step 3: Convert Lat/Lon to 3D Coordinates
# ----------------------------------------------------
def latlon_to_xyz(lat, lon, alt_km=420):
    R = 6371 + alt_km
    lat_r = np.radians(lat)
    lon_r = np.radians(lon)
    x = R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)
    return x, y, z

# ----------------------------------------------------
# 📡 Step 4: Get Live ISS Position
# ----------------------------------------------------
def get_iss_position():
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        lat = float(response["iss_position"]["latitude"])
        lon = float(response["iss_position"]["longitude"])
        x, y, z = latlon_to_xyz(lat, lon)
        return x, y, z, lat, lon
    except Exception as e:
        st.error(f"Error getting ISS position: {e}")
        return None

# ----------------------------------------------------
# 🗺️ Step 5: Reverse Geocode (Country, State, Time)
# ---------------------------------------------------

