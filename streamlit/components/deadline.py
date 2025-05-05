import streamlit as st
import requests
from datetime import datetime, timezone
import pytz

@st.cache_data(ttl=3600)
def get_next_deadline():
    """Get the next FPL gameweek deadline from the API."""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    events = data['events']
    current_event = next((event for event in events if event['is_current']), None)
    if current_event:
        return current_event['deadline_time']
    return None

def format_time_until_deadline(deadline_str):
    """Format the time remaining until the deadline."""
    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    time_left = deadline - now
    
    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def render_deadline():
    col1, col2, col3 = st.columns(3)
    local_tz = pytz.timezone('Europe/London')
    current_time = datetime.now(local_tz)
    last_updated_str = current_time.strftime('%-d %b, %H:%M %Z')

    deadline = get_next_deadline()
    if deadline:
        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        deadline_local = deadline_dt.astimezone(local_tz)
        deadline_str = deadline_local.strftime('%-d %b, %H:%M %Z')
        time_left = format_time_until_deadline(deadline)
    else:
        deadline_str = "-"
        time_left = "-"

    box_style = "background: #223344; color: #e0e6ed; border-radius: 12px; padding: 18px 24px; font-size: 1.1rem; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;"
    box_style2 = "background: #5a5a2e; color: #f7f7d4; border-radius: 12px; padding: 18px 24px; font-size: 1.1rem; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;"

    with col1:
        st.markdown(
            f"""
            <div style='{box_style}'>
                <span style='font-size:1.1em;'><b><span style="font-size:1.3em; vertical-align:middle;">⏰</span> Last updated:</b> {last_updated_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style='{box_style2}'>
                <span style='font-size:1.1em;'><b><span style="font-size:1.3em; vertical-align:middle;">🗓️</span> Next gameweek deadline:</b><br>{deadline_str}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style='{box_style2}'>
                <span style='font-size:1.1em;'><b><span style="font-size:1.3em; vertical-align:middle;">⏳</span> Time remaining:</b> {time_left}</span>
            </div>
            """,
            unsafe_allow_html=True
        ) 