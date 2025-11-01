#!/usr/bin/env python3
"""
Script to generate a lookup database of SuperBru predictions for all combinations
of home and away xG values from 0.00 to 5.00 (in 0.01 increments).

This script calculates the best SuperBru prediction for each xG combination using
Poisson distribution and Superbru scoring rules. It takes user-inputted home and 
away xG values, runs Poisson distribution analysis to find the highest scoring 
Superbru prediction, and outputs that prediction.

Optimized with numpy vectorization for fast computation.
"""

import json
import numpy as np
from scipy.stats import poisson

# Configuration
OUTPUT_FILE = 'predictions-db.json'
STEP = 0.01  # Increment for xG values
MIN_XG = 0.00
MAX_XG = 5.00
MAX_GOALS = 10  # Maximum goals to consider in calculations

def generate_xg_values():
    """Generate all xG values from MIN_XG to MAX_XG with STEP increments."""
    values = []
    current = MIN_XG
    while current <= MAX_XG:
        values.append(round(current, 2))
        current += STEP
        current = round(current, 2)  # Avoid floating point errors
    return values

def precompute_superbru_points_matrix():
    """
    Pre-compute Superbru points matrix for all prediction vs actual combinations.
    Returns a 4D array: points[pred_home, pred_away, actual_home, actual_away]
    
    Superbru Scoring System:
    - 3.0 points: Exact score prediction
    - 1.5 points: Close prediction (within 1 goal) with correct result
    - 1.0 points: Correct result only (win/draw/loss)
    - 0.0 points: Everything else
    """
    points_matrix = np.zeros((MAX_GOALS + 1, MAX_GOALS + 1, MAX_GOALS + 1, MAX_GOALS + 1), dtype=np.float32)
    
    for pred_home in range(MAX_GOALS + 1):
        for pred_away in range(MAX_GOALS + 1):
            for actual_home in range(MAX_GOALS + 1):
                for actual_away in range(MAX_GOALS + 1):
                    # Exact match: 3.0 points
                    if pred_home == actual_home and pred_away == actual_away:
                        points_matrix[pred_home, pred_away, actual_home, actual_away] = 3.0
                    else:
                        # Determine result (H=home win, A=away win, D=draw)
                        pred_result = 'H' if pred_home > pred_away else ('A' if pred_away > pred_home else 'D')
                        actual_result = 'H' if actual_home > actual_away else ('A' if actual_away > actual_home else 'D')
                        
                        # Close prediction (within 1 goal) with correct result: 1.5 points
                        if (abs(pred_home - actual_home) <= 1 and 
                            abs(pred_away - actual_away) <= 1 and 
                            pred_result == actual_result):
                            points_matrix[pred_home, pred_away, actual_home, actual_away] = 1.5
                        # Correct result only: 1.0 points
                        elif pred_result == actual_result:
                            points_matrix[pred_home, pred_away, actual_home, actual_away] = 1.0
                        # No points
                        else:
                            points_matrix[pred_home, pred_away, actual_home, actual_away] = 0.0
    
    return points_matrix

def calculate_best_prediction_vectorized(home_xg, away_xg, points_matrix):
    """
    Calculate the best Superbru prediction using vectorized Poisson distribution operations.
    Takes home and away xG values, generates probability matrix, and finds optimal prediction.
    """
    # Pre-compute probability matrix for all actual scorelines
    actual_home_range = np.arange(MAX_GOALS + 1)
    actual_away_range = np.arange(MAX_GOALS + 1)
    
    # Probability of each actual scoreline (Poisson)
    prob_home = poisson.pmf(actual_home_range, home_xg)
    prob_away = poisson.pmf(actual_away_range, away_xg)
    
    # Outer product to get probability matrix for all actual combinations
    prob_matrix = np.outer(prob_home, prob_away)  # Shape: (11, 11)
    
    # Calculate expected points for each possible prediction
    best_prediction = None
    best_expected_points = -1.0
    
    for pred_home in range(MAX_GOALS + 1):
        for pred_away in range(MAX_GOALS + 1):
            # Get points for this prediction against all actual results
            points = points_matrix[pred_home, pred_away, :, :]  # Shape: (11, 11)
            
            # Calculate expected points (element-wise multiply and sum)
            expected_points = np.sum(prob_matrix * points)
            
            if expected_points > best_expected_points:
                best_expected_points = expected_points
                best_prediction = f"{pred_home}-{pred_away}"
    
    return best_prediction

def generate_database():
    """Generate the complete lookup database."""
    print("Generating SuperBru prediction database...")
    print(f"Range: {MIN_XG} to {MAX_XG} (step: {STEP})")
    
    xg_values = generate_xg_values()
    total_combinations = len(xg_values) * len(xg_values)
    print(f"Total combinations: {total_combinations:,}")
    print("Pre-computing SuperBru points matrix...")
    
    # Pre-compute the points matrix once (this is expensive but only done once)
    points_matrix = precompute_superbru_points_matrix()
    print("Points matrix pre-computed. Starting database generation...\n")
    
    database = {}
    
    # Generate all combinations
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_combinations, desc="Processing", unit="combo")
    except ImportError:
        print("tqdm not available, progress will be shown periodically")
        progress_bar = None
        combo_count = 0
    
    for home_xg in xg_values:
        for away_xg in xg_values:
            key = f"{home_xg:.2f}_{away_xg:.2f}"
            
            # Calculate best prediction using vectorized approach
            prediction = calculate_best_prediction_vectorized(home_xg, away_xg, points_matrix)
            
            # When xG values are equal, mark it so we can show both directions are equally valid
            if home_xg == away_xg:
                database[key] = f"{prediction}|EQUAL"
            else:
                database[key] = prediction
            
            if progress_bar:
                progress_bar.update(1)
            else:
                combo_count += 1
                if combo_count % 10000 == 0:
                    print(f"Processed {combo_count:,} / {total_combinations:,} combinations...")
    
    if progress_bar:
        progress_bar.close()
    
    # Save to JSON file
    print(f"\nSaving database to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(database, f)
    
    print(f"Database saved! Total entries: {len(database):,}")
    file_size_mb = len(json.dumps(database)) / 1024 / 1024
    print(f"File size: {file_size_mb:.2f} MB")
    
    return database

if __name__ == "__main__":
    try:
        database = generate_database()
        print("\n✓ Done! Database generated successfully.")
        print(f"✓ File saved as: {OUTPUT_FILE}")
        print("\nYou can now use this database in your HTML page for fast lookups.")
    except ImportError as e:
        print(f"\n✗ Error: Missing required library: {e}")
        print("\nPlease install required packages:")
        print("  pip install scipy numpy tqdm")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
