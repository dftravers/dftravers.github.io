import streamlit as st

def render_feature_cards():
    """Render the feature cards section."""
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