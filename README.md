# Canadian Oil & Gas Market Concentration — HHI Analysis

A Python-based analysis of market concentration among TSX-listed Canadian upstream 
oil and gas producers from 2023 to 2026, using the Herfindahl-Hirschman Index (HHI).
Built by an O&G engineer who spent too much time studying for the CFA and decided to 
do something useful with it.

---

## What is the HHI?

The Herfindahl-Hirschman Index (HHI) measures market concentration by summing the 
squared market shares of all firms in a market. It ranges from 0 (perfect competition) 
to 10,000 (pure monopoly).

| HHI Range | Market Structure |
|---|---|
| Below 1,500 | Competitive |
| 1,500 – 2,500 | Moderately Concentrated |
| Above 2,500 | Highly Concentrated |

Regulators like the Canadian Competition Bureau use HHI thresholds when reviewing 
proposed mergers — so this isn't just an academic exercise.

---

## Why Canadian O&G?

Because if you've been paying attention to the Calgary energy patch lately, you'll 
have noticed it's been a busy few years. Billions of dollars in deals, majors gobbling 
up assets, and now a foreign supermajor reaching into the Montney. This project 
attempts to quantify what that consolidation actually looks like using publicly 
available market data.

---

## Peer Group

Analysis covers 13 TSX-listed large and mid-cap upstream producers:

**Large Cap**
- Canadian Natural Resources (CNQ.TO)
- Cenovus Energy (CVE.TO)
- Suncor Energy (SU.TO)
- Imperial Oil (IMO.TO)
- Tourmaline Oil (TOU.TO)
- ARC Resources (ARX.TO)
- Whitecap Resources (WCP.TO)

**Mid Cap**
- Ovintiv (OVV.TO)
- Strathcona Resources (SCR.TO)
- Baytex Energy (BTE.TO)
- Peyto Exploration (PEY.TO)
- Tamarack Valley (TVE.TO)
- Athabasca Oil (ATH.TO)

---

## Key Deals Captured

| Date | Deal |
|---|---|
| October 2023 | Suncor acquires TotalEnergies' Fort Hills stake ($1.47B) |
| June 2024 | Whitecap acquires Veren (formerly Crescent Point) |
| October 2024 | CNQ acquires Chevron Canada AOSP assets ($8.8B USD) |
| November 2025 | Cenovus acquires MEG Energy |
| April 2026 | Shell announces acquisition of ARC Resources ($13.6B USD) — pending |

---

## Methodology & Assumptions

- **Market share metric:** Daily market capitalization (share price × shares outstanding) 
sourced from Yahoo Finance via the `yfinance` library
- **Why not production data?** BOE/day is the more analytically pure measure of market 
share in upstream O&G, but is not available through automated public APIs at the company 
level. Market cap is used as a practical proxy with the caveat that it reflects investor 
sentiment alongside operational scale
- **Peer group scope:** Limited to TSX-listed public companies. Private producers and 
foreign-owned subsidiaries are excluded due to data unavailability — this means the 
model understates true market concentration
- **Delisted companies:** MEG Energy and Veren were excluded post-acquisition as 
Yahoo Finance does not retain historical data for delisted tickers. Their market share 
is implicitly captured through the acquiring companies' market cap growth
- **Smoothing:** A 60-day moving average is applied to reduce daily noise and highlight 
the underlying concentration trend

---

## Forward-Looking Scenario Analysis

The pending Shell/ARC deal (announced April 27, 2026) is modeled under two scenarios 
projected to December 2026:

- **Scenario 1 — Deal Closes:** ARC Resources exits the TSX peer group entirely, 
absorbed by a foreign supermajor. Remaining Canadian independents hold a larger 
relative share of a smaller peer group
- **Scenario 2 — Deal Blocked:** Competition Bureau intervenes, ARC remains 
independent, HHI holds at current levels

---

## Output Charts

**Canadian O&G HHI — 2023 to 2026 with Shell/ARC Scenario Analysis**
Daily HHI and 60-day moving average with major acquisition event markers and 
forward-looking scenario projections for the pending Shell/ARC deal to December 2026.

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/canadian-og-hhi.git
cd canadian-og-hhi
```

**2. Install dependencies**
```bash
pip install yfinance pandas matplotlib
```

**3. Run the analysis**
```bash
python hhi_analysis.py
```

Charts will save automatically to your Downloads folder.

---

## Dependencies

- `yfinance` — market data
- `pandas` — data manipulation
- `matplotlib` — visualization

---

## Author

**Jerett Rodriguez** — UAlberta Engineering grad 
[LinkedIn](https://www.linkedin.com/in/jerett-rodriguez-6b8119208/)

---

*This project is for educational and portfolio purposes. Nothing here constitutes 
financial or investment advice.*
