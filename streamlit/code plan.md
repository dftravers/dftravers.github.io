# FPL Analytics Dashboard - Code Structure

## Directory Structure

```
streamlit/
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (gitignored)
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
│
├── components/          # Reusable UI components
│   ├── __init__.py
│   ├── header.py       # Header component with title and description
│   ├── footer.py       # Footer component
│   ├── cards.py        # Feature cards component
│   └── deadline.py     # Deadline display component
│
├── pages/              # Streamlit pages
│   ├── 1_Player_Database.py
│   ├── 2_Point_Predictions.py
│   ├── 3_Fixture_Planner.py
│   ├── 4_Transfer_Suggester.py
│   └── 5_Optimal_Team.py
│
├── utils/              # Utility functions and helpers
│   ├── __init__.py
│   ├── api/           # API related utilities
│   │   ├── __init__.py
│   │   ├── fpl_api.py    # FPL API wrapper
│   │   └── understat_api.py  # Understat API wrapper
│   ├── auth/          # Authentication utilities
│   │   ├── __init__.py
│   │   └── auth.py    # Login and authentication logic
│   ├── data/          # Data processing utilities
│   │   ├── __init__.py
│   │   ├── processors.py  # Data processing functions
│   │   └── validators.py  # Data validation functions
│   └── models/        # Prediction models
│       ├── __init__.py
│       └── point_predictor.py  # Points prediction model
│
├── data/              # Data storage and caching
│   ├── raw/          # Raw data from APIs
│   ├── processed/    # Processed data ready for use
│   └── cache/        # Cached data for faster access
│
└── config/           # Configuration files
    ├── __init__.py
    ├── settings.py   # Application settings
    └── constants.py  # Constants and enums
```

## Key Components

### 1. Main Application (app.py)
- Entry point for the Streamlit application
- Page configuration and layout
- Navigation setup
- Global state management

### 2. Components
- Reusable UI components
- Each component should be self-contained
- Include proper documentation and type hints
- Follow consistent styling

### 3. Pages
- Each page should be focused on a specific feature
- Follow consistent naming convention (number_prefix_name.py)
- Include proper documentation
- Handle its own state management

### 4. Utils
- API wrappers for FPL and Understat
- Authentication and user management
- Data processing and validation
- Prediction models and algorithms

### 5. Data Management
- Raw data storage from APIs
- Processed data for application use
- Caching mechanism for performance
- Data validation and cleaning

### 6. Configuration
- Application settings
- Constants and enums
- Environment variables
- Feature flags

## Best Practices

1. **Code Organization**
   - Keep related code together
   - Use clear, descriptive names
   - Follow Python naming conventions
   - Include proper documentation

2. **State Management**
   - Use Streamlit's session state for global state
   - Keep state management simple and predictable
   - Document state dependencies

3. **Error Handling**
   - Implement proper error handling
   - Use custom exceptions where appropriate
   - Log errors for debugging

4. **Performance**
   - Use caching for expensive operations
   - Optimize data loading and processing
   - Implement lazy loading where appropriate

5. **Security**
   - Keep sensitive data in environment variables
   - Implement proper authentication
   - Validate user input
   - Use secure API calls

6. **Testing**
   - Write unit tests for critical functions
   - Include integration tests
   - Document test cases

## Next Steps

1. Set up the basic directory structure
2. Create necessary __init__.py files
3. Move existing code into appropriate locations
4. Set up configuration files
5. Implement authentication system
6. Create reusable components
7. Develop individual pages
8. Set up data processing pipeline
9. Implement caching mechanism
10. Add documentation and tests
