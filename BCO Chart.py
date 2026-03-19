import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Brent Crude Oil Analysis", layout="wide")

st.title("🪖Iran vs USA & Israel: Impact on Brent Crude Oil")
st.subheader("28 February 2026 → 19 March 2026")

# ---------------- DATA ----------------
data = [
    ["28 Feb", "Conflict risk rises", 70.89, 2.45, "Geopolitical tensions rising"],
    ["01 Mar", "Hormuz disruption begins", 78.22, 6.82, "Shipping route threatened"],
    ["02 Mar", "Strikes escalate", 77.74, 7.26, "Military escalation risk"],
    ["03 Mar", "Hormuz effectively closes", 81.40, 4.71, "Supply route blocked"],
    ["04 Mar", "Supply fears persist", 81.40, 0.00, "Market holding position"],
    ["05 Mar", "Shipping disrupted", 85.41, 4.93, "Transport capacity reduced"],
    ["06 Mar", "Severe supply shock", 92.69, 8.52, "Major supply disruption"],
    ["07 Mar", "Stabilization", 92.86, 0.00, "No new escalation"],
    ["08 Mar", "Major disruption warning", 105.15, 13.23, "Severe shortage fears"],
    ["09 Mar", "Conflict intensifies", 98.96, 6.76, "Volatility after spike"],
    ["10 Mar", "De-escalation hopes", 87.80, -11.28, "Possible reopening optimism"],
    ["11 Mar", "Supply still tight", 91.98, 4.76, "Demand outweighs supply"],
    ["12 Mar", "Hormuz stays closed", 100.46, 9.22, "Confirmed closure"],
    ["13 Mar", "Ongoing disruptions", 103.14, 2.67, "Continued tension"],
    ["14 Mar", "No oil infrastructure hit", 101.16, 0.00, "Limited escalation"],
    ["15 Mar", "Talks to reopen Hormuz", 100.80, -0.36, "Diplomatic optimism"],
    ["16 Mar", "Some ships pass", 100.21, -2.84, "Partial relief"],
    ["17 Mar", "Tensions persist", 103.42, 3.20, "Ongoing conflict"],
    ["18 Mar", "Gas field attacked", 107.38, 3.83, "Energy infrastructure hit"],
    ["19 Mar", "Major escalation", 115.52, 7.58, "Widespread supply risk"]
]

df = pd.DataFrame(data, columns=["Date", "Event", "Price", "Change %", "Reason"])

# Create numeric version (FOR LOGIC + CHART)
df["Change_numeric"] = df["Change %"].astype(float)

# Create formatted version (FOR DISPLAY ONLY)
df["Change %"] = df["Change_numeric"].apply(lambda x: f"{x:+.2f}%")

# ---------------- METRICS ----------------
st.markdown("## Key Metrics")

highest = df['Price'].max()
lowest = df['Price'].min()
average = round(df['Price'].mean(), 2)

col1, col2, col3 = st.columns(3)

# GREEN GLOW (Highest)
col1.markdown(f"""
<div style="
    padding: 20px;
    border-radius: 15px;
    background-color: #0f1f0f;
    text-align: center;
    box-shadow: 0 0 15px #00ff00;
">
    <h4 style="color: white;">Highest Price</h4>
    <h2 style="color: #00ff00;">${highest}</h2>
</div>
""", unsafe_allow_html=True)

# RED GLOW (Lowest)
col2.markdown(f"""
<div style="
    padding: 20px;
    border-radius: 15px;
    background-color: #1f0f0f;
    text-align: center;
    box-shadow: 0 0 15px #ff0000;
">
    <h4 style="color: white;">Lowest Price</h4>
    <h2 style="color: #ff4d4d;">${lowest}</h2>
</div>
""", unsafe_allow_html=True)

