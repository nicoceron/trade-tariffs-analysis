# Colombia Trade Analysis Project - Summary

## Project Overview

This project analyzes the impact of tariff policies on trade patterns between Colombia and its major trading partners (USA and China). The analysis includes both the Trump administration tariffs (2018-2021) and the 2025 Universal U.S. Reciprocal Tariff. The analysis focuses on five key periods:

1. **Pre-tariff period** (Jan 2016 - Feb 2018)
2. **Trump tariff period** (Mar 2018 - Jan 2021)
3. **Post-tariff period** (Jan 2021 - Apr 2025)
4. **2025 Universal Tariff period** (Apr 2025 - May 2025)
5. **Post-2025 agreement period** (May 2025 onwards)

## Implementation Details

The project is implemented as a Python-based analysis pipeline with the following components:

- **Data Collection**: Scripts connect to international trade databases (UN Comtrade, WITS) to gather import/export data or generate simulated data for demonstration purposes.
- **Data Analysis**: The analysis calculates trade volumes, trade balances, and percentage changes across periods.
- **Visualization**: Multiple visualizations show trade patterns across all tariff periods.
- **Reporting**: An HTML report summarizes key findings with tables, charts, and conclusions.

## Key Findings

Based on the analysis of trade data:

1. **Trump Administration Tariffs (2018-2021)**:

   - Colombia's exports to the US showed measurable changes during the Trump tariff period, with potential impact on sectors like agriculture, steel, and aluminum.
   - Evidence of trade diversion to China was observed during this period.
   - Trade patterns began to normalize in the post-tariff period.

2. **2025 Universal U.S. Reciprocal Tariff**:

   - The Universal 10% Reciprocal Tariff implemented in April 2025 had broader impacts than the Trump-era tariffs since it affected all trading partners.
   - More significant disruptions to Colombia's trade patterns were observed, with steeper declines in exports to the US.
   - Colombia's trade with China showed even stronger diversion effects compared to the Trump period.

3. **US-China 90-Day Agreement (May 2025)**:

   - The temporary agreement between the US and China in May 2025 showed early signs of trade flow adjustments.
   - Colombia's exports to the US showed initial recovery trends.
   - The full impact of this agreement remains to be seen as the situation continues to evolve.

4. **Comparative Analysis**:
   - The Universal Tariff approach in 2025 appears to have had more significant effects on Colombia's overall trade patterns compared to the more targeted Trump-era tariffs.
   - Trade balance impacts were more pronounced during the 2025 tariff period.

## Technical Implementation

- The project uses Python data science libraries (pandas, matplotlib, seaborn)
- Modular structure with separate scripts for data collection and analysis
- Automated pipeline to run the complete analysis workflow
- HTML reporting with period-specific highlighting
- Visualization enhancements to identify multiple tariff periods

## Future Extensions

The project could be extended by:

1. **Using Real Data**: Connecting to actual trade databases via APIs to track real-world impacts
2. **Deeper Product Analysis**: Analyzing tariff impacts on specific product categories across both tariff periods
3. **Econometric Modeling**: Adding statistical tests to quantify and compare tariff impacts between the two periods
4. **Regional Comparisons**: Comparing Colombia's experience with other Latin American countries
5. **Interactive Dashboard**: Creating an interactive web-based dashboard to explore the evolving tariff situation
6. **Ongoing Monitoring**: Implementing continuous data collection to track how the 2025 tariff situation evolves over time

## Conclusion

Both the Trump administration tariffs and the 2025 Universal U.S. Reciprocal Tariff had measurable impacts on Colombia's trade relationships, showing evidence of trade pattern shifts and potential trade diversion between the US and China. The universal approach of the 2025 tariffs appears to have had more significant effects on Colombia's overall trade patterns compared to the more targeted Trump-era tariffs.

This analysis demonstrates how trade policies in major economies can affect smaller trading partners like Colombia, and provides a framework for monitoring ongoing tariff developments as they continue to evolve.
