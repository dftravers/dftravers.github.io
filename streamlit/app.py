import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title="Fantasy Premier League Dashboard", layout="wide")

st.title("🏈 Fantasy Premier League Dashboard (2024-25)")

# Load Fantasy Premier League (FPL) Data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2024-25/cleaned_players.csv"
    df = pd.read_csv(url)

    # Rename 'element_type' to 'Position' for clarity
    position_mapping = {
        "GK": "Goalkeeper",
        "DEF": "Defender",
        "MID": "Midfielder",
        "FWD": "Forward"
    }
    df["Position"] = df["element_type"].map(position_mapping)

    return df

df = load_data()

# **Sidebar Filters**
st.sidebar.header("Filter Players")

# Extract unique positions and cost ranges
positions = df["Position"].unique().tolist()
min_cost, max_cost = int(df["now_cost"].min()), int(df["now_cost"].max())

# **User selection for filters**
selected_positions = st.sidebar.multiselect("Select Position", positions, default=positions)
selected_cost_range = st.sidebar.slider("Select Price Range (in £M)", min_cost, max_cost, (min_cost, max_cost))

# **Apply filters**
filtered_df = df[
    (df["Position"].isin(selected_positions)) & 
    (df["now_cost"].between(*selected_cost_range))
]

# **Display table with filtered player stats**
st.write("### Player Statistics (Filtered)")
st.dataframe(filtered_df)

# **Top 10 Players by Total Points**
st.write("### Top 10 Players by Total Points")
top_players = filtered_df.sort_values("total_points", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(
    top_players["first_name"] + " " + top_players["second_name"],
    top_players["total_points"],
    color="blue"
)
ax.set_xlabel("Total Points")
ax.set_ylabel("Player")
ax.set_title("Top 10 Fantasy Premier League Players (by Total Points)")
ax.invert_yaxis()  # Flip order so highest is at the top
st.pyplot(fig)
