import requests
from typing import Dict, Any, Optional

class UnderstatAPI:
    """Wrapper for the Understat API."""
    
    BASE_URL = "https://understat.com"
    
    @staticmethod
    def get_player_stats(season: str = "2023") -> Dict[str, Any]:
        """Get player statistics for a specific season."""
        url = f"{UnderstatAPI.BASE_URL}/league/EPL/{season}"
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_team_stats(season: str = "2023") -> Dict[str, Any]:
        """Get team statistics for a specific season."""
        url = f"{UnderstatAPI.BASE_URL}/league/EPL/{season}"
        response = requests.get(url)
        return response.json() 