# NORMAL (Average)
col3.markdown(f"""
<div style="
    padding: 20px;
    border-radius: 15px;
    background-color: #111;
    text-align: center;
">
    <h4 style="color: white;">Average Price</h4>
    <h2 style="color: #ccc;">${average}</h2>
</div>
""", unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown("## Full Data Table")

styled_df = df.style.set_properties(
    subset=["Price", "Change %"],
    **{"text-align": "center"}
)

st.dataframe(
    df.drop(columns=["Change_numeric"]),
    use_container_width=True
)

# ---------------- INTERACTIVE CHART ----------------
st.markdown("## Brent Crude Oil Price Trend")

fig = px.line(
    df,
    x="Date",
    y="Price",
    title="Brent Crude Oil Prices Over Time",
    markers=True,
    hover_data=["Event", "Reason", "Change %"]
)

fig.update_traces(
    line=dict(color="#00D4FF", width=3),
    marker=dict(size=8)
)

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price ($/Barrel)"
)

fig.update_layout(annotations=[])

for i in range(len(df)):
    change = df["Change_numeric"].iloc[i]

    if change > 7 or change < -7:

        color = "#00FFAA" if change > 0 else "#FF4B4B"

        fig.add_annotation(
            x=df["Date"].iloc[i],
            y=df["Price"].iloc[i],

            # CLEAN label
            text=f"{df['Change %'].iloc[i]}",

            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=color,

            ax=0,
            ay=-80 if change > 0 else 80,

            bgcolor="rgba(0,0,0,0.6)",
            bordercolor=color,
            borderwidth=1,
            font=dict(size=12, color="white"),

            align="center"
        )

# ---------------- SHOW CHART ----------------
st.plotly_chart(fig, use_container_width=True)

# ---------------- DESCRIPTION ----------------
st.markdown("## What is Crude Oil?")
st.write("""
Crude oil is a naturally occurring liquid fossil fuel composed of hydrocarbons.
It is refined into fuels like petrol, diesel, jet fuel, and used in plastics, chemicals, and more.
Brent Crude Oil is the global benchmark used to price oil internationally.
""")

# ---------------- SPECS ----------------
st.markdown("## Crude Oil Specifications")
st.write("""
- Benchmark: Brent Crude
- Unit: Barrels (1 barrel = 159 liters)
- Pricing: USD ($)/barrel
- Type: Light Sweet Crude
- Sulfur Content: Low
- Global Influence: High - used Worldwide
""")

# ---------------- CONVERSION ----------------
st.markdown("## Conversion")
usd_to_zar = 18.5  # approximate
df["Price (ZAR)"] = df["Price"] * usd_to_zar
st.write("Approximate USD → ZAR conversion rate: $1 = R18.5")
st.dataframe(df[["Date", "Price", "Price (ZAR)"]])

# ---------------- GEOPOLITICAL COMMENTS ----------------
st.markdown("## Geopolitical Influence (Key Quotes)")

st.write("""
- Trump: "No ship is allowed to pass the Strait of Hormuz" → Supply shock → Prices ↑  
- Iran IRGC: "We will target ships" → Fear → Prices ↑ (Increased)  
- Trump: "War could end soon" → Relief → Prices ↓  
- Powell: "We will wait and see" → Uncertainty → Prices ↑  
- Iran: "Energy facilities are targets" → Major escalation → Prices ↑↑  
""")

# ---------------- DAILY SUMMARY ----------------
st.markdown("## Daily Market Summary")

for i in range(len(df)):
    st.write(f"**{df['Date'][i]}** → {df['Event'][i]} | Price: ${df['Price'][i]} | Change: {df['Change %'][i]}%")

# ---------------- FINAL SUMMARY ----------------
st.markdown("## Final Analysis")

st.write("""
- The dominant driver of price increases was supply disruption via the Strait of Hormuz.
- Any threat or closure caused immediate spikes.
- Temporary declines occurred only when:
  - De-escalation was suggested
  - Ships resumed partial movement
- The largest spikes were tied to:
  - Direct attacks on infrastructure
  - Explicit military threats
- The market remained highly sensitive to geopolitical statements.
""")