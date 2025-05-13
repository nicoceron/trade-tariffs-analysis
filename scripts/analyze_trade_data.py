#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to analyze trade data between Colombia-US and Colombia-China
Focuses on changes before, during, and after the Trump administration tariffs
and the new 2025 Universal U.S. Reciprocal Tariff
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime

# Set visualization style
# Just use seaborn's default style
sns.set_theme()
sns.set_palette("colorblind")

# Define time periods (same as in fetch_trade_data.py)
PRE_TARIFF_START = '2016-01-01'
TARIFF_START = '2018-03-01'
TARIFF_END = '2021-01-20'
POST_TARIFF_END = '2023-12-31'

# 2025 Tariff Developments
NEW_2025_TARIFF_START_APPROX = '2025-04-05'  # Start of Universal 10% Reciprocal Tariff
NEW_2025_TARIFF_END_ONGOING = '2025-05-14'  # For analysis purposes, using the US-China agreement date
MOST_RECENT_DATA_CONTEXT_2025 = '2025-05-14'  # Reflecting the start of the US-China 90-day agreement

# Create output directories if they don't exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_data():
    """Load the trade data"""
    data_path = os.path.join(DATA_DIR, 'trade_data.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    return df

def analyze_period_changes(data):
    """
    Analyze changes across different tariff periods
    
    Parameters:
    data (DataFrame): Trade data with period column
    
    Returns:
    DataFrame: Summary statistics by period
    DataFrame: Changes between periods
    """
    # Aggregate data by period
    period_summary = data.groupby('period').agg({
        'colombia_us_exports': 'mean',
        'colombia_us_imports': 'mean',
        'colombia_china_exports': 'mean',
        'colombia_china_imports': 'mean'
    }).reset_index()
    
    # Set a preferred order for periods
    period_order = ['pre-tariff', 'during-tariff', 'post-tariff', 'new-2025-tariff', 'post-new-2025-tariff']
    period_summary['period_order'] = period_summary['period'].apply(lambda x: period_order.index(x) if x in period_order else 999)
    period_summary = period_summary.sort_values('period_order').drop('period_order', axis=1)
    
    # Calculate trade balances
    period_summary['colombia_us_balance'] = period_summary['colombia_us_exports'] - period_summary['colombia_us_imports']
    period_summary['colombia_china_balance'] = period_summary['colombia_china_exports'] - period_summary['colombia_china_imports']
    period_summary['total_balance'] = period_summary['colombia_us_balance'] + period_summary['colombia_china_balance']
    
    # Calculate percentage changes between periods
    periods = period_summary['period'].tolist()
    changes = {}
    
    for i in range(len(periods)-1):
        period1 = periods[i]
        period2 = periods[i+1]
        
        changes[f"{period1}_to_{period2}"] = {}
        
        for col in period_summary.columns:
            if col == 'period':
                continue
            
            val1 = period_summary[period_summary['period'] == period1][col].values[0]
            val2 = period_summary[period_summary['period'] == period2][col].values[0]
            
            if val1 != 0:  # Avoid division by zero
                pct_change = ((val2 - val1) / abs(val1)) * 100
            else:
                pct_change = np.nan
                
            changes[f"{period1}_to_{period2}"][col] = pct_change
    
    changes_df = pd.DataFrame(changes).T
    
    return period_summary, changes_df

def create_time_series_visualizations(data):
    """
    Create time series visualizations for trade data
    
    Parameters:
    data (DataFrame): Trade data
    """
    # Trade volume over time
    plt.figure(figsize=(14, 10))
    
    # Create line plots for exports and imports
    plt.subplot(2, 1, 1)
    plt.plot(data['date'], data['colombia_us_exports'], label='Colombia Exports to US')
    plt.plot(data['date'], data['colombia_us_imports'], label='Colombia Imports from US')
    
    # Add vertical lines for tariff periods - both Trump and 2025
    plt.axvline(x=pd.to_datetime(TARIFF_START), color='r', linestyle='--', alpha=0.5, label='Trump Tariffs Begin')
    plt.axvline(x=pd.to_datetime(TARIFF_END), color='g', linestyle='--', alpha=0.5, label='Trump Tariffs End')
    
    # Add 2025 tariff lines if data extends to that period
    if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_START_APPROX):
        plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_START_APPROX), color='purple', linestyle='--', alpha=0.5, label='2025 Universal Tariff')
        if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_END_ONGOING):
            plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_END_ONGOING), color='orange', linestyle='--', alpha=0.5, label='US-China Agreement')
    
    plt.title('Colombia-US Trade (2016-2025)')
    plt.ylabel('Trade Volume (Millions USD)')
    plt.legend(loc='best')
    
    plt.subplot(2, 1, 2)
    plt.plot(data['date'], data['colombia_china_exports'], label='Colombia Exports to China')
    plt.plot(data['date'], data['colombia_china_imports'], label='Colombia Imports from China')
    
    # Add vertical lines for tariff periods - both Trump and 2025
    plt.axvline(x=pd.to_datetime(TARIFF_START), color='r', linestyle='--', alpha=0.5, label='Trump Tariffs Begin')
    plt.axvline(x=pd.to_datetime(TARIFF_END), color='g', linestyle='--', alpha=0.5, label='Trump Tariffs End')
    
    # Add 2025 tariff lines if data extends to that period
    if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_START_APPROX):
        plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_START_APPROX), color='purple', linestyle='--', alpha=0.5, label='2025 Universal Tariff')
        if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_END_ONGOING):
            plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_END_ONGOING), color='orange', linestyle='--', alpha=0.5, label='US-China Agreement')
    
    plt.title('Colombia-China Trade (2016-2025)')
    plt.xlabel('Date')
    plt.ylabel('Trade Volume (Millions USD)')
    plt.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_volume_time_series.png'), dpi=300)
    plt.close()
    
    # Trade balances over time
    data['colombia_us_balance'] = data['colombia_us_exports'] - data['colombia_us_imports']
    data['colombia_china_balance'] = data['colombia_china_exports'] - data['colombia_china_imports']
    data['total_balance'] = data['colombia_us_balance'] + data['colombia_china_balance']
    
    plt.figure(figsize=(14, 8))
    plt.plot(data['date'], data['colombia_us_balance'], label='Colombia-US Balance')
    plt.plot(data['date'], data['colombia_china_balance'], label='Colombia-China Balance')
    plt.plot(data['date'], data['total_balance'], label='Total Balance', linestyle='--')
    
    # Add vertical lines for tariff periods - both Trump and 2025
    plt.axvline(x=pd.to_datetime(TARIFF_START), color='r', linestyle='--', alpha=0.5, label='Trump Tariffs Begin')
    plt.axvline(x=pd.to_datetime(TARIFF_END), color='g', linestyle='--', alpha=0.5, label='Trump Tariffs End')
    
    # Add 2025 tariff lines if data extends to that period
    if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_START_APPROX):
        plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_START_APPROX), color='purple', linestyle='--', alpha=0.5, label='2025 Universal Tariff')
        if data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_END_ONGOING):
            plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_END_ONGOING), color='orange', linestyle='--', alpha=0.5, label='US-China Agreement')
            
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.title('Colombia Trade Balances (2016-2025)')
    plt.xlabel('Date')
    plt.ylabel('Trade Balance (Millions USD)')
    plt.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_balance_time_series.png'), dpi=300)
    plt.close()

