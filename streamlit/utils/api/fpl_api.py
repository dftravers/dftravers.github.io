import requests
from typing import Dict, Any, Optional

class FPLAPI:
    """Wrapper for the Fantasy Premier League API."""
    
    BASE_URL = "https://fantasy.premierleague.com/api"
    
    @staticmethod
    def get_bootstrap_static() -> Dict[str, Any]:
        """Get the bootstrap static data from the FPL API."""
        url = f"{FPLAPI.BASE_URL}/bootstrap-static/"
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_player_details(player_id: int) -> Dict[str, Any]:
        """Get detailed information for a specific player."""
        url = f"{FPLAPI.BASE_URL}/element-summary/{player_id}/"
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_team_details(team_id: int) -> Dict[str, Any]:
        """Get detailed information for a specific team."""
        url = f"{FPLAPI.BASE_URL}/entry/{team_id}/"
        response = requests.get(url)
        return response.json() 