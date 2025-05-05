# High Level Purpose

Build a Streamlit app to help Fantasy Premier League (FPL) managers make better, data-driven decisions.

The app will:
- Centralise key stats (player, team, fixtures)
- Provide weekly player point predictions
- Offer visualisations including of upcoming fixture runs
- Suggest transfers and optimal teams for different time horizons
- Run interactively in-browser for ease of use

# Different Pages in the Web app

Dashboard
- This gives a summary and preview of all the key tools.
- It also has information to hook people in, such as 'Last updated', 'Next GW deadline'

Player Database
- This shows all the players in the league along with key stats.
- These include name, position, price, goals, assists, expected goals, expected assists, yellow cards, red cards, minutes, and all of these per 90 too.

Point Prediction Model
- This creates a predicted points score for each player in the league for each week.
- It uses historical data and upcoming fixture difficulties to calculate this.
- There is a toggle for 'Assume 90 minutes' and 'Assume average minutes'.

Fixture Planner
- This shows an interactive widget with all 20 clubs in one column and their upcoming fixtures for the next k gameweeks in that row.
- This k value can be toggled.
- The entries of the fixtures should be colour coded according to fixture difficulty rating metrics called ASM and DWM which I designed.
- When a k value is chosen, this table shown be displayed along with a ranking of which teams have the easiest to hardest runs.

Transfer Suggester
- This tool suggests a transfer to a player's team by pulling their last GW squad using an API key.
- It then looks ahead to whatever number of weeks the user requests and suggests which transfer would be optimal.

Optimal Team Creator
- This creates the optimal team for three different options: weak bench, medium bench and strong bench quality.
- It uses the recursive knapsack algorithm on the time horizon of the player's request.
- The code for this algorithm has been created elsewhere.

# Data Sources

The data comes from the official FPL website API and the Understat API.

# Infrastructure: What's stored where? What runs what?

Eventually, I want the web app to have a log-in function and payment function for a premium version.
I also want the API data to be scraped everyday at midnight so its always updated for users.

For logins: Use streamlit-authenticator

For payments: Use Stripe

For secrets: Store in Gitbut now, AWS Secrets later

Free users can be limited from using premium features with simple checks
