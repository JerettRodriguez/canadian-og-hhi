"""
@author: Jerett
"""
#Measures market concentration among TSX-listed Canadian upstream oil and gas 
#producers using the Herfindahl-Hirschman Index (HHI) from 2023 to 2026.
#Includes scenario analysis for the pending Shell acquisition of ARC Resources.

#Alberta Oil&Gas Herfindahl-Hirschman Index (HHI) Analysis for Consolidation

#Below 1,500 — competitive
#1,500 to 2,500 — moderately concentrated
#Above 2,500 — highly concentrated

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#Function to calc market caps
def grab_market_cap_data(ticker, start_date, end_date):
    t = yf.Ticker(ticker)
    hist = t.history(start=start_date, end=end_date)
    price = hist["Close"]
    shares = t.info.get("sharesOutstanding", None)
    if shares is None:
        print(f"Skipping {ticker} — no shares outstanding data")
        return None
    mktcap = price * shares
    return mktcap

#Function to calc periodic HHIs
def calc_HHI(all_data):
    market_shares = all_data.div(all_data.sum(axis=1), axis=0)
    hhi = (market_shares ** 2).sum(axis=1) * 10000
    return hhi

#Function to define predictive cases of ARC-Shell deal
def build_scenarios(all_data, split_date, project_to):
    # Strip timezone for comparison
    data_stripped = all_data.copy()
    data_stripped.index = data_stripped.index.tz_localize(None)
    
    # Use last known market caps on or before split_date
    base = data_stripped[data_stripped.index <= split_date].iloc[-1]

    # Build future date range
    future_dates = pd.bdate_range(start=split_date, end=project_to)

    # Scenario 1 — ARX exits, removed from calculation
    base_no_arc = base.drop("ARX.TO")
    hhi_deal_closes = ((base_no_arc / base_no_arc.sum()) ** 2).sum() * 10000

    # Scenario 2 — Status quo, ARX stays
    hhi_deal_blocked = ((base / base.sum()) ** 2).sum() * 10000

    # Project as flat lines across future date range
    scenario_closes = pd.Series(hhi_deal_closes, index=future_dates)
    scenario_blocked = pd.Series(hhi_deal_blocked, index=future_dates)

    return scenario_closes, scenario_blocked

# Define acquisition dates
acquisitions = {
    "Suncor / TotalEnergies Fort Hills": "2023-10-04",
    "CNQ / Chevron AOSP": "2024-10-01",
    "Whitecap / Veren": "2024-06-01",
    "Cenovus / MEG": "2025-11-06",
    "Shell / ARC (Announced)": "2026-04-27"
}

#Define Time Periods
start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2026-05-17")
#Define Dates for ARC Case prediction
split_date = pd.Timestamp("2026-04-27")
project_to = pd.Timestamp("2026-12-31")

# Create list of tickers
tickers = [
    # Large Cap
    "CNQ.TO", "CVE.TO", "SU.TO", "IMO.TO", "TOU.TO", "ARX.TO", "WCP.TO",
    # Mid Cap
    "OVV.TO", "SCR.TO", "BTE.TO", "PEY.TO", "TVE.TO", "ATH.TO"]

# Create data frame of market cap data
all_data = pd.DataFrame()
for ticker in tickers:
    result = grab_market_cap_data(ticker, start_date, end_date)
    if result is not None:
        all_data[ticker] = result

#Calculate daily HHI and forward-looking scenarios
hhi = calc_HHI(all_data)
scenario_closes, scenario_blocked = build_scenarios(all_data, split_date, project_to)

