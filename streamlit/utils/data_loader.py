import pandas as pd
import requests
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_fpl_data():
    """
    Load and process FPL data from the official API
    Returns:
        pd.DataFrame: Processed FPL data
    """
    # Fetch data from FPL API
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    
    # Convert elements to DataFrame
    df = pd.DataFrame(data['elements'])
    
    # Get team names
    teams = {team['id']: team['name'] for team in data['teams']}
    df['team_name'] = df['team'].map(teams)
    
    # Get position names
    positions = {pos['id']: pos['singular_name'] for pos in data['element_types']}
    df['position'] = df['element_type'].map(positions)
    
    # Convert numeric columns
    numeric_columns = [
        'now_cost', 'minutes', 'goals_scored', 'assists',
        'expected_goals', 'expected_assists', 'total_points',
        'form', 'selected_by_percent'
    ]
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert price to millions
    df['price_million'] = df['now_cost'] / 10
    
    # Calculate per 90 stats
    df['minutes_played'] = df['minutes']
    df['goals_per_90'] = (df['goals_scored'] / df['minutes_played']) * 90
    df['assists_per_90'] = (df['assists'] / df['minutes_played']) * 90
    df['xG_per_90'] = (df['expected_goals'] / df['minutes_played']) * 90
    df['xA_per_90'] = (df['expected_assists'] / df['minutes_played']) * 90
    
    # Fill NaN values with 0 for per 90 stats
    per_90_columns = ['goals_per_90', 'assists_per_90', 'xG_per_90', 'xA_per_90']
    df[per_90_columns] = df[per_90_columns].fillna(0)
    
    return df 