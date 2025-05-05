"""Application settings and configuration."""

# API Settings
FPL_API_BASE_URL = "https://fantasy.premierleague.com/api"
UNDERSTAT_API_BASE_URL = "https://understat.com"

# Cache Settings
CACHE_TTL = 3600  # 1 hour in seconds

# Feature Flags
ENABLE_PREMIUM_FEATURES = False
ENABLE_AUTHENTICATION = False

# Data Settings
DEFAULT_SEASON = "2023"
DATA_REFRESH_INTERVAL = 24  # hours

# UI Settings
DEFAULT_LAYOUT = "wide"
DEFAULT_PAGE_ICON = "⚽" 