#Plot Function
def plot_hhi(hhi, acquisitions, scenario_closes, scenario_blocked, split_date):
    # Style and color palette
    BACKGROUND = '#0f1117'
    PANEL_BG = '#1a1d27'
    HHI_COLOR = '#4fc3f7'
    MA_COLOR = '#ffffff'
    GRID_COLOR = '#2a2d3a'
    ANNOTATION_COLOR = '#b39ddb'
    MODERATE_COLOR = '#4dd0e1'
    HIGH_COLOR = '#7986cb'
    TEXT_COLOR = '#e0e0e0'
    CLOSES_COLOR = '#80cbc4'
    BLOCKED_COLOR = '#a8d8ea'

    # Strip timezone from hhi index for plotting
    hhi_plot = hhi.copy()
    hhi_plot.index = hhi_plot.index.tz_localize(None)

    fig, ax = plt.subplots(figsize=(20, 8))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(PANEL_BG)

    # Raw HHI line
    ax.plot(hhi_plot.index, hhi_plot.values, color=HHI_COLOR, linewidth=1.2,
            alpha=0.7, label='Daily HHI')

    # 60-day moving average
    ax.plot(hhi_plot.rolling(60).mean(), color=MA_COLOR, linewidth=1.5,
            label='60-Day Moving Average')

    # Concentration threshold lines
    ax.axhline(y=1500, color=MODERATE_COLOR, linestyle='--', linewidth=1,
               alpha=0.8, label='Moderate Concentration (1,500)')
    ax.axhline(y=2500, color=HIGH_COLOR, linestyle='--', linewidth=1,
               alpha=0.8, label='High Concentration (2,500)')

    # Shaded zone between thresholds
    ax.axhspan(1500, 2500, alpha=0.04, color=MODERATE_COLOR)

    # Acquisition vertical lines
    heights = [1900, 2050, 1900, 2050, 1900]
    for i, (label, date) in enumerate(acquisitions.items()):
        ax.axvline(x=pd.Timestamp(date), color=ANNOTATION_COLOR,
                   linestyle='--', linewidth=1, alpha=0.7)
        ax.text(pd.Timestamp(date) + pd.Timedelta(days=5), heights[i], label,
                rotation=0, fontsize=9, verticalalignment='bottom',
                color=ANNOTATION_COLOR,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=PANEL_BG,
                          edgecolor=ANNOTATION_COLOR, alpha=0.8))

    # Shaded predictive region
    ax.axvspan(split_date, pd.Timestamp("2026-12-31"),
               alpha=0.06, color='white', label='Forecast Region')

    # Scenario lines
    ax.plot(scenario_closes.index, scenario_closes.values,
            color=CLOSES_COLOR, linewidth=2, linestyle='--',
            label='Scenario 1: Deal Closes (ARC exits TSX)')
    ax.plot(scenario_blocked.index, scenario_blocked.values,
            color=BLOCKED_COLOR, linewidth=2, linestyle='--',
            label='Scenario 2: Deal Blocked (Status Quo)')

    # Scenario end labels
    ax.text(scenario_closes.index[-1] + pd.Timedelta(days=3),
            scenario_closes.iloc[-1], 'Deal Closes',
            color=CLOSES_COLOR, fontsize=9, verticalalignment='center')
    ax.text(scenario_blocked.index[-1] + pd.Timedelta(days=3),
            scenario_blocked.iloc[-1], 'Deal Blocked',
            color=BLOCKED_COLOR, fontsize=9, verticalalignment='center')

    # Titles and labels
    ax.set_title("Canadian Oil & Gas Market Concentration (HHI)\nTSX Large-Cap Upstream Producers — 2023 to 2026 (with Shell/ARC Scenarios)",
                 fontsize=18, color=TEXT_COLOR, fontweight='bold', pad=20)
    ax.set_xlabel("Date", fontsize=11, color=TEXT_COLOR, labelpad=10)
    ax.set_ylabel("HHI (0 – 10,000 Scale)", fontsize=11, color=TEXT_COLOR, labelpad=10)

    # Tick formatting
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)

    # Grid
    ax.grid(color=GRID_COLOR, linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    # Legend
    ax.legend(facecolor=PANEL_BG, edgecolor=GRID_COLOR,
              labelcolor=TEXT_COLOR, fontsize=9, loc='center left')

    # Watermark/source note
    fig.text(0.99, 0.01, 'Data: Yahoo Finance | Analysis: TSX Upstream Peer Group',
             ha='right', fontsize=7, color='#555555', style='italic')

    plt.savefig(r"C:/Users/Jerett/Downloads/hhi_analysis.png",
            dpi=300, bbox_inches='tight', facecolor='#0f1117')

#Create Plot
plot_hhi(hhi, acquisitions, scenario_closes, scenario_blocked, split_date)
