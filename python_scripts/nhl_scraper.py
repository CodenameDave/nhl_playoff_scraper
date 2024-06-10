import requests
import sqlite3


# Function to fetch NHL standings data from the API
def fetch_nhl_standings():
    url = 'https://api-web.nhle.com/v1/standings/now'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve NHL standings data: {response.status_code}")
        return None


# Function to extract team names with clinch indicators
def extract_team_names_with_clinch(standings_data):
    if not standings_data:
        print("No standings data available.")
        return []

    team_names = []
    for record in standings_data.get('standings', []):
        if 'clinchIndicator' in record:
            team_name = record.get('teamName', {}).get('default', 'Unknown Team')
            team_names.append(team_name)

    return team_names


# Function to create a database and insert team names into a table
def save_team_names_to_db(team_names):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('nhl_teams.db')
    cursor = conn.cursor()

    # Create the 'teams' table if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT NOT NULL
    )
    ''')

    # Insert team names into the 'teams' table
    cursor.executemany('INSERT INTO teams (team_name) VALUES (?)', [(name,) for name in team_names])

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print(f"{len(team_names)} team names written to 'nhl_teams.db'.")


# Main function
if __name__ == '__main__':
    standings_data = fetch_nhl_standings()
    team_names = extract_team_names_with_clinch(standings_data)
    save_team_names_to_db(team_names)