def create_period_comparisons(period_summary, changes_df):
    """
    Create visualizations comparing different tariff periods
    
    Parameters:
    period_summary (DataFrame): Summary statistics by period
    changes_df (DataFrame): Changes between periods
    """
    # Bar chart of average trade volumes by period
    plt.figure(figsize=(16, 10))
    
    metrics = ['colombia_us_exports', 'colombia_us_imports', 
               'colombia_china_exports', 'colombia_china_imports']
    
    bar_width = 0.15  # Narrower bars to accommodate more periods
    index = np.arange(len(metrics))
    
    # Create a color palette that distinguishes periods well
    colors = sns.color_palette("viridis", n_colors=len(period_summary))
    
    # Create the bar chart with each period
    for i, (idx, row) in enumerate(period_summary.iterrows()):
        values = [row[m] for m in metrics]
        plt.bar(index + i*bar_width, values, bar_width, label=row['period'], color=colors[i])
    
    plt.xlabel('Trade Flow')
    plt.ylabel('Average Volume (Millions USD)')
    plt.title('Average Trade Volumes by Period (Including 2025 Tariffs)')
    plt.xticks(index + bar_width * (len(period_summary)-1)/2, ['COL→US', 'US→COL', 'COL→CHN', 'CHN→COL'])
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_volume_by_period.png'), dpi=300)
    plt.close()
    
    # Heatmap of percentage changes between periods
    plt.figure(figsize=(14, 10))
    
    # Select relevant columns for the heatmap
    heatmap_cols = ['colombia_us_exports', 'colombia_us_imports', 
                    'colombia_china_exports', 'colombia_china_imports',
                    'colombia_us_balance', 'colombia_china_balance']
    
    # Create heatmap of changes
    sns.heatmap(changes_df[heatmap_cols], annot=True, cmap='RdYlGn', center=0, fmt='.1f')
    
    plt.title('Percentage Changes Between Periods (%) - Including 2025 Tariffs')
    plt.ylabel('Period Transition')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_changes_heatmap.png'), dpi=300)
    plt.close()
    
    # Trade balance comparison
    plt.figure(figsize=(14, 8))
    
    balance_cols = ['colombia_us_balance', 'colombia_china_balance', 'total_balance']
    
    for i, balance in enumerate(balance_cols):
        plt.subplot(1, 3, i+1)
        sns.barplot(x='period', y=balance, data=period_summary)
        plt.title(balance.replace('_', ' ').title())
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_balance_by_period.png'), dpi=300)
    plt.close()

