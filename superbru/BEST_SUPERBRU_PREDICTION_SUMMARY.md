# Best Superbru Prediction Algorithm

## Overview
The algorithm calculates the optimal football score prediction for Superbru points using Poisson probability distributions.

## The Function

The core function takes user-inputted home and away expected goals (xG) values and returns the best Superbru prediction:

```python
def calculate_best_prediction(home_xg, away_xg):
    """
    Calculate the best SuperBru prediction using Poisson distribution.
    
    Args:
        home_xg: Expected goals for home team (0.00 to 5.00)
        away_xg: Expected goals for away team (0.00 to 5.00)
    
    Returns:
        String prediction in format "home-away" (e.g., "2-1")
    """
    max_goals = 10
    points_matrix = precompute_superbru_points_matrix()
    
    # Pre-compute probability matrix for all actual scorelines
    actual_home_range = np.arange(max_goals + 1)
    actual_away_range = np.arange(max_goals + 1)
    
    # Probability of each actual scoreline (Poisson)
    prob_home = poisson.pmf(actual_home_range, home_xg)
    prob_away = poisson.pmf(actual_away_range, away_xg)
    
    # Outer product to get probability matrix for all actual combinations
    prob_matrix = np.outer(prob_home, prob_away)
    
    # Calculate expected points for each possible prediction
    best_prediction = None
    best_expected_points = -1.0
    
    for pred_home in range(max_goals + 1):
        for pred_away in range(max_goals + 1):
            # Get points for this prediction against all actual results
            points = points_matrix[pred_home, pred_away, :, :]
            
            # Calculate expected points (element-wise multiply and sum)
            expected_points = np.sum(prob_matrix * points)
            
            if expected_points > best_expected_points:
                best_expected_points = expected_points
                best_prediction = f"{pred_home}-{pred_away}"
    
    return best_prediction
```

## Superbru Scoring System

The scoring system determines points awarded for predictions:

- **3.0 points**: Exact score prediction
- **1.5 points**: Close prediction (within 1 goal) with correct result
- **1.0 points**: Correct result only (win/draw/loss)
- **0.0 points**: Everything else

## How It Works

1. **Input**: User provides home xG and away xG values
2. **Probability Generation**: Uses Poisson distribution to calculate probability of all possible scorelines (0-0 through 10-10)
3. **Expected Value Calculation**: For each possible prediction, calculates expected Superbru points across all outcomes
4. **Optimization**: Selects the prediction with the highest expected value
5. **Output**: Returns the best prediction (e.g., "2-1")

The algorithm evaluates all possible predictions against all possible outcomes to find the optimal choice for maximum expected Superbru points.
