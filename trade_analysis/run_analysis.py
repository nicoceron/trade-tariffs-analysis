#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Launcher script that runs the entire trade analysis pipeline:
1. Fetches/generates trade data including the 2025 Universal U.S. Reciprocal Tariff
2. Performs analysis across all tariff periods (Trump and 2025)
3. Generates HTML report and visualizations
"""

import os
import sys
import subprocess
import time

def main():
    """Run the complete analysis pipeline"""
    print("============================================================")
    print("Colombia Trade Analysis: Trump and 2025 Universal Tariffs")
    print("============================================================")
    print("Analyzing trade patterns across multiple tariff periods:")
    print("- Pre-tariff period (Jan 2016 - Feb 2018)")
    print("- Trump tariff period (Mar 2018 - Jan 2021)")
    print("- Post-tariff period (Jan 2021 - Apr 2025)")
    print("- 2025 Universal Tariff period (Apr 2025 - May 2025)")
    print("- Post-2025 agreement period (May 2025 onwards)")
    print("============================================================")
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Step 1: Fetch/generate trade data
    print("\n[Step 1] Fetching trade data (through May 2025)...")
    fetch_script = os.path.join(base_dir, 'scripts', 'fetch_trade_data.py')
    result = subprocess.run([sys.executable, fetch_script], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error fetching trade data:")
        print(result.stderr)
        return 1
    
    print(result.stdout)
    print("✓ Trade data fetched successfully")
    
    # Step 2: Run analysis and generate report
    print("\n[Step 2] Analyzing trade patterns across all tariff periods...")
    analyze_script = os.path.join(base_dir, 'scripts', 'analyze_trade_data.py')
    result = subprocess.run([sys.executable, analyze_script], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error during analysis:")
        print(result.stderr)
        return 1
    
    print(result.stdout)
    print("✓ Analysis completed successfully")
    
    # Step 3: Display results location
    results_dir = os.path.join(base_dir, 'results')
    report_path = os.path.join(results_dir, 'trade_analysis_report.html')
    
    if os.path.exists(report_path):
        print(f"\n[Step 3] Analysis report generated at: {report_path}")
        print("\nThe report includes comparative analysis between:")
        print("- Trump administration tariffs (2018-2021)")
        print("- 2025 Universal U.S. Reciprocal Tariff")
        print("- US-China 90-day agreement (May 2025)")
        
        # Try to open the report in the default browser
        print("\nAttempting to open the report in your default browser...")
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', report_path])
            elif sys.platform == 'win32':  # Windows
                os.startfile(report_path)
            elif sys.platform == 'linux':  # Linux
                subprocess.run(['xdg-open', report_path])
            
            print("Report opened in browser.")
        except Exception as e:
            print(f"Could not open automatically: {e}")
            print(f"Please open {report_path} manually.")
    else:
        print("Report file not found. Check for errors in the analysis step.")
    
    print("\n============================================================")
    print("Analysis pipeline completed!")
    print("The analysis compares the impacts of both the Trump-era and 2025 tariffs")
    print("on Colombia's trade relationships with the US and China.")
    print("============================================================")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 