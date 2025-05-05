import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(page_title="Fantasy Premier League Dashboard", layout="wide")
st.title("🏈 Fantasy Premier League Dashboard")

# Load Fantasy Premier League (FPL) Data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_fpl_data():
    # Fetch data from FPL API
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    
    # Convert elements to DataFrame
    df = pd.DataFrame(data['elements'])
    
    # Get team names and strength data
    teams_df = pd.DataFrame(data['teams'])
    teams = {team['id']: team['name'] for team in data['teams']}
    df['team_name'] = df['team'].map(teams)
    
    # Get position names
    positions = {pos['id']: pos['singular_name'] for pos in data['element_types']}
    df['position'] = df['element_type'].map(positions)
    
    # Convert price to millions
    df['price_million'] = df['now_cost'] / 10
    
    # Add expected stats
    df['xG'] = df.get('expected_goals', float('nan'))
    df['xA'] = df.get('expected_assists', float('nan'))
    df['xGI'] = df.get('expected_goal_involvements', float('nan'))
    df['xP'] = df.get('expected_points', float('nan'))
    
    # Add team strength data
    team_strength = teams_df[['id', 'strength', 'strength_overall_home', 'strength_overall_away']]
    team_strength = team_strength.rename(columns={
        'id': 'team',
        'strength': 'team_strength',
        'strength_overall_home': 'home_strength',
        'strength_overall_away': 'away_strength'
    })
    df = df.merge(team_strength, on='team', how='left')
    
    # Calculate value metrics
    df['form'] = pd.to_numeric(df['form'], errors='coerce')
    df['total_points'] = pd.to_numeric(df['total_points'], errors='coerce')
    df['price_million'] = pd.to_numeric(df['price_million'], errors='coerce')
    df['points_per_million'] = df['total_points'] / df['price_million']
    df['form_per_million'] = df['form'] / df['price_million']
    
    return df, teams_df

# Load fixtures data
@st.cache_data(ttl=3600)
def load_fixtures_data():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    fixtures = pd.DataFrame(response.json())
    return fixtures

# Load data
df, teams_df = load_fpl_data()
fixtures_df = load_fixtures_data()

# Sidebar Filters
st.sidebar.header("Filter Players")

# Position filter
positions = df['position'].unique()
selected_positions = st.sidebar.multiselect(
    "Select Positions",
    positions,
    default=positions
)

# Budget filter
min_cost = float(df['price_million'].min())
max_cost = float(df['price_million'].max())
selected_cost_range = st.sidebar.slider(
    "Select Price Range (in £M)",
    min_cost,
    max_cost,
    (min_cost, max_cost),
    step=0.1
)

# Apply filters
filtered_df = df[
    (df['position'].isin(selected_positions)) &
    (df['price_million'].between(*selected_cost_range))
]

# Display filtered data
st.write("### Player Statistics")
st.dataframe(
    filtered_df[[
        'first_name', 'second_name', 'team_name', 'position',
        'price_million', 'total_points', 'form', 'selected_by_percent',
        'xG', 'xA', 'xGI', 'points_per_million', 'form_per_million'
    ]].rename(columns={
        'first_name': 'First Name',
        'second_name': 'Last Name',
        'team_name': 'Team',
        'position': 'Position',
        'price_million': 'Price (£M)',
        'total_points': 'Total Points',
        'form': 'Form',
        'selected_by_percent': 'Selected By %',
        'xG': 'Expected Goals',
        'xA': 'Expected Assists',
        'xGI': 'Expected Goal Involvements',
        'points_per_million': 'Points/£M',
        'form_per_million': 'Form/£M'
    }),
    use_container_width=True
)

# Top 10 Players by Total Points
st.write("### Top 10 Players by Total Points")
top_players = filtered_df.sort_values('total_points', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top_players['first_name'] + ' ' + top_players['second_name'],
    top_players['total_points'],
    color='blue'
)
ax.set_xlabel('Total Points')
ax.set_ylabel('Player')
ax.set_title('Top 10 Fantasy Premier League Players (by Total Points)')
ax.invert_yaxis()  # Flip order so highest is at the top
st.pyplot(fig)

# Team Strength Analysis
st.write("### Team Strength Analysis")
team_strength = teams_df[['name', 'strength', 'strength_overall_home', 'strength_overall_away']]
team_strength = team_strength.sort_values('strength', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(team_strength))
width = 0.25

ax.bar(x - width, team_strength['strength'], width, label='Overall Strength')
ax.bar(x, team_strength['strength_overall_home'], width, label='Home Strength')
ax.bar(x + width, team_strength['strength_overall_away'], width, label='Away Strength')

ax.set_xlabel('Team')
ax.set_ylabel('Strength Rating')
ax.set_title('Team Strength Comparison')
ax.set_xticks(x)
ax.set_xticklabels(team_strength['name'], rotation=45, ha='right')
ax.legend()

plt.tight_layout()
st.pyplot(fig)

# Value Analysis
st.write("### Best Value Players (Points per Million)")
value_players = filtered_df.sort_values('points_per_million', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    value_players['first_name'] + ' ' + value_players['second_name'],
    value_players['points_per_million'],
    color='green'
)
ax.set_xlabel('Points per Million')
ax.set_ylabel('Player')
ax.set_title('Top 10 Value Players')
ax.invert_yaxis()
st.pyplot(fig)
