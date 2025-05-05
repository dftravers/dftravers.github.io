import streamlit as st

def create_player_filters(df):
    """
    Create sidebar filters for player data
    Args:
        df (pd.DataFrame): Player data
    Returns:
        tuple: Selected filter values
    """
    st.sidebar.header("Filter Players")

    # Position filter
    positions = df['position'].unique()
    selected_positions = st.sidebar.multiselect(
        "Select Positions",
        positions,
        default=positions
    )

    # Team filter
    teams = sorted(df['team_name'].unique())
    selected_teams = st.sidebar.multiselect(
        "Select Teams",
        teams,
        default=teams
    )

    # Price range filter
    min_cost = float(df['price_million'].min())
    max_cost = float(df['price_million'].max())
    selected_cost_range = st.sidebar.slider(
        "Select Price Range (in £M)",
        min_cost,
        max_cost,
        (min_cost, max_cost),
        step=0.1
    )

    # Minutes played filter
    min_minutes = int(df['minutes_played'].min())
    max_minutes = int(df['minutes_played'].max())
    selected_minutes = st.sidebar.slider(
        "Minimum Minutes Played",
        min_minutes,
        max_minutes,
        min_minutes,
        step=50
    )

    return selected_positions, selected_teams, selected_cost_range, selected_minutes 