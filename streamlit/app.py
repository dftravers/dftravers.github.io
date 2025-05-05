import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(
    page_title="FPL Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Title and description
st.title("⚽ Fantasy Premier League Analytics")
st.markdown("""
Welcome to the FPL Analytics Dashboard! This tool helps you make data-driven decisions for your Fantasy Premier League team.
""")

# Get next gameweek deadline
@st.cache_data(ttl=3600)
def get_next_deadline():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    events = data['events']
    current_event = next((event for event in events if event['is_current']), None)
    if current_event:
        return current_event['deadline_time']
    return None

# Display last updated and next deadline
col1, col2 = st.columns(2)
with col1:
    st.info(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    deadline = get_next_deadline()
    if deadline:
        st.warning(f"Next gameweek deadline: {deadline}")

# Features overview
st.header("📊 Available Tools")

# Create three columns for feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 Player Database
    Comprehensive database of all FPL players with detailed statistics and visualizations.
    - Player performance metrics
    - Expected stats (xG, xA)
    - Per 90 statistics
    - Interactive visualizations
    """)

with col2:
    st.markdown("""
    ### 📈 Point Predictions
    Coming soon: Predict player points for upcoming gameweeks.
    - Historical performance analysis
    - Fixture difficulty consideration
    - Form and fitness factors
    - Customizable predictions
    """)

with col3:
    st.markdown("""
    ### 🔄 Transfer Suggester
    Coming soon: Get transfer suggestions based on your team.
    - Team analysis
    - Fixture difficulty
    - Value for money
    - Form and fitness
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit</p>
    <p>Data provided by the official FPL API</p>
</div>
""", unsafe_allow_html=True)