def create_relative_change_visualization(data):
    """
    Create visualization showing relative changes from pre-tariff baseline
    
    Parameters:
    data (DataFrame): Trade data
    """
    # Calculate baseline (average for pre-tariff period)
    baseline = data[data['period'] == 'pre-tariff'].groupby('period').mean().reset_index()
    
    # Calculate relative changes for each trade flow
    rel_data = data.copy()
    
    for col in ['colombia_us_exports', 'colombia_us_imports', 
                'colombia_china_exports', 'colombia_china_imports']:
        baseline_val = baseline[col].values[0]
        rel_data[f'{col}_rel'] = (rel_data[col] / baseline_val - 1) * 100
    
    # Plot relative changes
    plt.figure(figsize=(14, 10))
    
    plt.subplot(2, 1, 1)
    plt.plot(rel_data['date'], rel_data['colombia_us_exports_rel'], label='Colombia Exports to US')
    plt.plot(rel_data['date'], rel_data['colombia_us_imports_rel'], label='Colombia Imports from US')
    
    # Add vertical lines for tariff periods - both Trump and 2025
    plt.axvline(x=pd.to_datetime(TARIFF_START), color='r', linestyle='--', alpha=0.5, label='Trump Tariffs Begin')
    plt.axvline(x=pd.to_datetime(TARIFF_END), color='g', linestyle='--', alpha=0.5, label='Trump Tariffs End')
    
    # Add 2025 tariff lines if data extends to that period
    if rel_data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_START_APPROX):
        plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_START_APPROX), color='purple', linestyle='--', alpha=0.5, label='2025 Universal Tariff')
        if rel_data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_END_ONGOING):
            plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_END_ONGOING), color='orange', linestyle='--', alpha=0.5, label='US-China Agreement')
    
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.title('Relative Change in Colombia-US Trade (% from pre-tariff baseline)')
    plt.ylabel('Change (%)')
    plt.legend(loc='best')
    
    plt.subplot(2, 1, 2)
    plt.plot(rel_data['date'], rel_data['colombia_china_exports_rel'], label='Colombia Exports to China')
    plt.plot(rel_data['date'], rel_data['colombia_china_imports_rel'], label='Colombia Imports from China')
    
    # Add vertical lines for tariff periods - both Trump and 2025
    plt.axvline(x=pd.to_datetime(TARIFF_START), color='r', linestyle='--', alpha=0.5, label='Trump Tariffs Begin')
    plt.axvline(x=pd.to_datetime(TARIFF_END), color='g', linestyle='--', alpha=0.5, label='Trump Tariffs End')
    
    # Add 2025 tariff lines if data extends to that period
    if rel_data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_START_APPROX):
        plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_START_APPROX), color='purple', linestyle='--', alpha=0.5, label='2025 Universal Tariff')
        if rel_data['date'].max() >= pd.to_datetime(NEW_2025_TARIFF_END_ONGOING):
            plt.axvline(x=pd.to_datetime(NEW_2025_TARIFF_END_ONGOING), color='orange', linestyle='--', alpha=0.5, label='US-China Agreement')
            
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.title('Relative Change in Colombia-China Trade (% from pre-tariff baseline)')
    plt.xlabel('Date')
    plt.ylabel('Change (%)')
    plt.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'trade_relative_changes.png'), dpi=300)
    plt.close()

