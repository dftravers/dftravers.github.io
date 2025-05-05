import streamlit as st
import pandas as pd

from utils.data_loader import load_fpl_data
from components.filters import create_player_filters
from components.visualizations import (
    create_goals_xg_plot,
    create_assists_xa_plot,
    create_top_points_plot
)

# Page setup
st.set_page_config(
    page_title="Player Database - FPL Analytics",
    page_icon="⚽",
    layout="wide"
)

st.title("🎯 Player Database")

st.markdown("""
This page will contain a comprehensive database of all FPL players with detailed statistics and visualizations.
""")

# Placeholder for future implementation
st.info("This feature is under development. Check back soon!")

# Load data
df = load_fpl_data()

# Create filters
selected_positions, selected_teams, selected_cost_range, selected_minutes = create_player_filters(df)

# Apply filters
filtered_df = df[
    (df['position'].isin(selected_positions)) &
    (df['team_name'].isin(selected_teams)) &
    (df['price_million'].between(*selected_cost_range)) &
    (df['minutes_played'] >= selected_minutes)
]

# Display filtered data
st.write("### Player Statistics")

# Create tabs for different views
tab1, tab2 = st.tabs(["Table View", "Visualizations"])

with tab1:
    # Select columns to display
    columns_to_display = [
        'first_name', 'second_name', 'team_name', 'position',
        'price_million', 'minutes_played', 'goals_scored', 'assists',
        'expected_goals', 'expected_assists', 'goals_per_90', 'assists_per_90',
        'xG_per_90', 'xA_per_90', 'yellow_cards', 'red_cards',
        'total_points', 'form', 'selected_by_percent'
    ]
    
    # Rename columns for display
    column_names = {
        'first_name': 'First Name',
        'second_name': 'Last Name',
        'team_name': 'Team',
        'position': 'Position',
        'price_million': 'Price (£M)',
        'minutes_played': 'Minutes',
        'goals_scored': 'Goals',
        'assists': 'Assists',
        'expected_goals': 'xG',
        'expected_assists': 'xA',
        'goals_per_90': 'Goals/90',
        'assists_per_90': 'Assists/90',
        'xG_per_90': 'xG/90',
        'xA_per_90': 'xA/90',
        'yellow_cards': 'Yellow Cards',
        'red_cards': 'Red Cards',
        'total_points': 'Total Points',
        'form': 'Form',
        'selected_by_percent': 'Selected By %'
    }
    
    display_df = filtered_df[columns_to_display].rename(columns=column_names)
    st.dataframe(display_df, use_container_width=True)

with tab2:
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_goals_xg_plot(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_assists_xa_plot(filtered_df), use_container_width=True)
    
    st.plotly_chart(create_top_points_plot(filtered_df), use_container_width=True) 