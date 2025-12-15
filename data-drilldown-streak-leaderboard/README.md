# Lesson Streak Leaderboard

A data analysis project that calculates and ranks user learning streaks from lesson completion data.

## Overview

This project analyzes lesson completion data to identify consecutive day streaks for each user, then generates a leaderboard showing the top 10 users with active streaks. It includes both Python (pandas) and SQL implementations.

## Features

- **Streak Detection**: Identifies consecutive day learning streaks for each user
- **Leaderboard Generation**: Ranks users by their longest active streaks
- **Duplicate Handling**: Removes duplicate lessons completed on the same day
- **Active Streak Filtering**: Shows only streaks that are currently active (as of 2025-09-28)

## Files

- **streak-leaderboard.py**: Python implementation using pandas
- **streak-leaderboard.sql**: SQL implementation for data warehouses
- **LessonStreaks.csv**: Input data containing lesson completion records
- **pyproject.toml**: Project dependencies and configuration

## Data Format

The input CSV file contains the following columns:
- `id`: Record ID
- `lesson_id`: Unique lesson identifier
- `date`: Completion date (YYYY-MM-DD)
- `user_id`: Unique user identifier
- `user_name`: User's display name

## Requirements

- Python >= 3.14
- pandas >= 2.3.3
- polars >= 1.36.1

## Installation

```bash
pip install -e .
```

## Usage

### Python Implementation

```bash
python streak-leaderboard.py
```

The script will:
1. Load and clean the lesson data
2. Calculate streaks for each user
3. Display the top 10 users with active streaks

### SQL Implementation

Execute the SQL query in your preferred SQL database or data warehouse that supports:
- Common Table Expressions (CTEs)
- Window functions (LAG, SUM OVER)
- DATEDIFF function

## How It Works

1. **Data Cleaning**: Remove duplicate lessons completed on the same day by the same user
2. **Streak Calculation**: 
   - Calculate date differences between consecutive lessons
   - Mark streak breaks when days_difference != 1
   - Group consecutive days into streak segments
3. **Aggregation**: For each streak, calculate:
   - Streak length (number of consecutive days)
   - Start date
   - End date
4. **Filtering**: Keep only active streaks (end date >= 2025-09-28)
5. **Ranking**: Sort by streak length and display top 10

## Output

The script outputs a DataFrame with columns:
- `user_id`: User identifier
- `user_name`: User's display name
- `streak`: Streak group identifier
- `streak_length`: Number of consecutive days
- `start_date`: First day of the streak
- `end_date`: Last day of the streak

## Example Output

```
   user_id     user_name  streak  streak_length start_date   end_date
0  12345678    John Doe      5             45  2025-08-14  2025-09-28
1  87654321    Jane Smith    3             42  2025-08-17  2025-09-28
...
```

## License

MIT License
