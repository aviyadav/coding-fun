# Data Drilldown Movie Metrics

A project to analyze user movie activity using Pandas and Polars. It processes user and activity data to calculate metrics such as started and finished movies, and identifies specific movie watching patterns.

## Prerequisites

-   Python 3.14+
-   Pandas >= 2.3.3
-   Polars >= 1.36.1

## Installation

1.  Clone the repository.
2.  Install dependencies (using `uv` or `pip`):

```powershell
pip install -r requirements.txt
# or if using uv
uv sync
```

## Usage

Run the script to see the analysis results:

```powershell
python movie-metrics-data-drill.py
```

## Features

-   **Data Loading**: Loads user and activity data from CSV files.
-   **Aggregations**: Calculates metrics per user.
-   **Drilldown**: Filters for specific movies (e.g., "Fight Club").
-   **Lazy Evaluation**: Utilizes Polars `LazyFrame` for efficient query execution.
