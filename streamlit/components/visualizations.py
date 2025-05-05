import plotly.express as px

def create_goals_xg_plot(df):
    """Create scatter plot of goals vs expected goals"""
    return px.scatter(
        df,
        x='expected_goals',
        y='goals_scored',
        hover_data=['first_name', 'second_name', 'team_name', 'position'],
        title='Goals vs Expected Goals',
        labels={'expected_goals': 'Expected Goals', 'goals_scored': 'Actual Goals'}
    )

def create_assists_xa_plot(df):
    """Create scatter plot of assists vs expected assists"""
    return px.scatter(
        df,
        x='expected_assists',
        y='assists',
        hover_data=['first_name', 'second_name', 'team_name', 'position'],
        title='Assists vs Expected Assists',
        labels={'expected_assists': 'Expected Assists', 'assists': 'Actual Assists'}
    )

def create_top_points_plot(df):
    """Create bar chart of top 10 players by points"""
    top_players = df.nlargest(10, 'total_points')
    return px.bar(
        top_players,
        x='first_name' + ' ' + top_players['second_name'],
        y='total_points',
        title='Top 10 Players by Total Points',
        labels={'x': 'Player', 'y': 'Total Points'}
    ) 