# SuperBru Prediction Database Generator

This directory contains the SuperBru prediction tool that allows you to look up the best SuperBru prediction for any combination of home and away xG values.

## Setup

1. Install required dependencies:
```bash
pip install scipy numpy tqdm
```

Or install from the main requirements.txt:
```bash
pip install -r ../requirements.txt
```

## Generating the Database

To generate the lookup database containing all possible xG combinations:

```bash
cd superbru
python generate_database.py
```

This will:
- Generate predictions for all combinations of xG from 0.00 to 5.00 (in 0.01 increments)
- Calculate the best SuperBru prediction for each combination using Poisson distribution
- Save the results to `predictions-db.json`

**Note:** This process will generate ~250,000 combinations (501 x 501). With optimizations, this should complete in a few minutes.

## How It Works

The script:
1. Uses Poisson distribution to model the probability of different scorelines given xG values
2. Calculates expected SuperBru points for each possible prediction (0-0 through 10-10)
3. Selects the prediction with the highest expected points
4. Stores results in a JSON lookup table for fast client-side queries

The SuperBru scoring system used (based on BEST_SUPERBRU_PREDICTION_SUMMARY.md):
- Exact match: 3.0 points
- Close prediction (within 1 goal) with correct result: 1.5 points
- Correct result only: 1.0 point
- Otherwise: 0.0 points

## Using the Database

Once `predictions-db.json` is generated, the HTML page (`index.html`) will automatically load it and provide instant lookups. Users can simply enter home and away xG values (0.00 to 5.00) and get the optimal prediction immediately.

