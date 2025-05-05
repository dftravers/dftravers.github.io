import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.deadline import render_deadline
from components.cards import render_feature_cards

# Page setup
st.set_page_config(
    page_title="FPL Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Render components
render_header()
render_deadline()
st.header("📊 Available Tools")
render_feature_cards()
render_footer()