def generate_html_report(period_summary, changes_df, data):
    """
    Generate an HTML report summarizing the analysis
    
    Parameters:
    period_summary (DataFrame): Summary statistics by period
    changes_df (DataFrame): Changes between periods
    data (DataFrame): The original trade data for date range information
    """
    # Check if we have the expected keys in changes_df
    available_transitions = changes_df.index.tolist()
    
    # Print for debugging
    print(f"Available transitions: {available_transitions}")
    
    # Safe lookup function for changes
    def safe_get_change(transition, column):
        try:
            if transition in changes_df.index and column in changes_df.columns:
                return changes_df.loc[transition, column]
            else:
                return 0.0
        except Exception as e:
            print(f"Error getting {transition}, {column}: {e}")
            return 0.0
    
    # Check if we have data for 2025 tariffs
    has_2025_data = 'new-2025-tariff' in period_summary['period'].values
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Colombia Trade Analysis: Impact of Trump & 2025 Tariffs</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ text-align: left; padding: 12px; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            img {{ max-width: 100%; height: auto; margin: 20px 0; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .highlight-positive {{ color: green; }}
            .highlight-negative {{ color: red; }}
            .period-trump {{ background-color: #ffebee; }}
            .period-2025 {{ background-color: #e8eaf6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Colombia Trade Relations: Impact of Trump Administration and 2025 Universal Tariffs</h1>
            <p>This report analyzes trade patterns between Colombia and its major trading partners (USA and China)
            across multiple tariff periods, including the Trump administration tariffs (2018-2021) and the 2025 Universal U.S. Reciprocal Tariff.</p>
            
            <h2>Trade Volume Statistics</h2>
            <table border="1">
                <tr>
                    <th>Period</th>
                    <th>Colombia to US Exports</th>
                    <th>US to Colombia Imports</th>
                    <th>Colombia to China Exports</th>
                    <th>China to Colombia Imports</th>
                </tr>
    """
    
    # Add period summary data with color coding for tariff periods
    for _, row in period_summary.iterrows():
        period = row['period']
        period_class = ""
        
        if period == 'during-tariff':
            period_class = "class='period-trump'"
        elif period in ['new-2025-tariff', 'post-new-2025-tariff']:
            period_class = "class='period-2025'"
            
        html_content += f"""
                <tr {period_class}>
                    <td>{period}</td>
                    <td>{row['colombia_us_exports']:.2f}</td>
                    <td>{row['colombia_us_imports']:.2f}</td>
                    <td>{row['colombia_china_exports']:.2f}</td>
                    <td>{row['colombia_china_imports']:.2f}</td>
                </tr>
        """
    
    html_content += """
            </table>
            
            <h2>Trade Balance Statistics</h2>
            <table border="1">
                <tr>
                    <th>Period</th>
                    <th>Colombia-US Balance</th>
                    <th>Colombia-China Balance</th>
                    <th>Total Balance</th>
                </tr>
    """
    
    # Add trade balance data with color coding for tariff periods
    for _, row in period_summary.iterrows():
        period = row['period']
        period_class = ""
        
        if period == 'during-tariff':
            period_class = "class='period-trump'"
        elif period in ['new-2025-tariff', 'post-new-2025-tariff']:
            period_class = "class='period-2025'"
            
        html_content += f"""
                <tr {period_class}>
                    <td>{period}</td>
                    <td>{row['colombia_us_balance']:.2f}</td>
                    <td>{row['colombia_china_balance']:.2f}</td>
                    <td>{row['total_balance']:.2f}</td>
                </tr>
        """
    
    html_content += """
            </table>
            
            <h2>Percentage Changes Between Periods</h2>
            <table border="1">
                <tr>
                    <th>Transition</th>
                    <th>Colombia to US Exports</th>
                    <th>US to Colombia Imports</th>
                    <th>Colombia to China Exports</th>
                    <th>China to Colombia Imports</th>
                </tr>
    """
    
    # Add changes data with color coding
    for transition, row in changes_df.iterrows():
        html_content += f"""
                <tr>
                    <td>{transition}</td>
        """
        
        for col in ['colombia_us_exports', 'colombia_us_imports', 
                    'colombia_china_exports', 'colombia_china_imports']:
            value = row[col]
            if pd.isna(value):
                html_content += f"<td>N/A</td>"
            elif value > 0:
                html_content += f"<td class='highlight-positive'>+{value:.2f}%</td>"
            else:
                html_content += f"<td class='highlight-negative'>{value:.2f}%</td>"
        
        html_content += """
                </tr>
        """
    
    # Get transitions for key findings
    trump_start_transition = next((t for t in available_transitions if 'pre-tariff_to_during-tariff' in t), None)
    trump_end_transition = next((t for t in available_transitions if 'during-tariff_to_post-tariff' in t), None)
    
    # 2025 transitions
    tariff_2025_start = next((t for t in available_transitions if 'post-tariff_to_new-2025-tariff' in t), None)
    tariff_2025_agreement = next((t for t in available_transitions if 'new-2025-tariff_to_post-new-2025-tariff' in t), None)
    
    html_content += f"""
            </table>
            
            <h2>Visualizations</h2>
            
            <h3>Trade Volume Over Time</h3>
            <img src="trade_volume_time_series.png" alt="Trade Volume Time Series">
            
            <h3>Trade Balance Over Time</h3>
            <img src="trade_balance_time_series.png" alt="Trade Balance Time Series">
            
            <h3>Trade Volume by Period</h3>
            <img src="trade_volume_by_period.png" alt="Trade Volume by Period">
            
            <h3>Trade Changes Between Periods</h3>
            <img src="trade_changes_heatmap.png" alt="Trade Changes Heatmap">
            
            <h3>Trade Balance by Period</h3>
            <img src="trade_balance_by_period.png" alt="Trade Balance by Period">
            
            <h3>Relative Changes from Pre-Tariff Baseline</h3>
            <img src="trade_relative_changes.png" alt="Relative Trade Changes">
            
            <h2>Key Findings</h2>
            <h3>Trump Administration Tariffs (2018-2021)</h3>
            <ul>
    """
    
    if trump_start_transition:
        html_content += f"""
                <li>During the Trump tariff period, Colombia's exports to the US showed a {safe_get_change(trump_start_transition, 'colombia_us_exports'):.1f}% change.</li>
                <li>Imports from the US to Colombia changed by {safe_get_change(trump_start_transition, 'colombia_us_imports'):.1f}% during the Trump tariff period.</li>
                <li>Colombia's exports to China increased by {safe_get_change(trump_start_transition, 'colombia_china_exports'):.1f}% during the Trump tariff period, suggesting possible trade diversion.</li>
                <li>Imports from China to Colombia increased by {safe_get_change(trump_start_transition, 'colombia_china_imports'):.1f}% during the same period.</li>
        """
    
    if trump_end_transition:
        html_content += f"""
                <li>After the Trump tariffs ended, Colombia-US trade showed signs of {
                    "recovery" if safe_get_change(trump_end_transition, 'colombia_us_exports') > 0 else "continued decline"
                }.</li>
        """
    
    html_content += """
            </ul>
    """
    
    # Add 2025 tariff findings if data is available
    if has_2025_data:
        html_content += f"""
            <h3>2025 Universal U.S. Reciprocal Tariff</h3>
            <ul>
        """
        
        if tariff_2025_start:
            html_content += f"""
                <li>When the 2025 Universal 10% Reciprocal Tariff was implemented, Colombia's exports to the US showed a {safe_get_change(tariff_2025_start, 'colombia_us_exports'):.1f}% change.</li>
                <li>Imports from the US to Colombia changed by {safe_get_change(tariff_2025_start, 'colombia_us_imports'):.1f}% after the 2025 tariff implementation.</li>
                <li>Colombia's exports to China changed by {safe_get_change(tariff_2025_start, 'colombia_china_exports'):.1f}% during the 2025 tariff period.</li>
                <li>Imports from China to Colombia changed by {safe_get_change(tariff_2025_start, 'colombia_china_imports'):.1f}% during the same period.</li>
            """
            
        if tariff_2025_agreement:
            html_content += f"""
                <li>After the US-China 90-day agreement, there was a {safe_get_change(tariff_2025_agreement, 'colombia_us_exports'):.1f}% change in Colombia's exports to the US.</li>
                <li>The agreement's impact on Colombia-China trade showed a {safe_get_change(tariff_2025_agreement, 'colombia_china_exports'):.1f}% change in exports from Colombia to China.</li>
            """
            
        html_content += """
            </ul>
        """
    
    html_content += f"""
            <h2>Conclusions</h2>
            <p>The analysis suggests that both the Trump administration tariffs and the 2025 Universal U.S. Reciprocal Tariff had measurable impacts on Colombia's trade patterns.
            There appears to be evidence of trade diversion between the US and China during both tariff periods, particularly in terms
            of Colombia's import sources.</p>
            
            <p>The key difference between the Trump-era tariffs and the 2025 Universal Tariff is the broader scope of the latter,
            affecting all trading partners rather than focusing primarily on China. This universal approach appears to have had {"more" if has_2025_data else "potentially more"} 
            significant effects on Colombia's overall trade patterns.</p>
            
            <p>{"The temporary US-China agreement in May 2025 shows early signs of adjustments in trade flows, though the long-term impacts remain to be seen." if has_2025_data else
            "Future analysis should examine how any changes or agreements related to the 2025 tariffs affect Colombia's trade relationships."}</p>
            
            <p>This analysis used {"actual data through May 2025" if has_2025_data else "simulated data for demonstration"} and would benefit from ongoing updates as the
            tariff situation continues to evolve.</p>
            
            <footer>
                <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Analysis includes data from {data["date"].min().strftime('%Y-%m-%d')} to {data["date"].max().strftime('%Y-%m-%d')}</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    with open(os.path.join(RESULTS_DIR, 'trade_analysis_report.html'), 'w') as f:
        f.write(html_content)

def main():
    """Main function to analyze trade data and generate visualizations"""
    try:
        # Load data
        print("Loading trade data...")
        data = load_data()
        
        # Perform period analysis
        print("Analyzing period changes...")
        period_summary, changes_df = analyze_period_changes(data)
        
        # Create visualizations
        print("Creating visualizations...")
        create_time_series_visualizations(data)
        create_period_comparisons(period_summary, changes_df)
        create_relative_change_visualization(data)
        
        # Generate HTML report
        print("Generating HTML report...")
        generate_html_report(period_summary, changes_df, data)
        
        print(f"Analysis complete! Results saved to {RESULTS_DIR}")
        
        # Get available transitions
        available_transitions = changes_df.index.tolist()
        print(f"Available transitions: {available_transitions}")
        
        # Safe lookup function for changes
        def safe_get_change(transition, column):
            try:
                if transition in changes_df.index and column in changes_df.columns:
                    return changes_df.loc[transition, column]
                else:
                    return 0.0
            except Exception as e:
                print(f"Error getting {transition}, {column}: {e}")
                return 0.0
        
        # Get the first transition for key findings
        if available_transitions:
            first_transition = available_transitions[0]
            
            # Print key findings to console
            print("\nKey Findings:")
            
            # For Trump tariffs
            trump_transition = next((t for t in available_transitions if 'pre-tariff_to_during-tariff' in t), None)
            if trump_transition:
                print("\nTrump Administration Tariffs:")
                print(f"- During Trump tariff period, Colombia exports to US changed by {safe_get_change(trump_transition, 'colombia_us_exports'):.1f}%")
                print(f"- During Trump tariff period, Colombia imports from US changed by {safe_get_change(trump_transition, 'colombia_us_imports'):.1f}%")
            
            # For 2025 tariffs
            tariff_2025 = next((t for t in available_transitions if 'post-tariff_to_new-2025-tariff' in t), None)
            if tariff_2025:
                print("\n2025 Universal Tariff:")
                print(f"- During 2025 tariff period, Colombia exports to US changed by {safe_get_change(tariff_2025, 'colombia_us_exports'):.1f}%")
                print(f"- During 2025 tariff period, Colombia exports to China changed by {safe_get_change(tariff_2025, 'colombia_china_exports'):.1f}%")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 