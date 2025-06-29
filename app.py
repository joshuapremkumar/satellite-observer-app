import streamlit as st
from satellite_utils import fetch_satellite_data, extract_satellite_info, compute_current_position
from tavily_utils import get_ground_location_insight
from my_copilot_handler import CopilotKit
from appwrite_config import login_user
from datetime import datetime

copilot = CopilotKit(
    assistant_name="Satellite Observer Copilot",
    assistant_instructions="Assist astronomers in tracking satellites, provide viewing advice, and summarize ground conditions near satellite paths."
)

st.set_page_config(page_title="Satellite Observer Assistant", layout="wide")
st.title("🛰️ Satellite Observation Intelligence Assistant")

with st.sidebar:
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome, {email}!")
        else:
            st.error("Login failed. Check credentials.")

st.subheader("🔍 Search Satellite by NORAD Catalog Number")
catalog_number = st.text_input("Enter NORAD Catalog Number")

if st.button("Fetch Satellite Data") and catalog_number.isdigit():
    with st.spinner("Fetching data from CelesTrak..."):
        data = fetch_satellite_data(catalog_number)
        sat_info = extract_satellite_info(data)

    if "error" in data:
        st.error(f"Error: {data['error']}")
    elif sat_info:
        st.success(f"Satellite Found: {sat_info['name']}")
        st.json(sat_info)

        with st.spinner("Computing real-time orbital position..."):
            lat, lon = compute_current_position(sat_info)
            st.markdown(f"📍 Real-Time Position: Latitude {lat:.4f}, Longitude {lon:.4f}")

        with st.spinner("Querying Tavily for ground insights..."):
            tavily_results = get_ground_location_insight(lat, lon)

        if tavily_results:
            st.subheader("🌍 Ground Location Insights")
            for result in tavily_results:
                st.markdown(f"**{result['title']}**\n{result['content']}\n[Read more]({result['url']})")
        else:
            st.warning("No relevant insights found from Tavily.")

        if st.button("🧠 Summarize with CopilotKit"):
            current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            user_prompt = f"""
Satellite Observation Report:
- Name: {sat_info['name']}
- NORAD ID: {catalog_number}
- Real-time Observation at {current_time}
- Coordinates: Latitude {lat:.4f}, Longitude {lon:.4f}
- Nearby ground location information includes: {[r['title'] for r in tavily_results] if tavily_results else 'N/A'}

Please generate a concise summary for astronomers including:
1. Observation condition and location insights
2. Whether this satellite is observable from the given coordinates
3. Suggestions for follow-up observation or research
"""
            response = copilot.chat(user_prompt)
            st.markdown("### 🧠 Copilot Summary")
            st.markdown(response)
    else:
        st.warning("No valid satellite data returned.")

st.markdown("---")
st.markdown("📡 Built using CelesTrak, Tavily, CopilotKit, Appwrite and Streamlit")