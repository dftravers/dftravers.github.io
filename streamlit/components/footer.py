import streamlit as st

def render_footer():
    """Render the application footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit</p>
        <p>Data provided by the official FPL API</p>
    </div>
    """, unsafe_allow_html=True) 