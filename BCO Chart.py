import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

* {
    font-family: 'Montserrat', sans-serif !important;
}
h1, h2, h3 {
    font-weight: 600;
}
p, span, div {
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

st.title("Closure of Strait of Hormuz: Impact on Brent Crude")
st.subheader("28 February to Present")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("BCO_Geopolitical_Tracker.xlsx", sheet_name="Daily Log", header=2)

# Clean column names
df.columns = df.columns.str.strip()

# ---------------- FORMAT DATA ----------------
df["Change_numeric"] = df["Change (%)"].astype(float)
df["Change (%)"] = df["Change_numeric"].apply(lambda x: f"{x:+.2f}%")

# ---------------- CHART (TOP PRIORITY) ----------------
st.markdown("## Brent Crude Oil Price Trend")

fig = px.line(
    df,
    x="Date",
    y="Price",
    title="Brent Crude Oil Prices Over Time",
    markers=True,
    hover_data=[
        "Headline Event",
        "Impact",
        "Event Category",
        "Key Actors",
        "Supply Impact (mb/d net)",
        "OPEC/IEA/Policy Response",
        "Price Mechanism",
        "Day-on-Day Narrative",
        "Key Quote",
        "Change (%)"
    ]
)

fig.update_traces(
    line=dict(color="#13008D", width=3),
    marker=dict(size=8),
    hoverlabel=dict(
        font=dict(
            family="Montserrat, sans-serif",
            size=12
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price ($/Barrel)",
    font=dict(
        family="Montserrat, sans-serif",
        size=12,
        color="white"
    ),
    title_font=dict(
        family="Montserrat, sans-serif",
        size=18
    ),
    legend=dict(
        font=dict(family="Montserrat, sans-serif")
    )
)

# Clear default annotations
fig.update_layout(annotations=[])

# ---------------- SMART CALLOUTS ----------------
for i in range(len(df)):
    change = df["Change_numeric"].iloc[i]

    if change > 5 or change < -5:

        color = "#00FFAA" if change > 0 else "#FF4B4B"

        fig.add_annotation(
            x=df["Date"].iloc[i],
            y=df["Price"].iloc[i],

            text=f"{df['Change (%)'].iloc[i]}<br>{str(df['Key Quote'].iloc[i])[:60]}...",

            showarrow=True,
            arrowhead=2,
            arrowcolor=color,

            ax=0,
            ay=-100 if change > 0 else 100,

            bgcolor="rgba(0,0,0,0.7)",
            bordercolor=color,
            borderwidth=1,

            font=dict(family="Montserrat, sans-serif", size=11, color="white"),
            align="center"
        )

# SHOW CHART
st.plotly_chart(fig, use_container_width=True)

# ---------------- METRICS ----------------
st.markdown("## Key Metrics")

highest = df['Price'].max()
lowest = df['Price'].min()
average = round(df['Price'].mean(), 2)

col1, col2, col3 = st.columns(3)

# Highest (Green Glow)
col1.markdown(f"""
<div style="padding:20px;border-radius:15px;background-color:#0f1f0f;text-align:center;box-shadow:0 0 15px #00ff00;">
<h4 style="color:white;">Highest Price</h4>
<h2 style="color:#00ff00;">${highest}</h2>
</div>
""", unsafe_allow_html=True)

# Lowest (Red Glow)
col2.markdown(f"""
<div style="padding:20px;border-radius:15px;background-color:#1f0f0f;text-align:center;box-shadow:0 0 15px #ff0000;">
<h4 style="color:white;">Lowest Price</h4>
<h2 style="color:#ff4d4d;">${lowest}</h2>
</div>
""", unsafe_allow_html=True)

# Average
col3.markdown(f"""
<div style="padding:20px;border-radius:15px;background-color:#111;text-align:center;">
<h4 style="color:white;">Average Price</h4>
<h2 style="color:#ccc;">${average}</h2>
</div>
""", unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown("## Full Data Table")

st.dataframe(
    df.drop(columns=["Change_numeric"]),
    use_container_width=True
)