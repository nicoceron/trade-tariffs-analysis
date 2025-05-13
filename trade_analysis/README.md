# Colombia Trade Analysis: Impact of Trump Administration and 2025 Universal Tariffs

This project analyzes the trade patterns between Colombia and its major trading partners (USA and China) before, during, and after both the Trump administration tariffs and the 2025 Universal U.S. Reciprocal Tariff.

## Project Overview

The analysis focuses on understanding how tariff policies affected trade flows between:

- Colombia and the United States
- Colombia and China

The analysis is divided into five time periods:

1. **Pre-tariff period** (Jan 2016 - Feb 2018): Before major Trump tariffs were implemented
2. **Trump tariff period** (Mar 2018 - Jan 2021): During the Trump administration's tariff policies
3. **Post-tariff period** (Jan 2021 - Apr 2025): Between the end of Trump tariffs and the 2025 Universal Tariff
4. **2025 Universal Tariff period** (Apr 2025 - May 2025): During the implementation of the Universal 10% Reciprocal Tariff
5. **Post-2025 agreement period** (May 2025 onwards): After the US-China 90-day tariff reduction agreement

## Repository Structure

```
trade_analysis/
│
├── data/                  # Data files
│   └── trade_data.csv     # Sample/fetched trade data
│
├── notebooks/             # Jupyter notebooks
│   └── trade_analysis.ipynb  # Main analysis notebook
│
├── scripts/               # Python scripts
│   ├── fetch_trade_data.py   # Script to fetch data from APIs
│   └── analyze_trade_data.py # Script to analyze and visualize data
│
├── results/               # Generated visualizations and reports
│   ├── trade_volume_time_series.png
│   ├── trade_balance_time_series.png
│   ├── trade_volume_by_period.png
│   ├── trade_changes_heatmap.png
│   ├── trade_balance_by_period.png
│   ├── trade_relative_changes.png
│   └── trade_analysis_report.html
│
├── run_analysis.py        # Launcher script to run the complete analysis
├── requirements.txt       # Project dependencies
├── SUMMARY.md            # Project summary document
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- requests
- jupyter (for notebooks)

### Installation

1. Clone this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Analysis

1. First, fetch the trade data:

   ```
   python scripts/fetch_trade_data.py
   ```

   This will either:

   - Fetch real data from UN Comtrade API (when uncommented in the code)
   - Generate sample data for demonstration (default)

2. Run the analysis script:

   ```
   python scripts/analyze_trade_data.py
   ```

   This will generate visualizations and an HTML report in the `results/` directory

3. Alternatively, open the Jupyter notebook:

   ```
   jupyter notebook notebooks/trade_analysis.ipynb
   ```

   And run the cells to perform the analysis interactively.

4. Or run the complete pipeline with one command:
   ```
   python run_analysis.py
   ```
   This will fetch data, run the analysis, and open the report in your browser.

## Data Sources

This project can use data from:

- UN Comtrade API: International trade statistics
- World Bank WITS: World Integrated Trade Solution
- DANE (Colombia's National Administrative Department of Statistics)
- US Census Bureau Foreign Trade data

By default, the project generates sample data to demonstrate the analysis workflow. For actual research, uncomment the API calls in the fetch_trade_data.py script and provide appropriate API keys if necessary.

## Analysis Methods

The analysis includes:

1. Time series analysis of trade volumes and trade balances
2. Period-based comparisons of average trade volumes
3. Calculation of percentage changes between different tariff periods
4. Relative change analysis from the pre-tariff baseline
5. Visualization of key trade metrics across time periods

## Key Findings

The analysis reveals how trade patterns shifted during different tariff periods:

### Trump Administration Tariffs (2018-2021)

- Changes in Colombia's exports to and imports from the United States
- Changes in Colombia's exports to and imports from China
- Evidence of possible trade diversion effects
- Post-tariff recovery patterns

### 2025 Universal U.S. Reciprocal Tariff

- Impact of the broader 10% Universal Reciprocal Tariff on Colombia's trade
- Comparison with the more targeted Trump-era tariffs
- Early effects of the US-China 90-day agreement
- Potential long-term implications for Colombia's trade relationships

Detailed findings can be found in the generated HTML report.

## Notes

- This project is designed for educational and research purposes
- The default configuration uses simulated data for demonstration
- For production use, configure the API connections to use real trade statistics
- The 2025 tariff situation is dynamic with multiple phases and temporary agreements
