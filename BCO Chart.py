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

# ---------------- DATA ----------------

data = [
    ["2026-02-28","Breakdown of U.S. Iran negotiations",70.89,2.45,"Positive","Diplomatic Breakdown","Trump / Iran",-0.5,"No OPEC response","Risk premium","Conflict fears rising","I'm not happy with Iran"],
    ["2026-03-01","Hormuz closure begins",78.22,6.82,"Positive","Chokepoint Closure","Iran IRGC",-12,"OPEC+ minor increase","Supply shock","Largest disruption","No ship allowed"],
    ["2026-03-02","US-Israel strikes Iran",77.74,7.26,"Positive","Military Escalation","US / Israel / Iran",-13,"Russian oil waiver","Escalation fears","Second rally","Ships will burn"],
    ["2026-03-03","Production shutdowns",81.40,4.71,"Positive","Shutdown","Saudi / Kuwait / UAE",-15,"Rerouting pipelines","Supply cut","15% supply hit","Escort tankers"],
    ["2026-03-04","Sustained disruption",81.40,0.00,"Positive","Supply Disruption","Traders",-15,"No action","Tight supply","Volatility","Oil flows disrupted"],
    ["2026-03-05","Tanker attacks",85.41,4.93,"Positive","Tanker Attack","Iran / Lloyds",-16,"Insurance spike","Shipping disruption","Freight surge","Inflation fears"],
    ["2026-03-06","Major supply shock",92.69,8.52,"Positive","Supply Shock","Trump",-17,"IEA discussions","No intervention","Biggest jump","Imminent action"],
    ["2026-03-07","Stabilisation",92.86,0.00,"Negative","Stability","Iran President",-17,"Talks hinted","No change","Flat trading","Conditional peace"],
    ["2026-03-08","Partial reopening",90.10,-2.97,"Negative","Partial Recovery","China / Iran",1,"China talks","Relief","Profit taking","Selective access"],
    ["2026-03-09","Infrastructure attacks",94.20,4.55,"Positive","Infrastructure Attack","Iran / UAE",-18,"Airspace closure","Renewed risk","Back above $94","Missile defense active"],
    ["2026-03-10","SPR talks",93.50,-0.74,"Negative","Policy","IEA",0,"400mb planned","Relief","Temporary drop","Largest disruption"],
    ["2026-03-11","SPR release + strikes",98.76,5.62,"Positive","Policy + Escalation","IEA / Iran",-18,"SPR announced","Insufficient supply","Prices surge","Temporary fix"],
    ["2026-03-12","Oil crosses $100",101.43,2.70,"Positive","Supply Loss","IEA",-8,"IEA confirms loss","Shortage confirmed","Break $100","Supply drop"],
    ["2026-03-13","Forecast upgrades",103.88,2.42,"Positive","Forecast","Goldman Sachs",-8,"Bullish outlook","Momentum buying","Prices rise","War panic ahead"],
    ["2026-03-14","Profit taking",102.15,-1.67,"Negative","Pullback","UAE",-17,"None","Correction","Slight drop","Tanker hit"],
    ["2026-03-15","Diplomatic talks",100.80,-0.36,"Negative","Diplomatic","India / Iran",-17,"Talks ongoing","Slight relief","Stable market","Talks ongoing"],
    ["2026-03-16","Sanctions easing signal",100.21,-2.84,"Negative","Policy","US Treasury",1.5,"Possible oil release","Relief","Price drops","Lift sanctions"],
    ["2026-03-17","Renewed attacks",103.42,3.20,"Positive","Attack","Iran",-16.5,"No progress","Tension","Prices climb","No NATO needed"],
    ["2026-03-18","Gas field attack",107.38,3.83,"Positive","Energy Attack","Iran / Qatar",-17,"LNG disruption","Energy crisis","Gas surge","Wait and see"],
    ["2026-03-19","Refinery strikes",115.52,7.58,"Positive","Infrastructure","Iran / Kuwait",-19,"Shutdown","Severe risk","Big jump","Energy targets"],
    ["2026-03-20","Iraq force majeure",112.19,3.26,"Positive","Force Majeure","Iraq",-20,"Production collapse","Real shortage","High volatility","Fields closed"],
    ["2026-03-21","Sustained attacks",112.50,0.28,"Positive","Sustained Damage","Kuwait",-20.5,"No solution","Holding levels","Flat day","Refinery fire"],
    ["2026-03-22","Market whipsaw",107.04,-4.86,"Negative","Volatility","US / Iran",-19,"Mixed signals","Uncertainty","Sharp drop","Price swings"],
    ["2026-03-23","Renewed surge",113.52,6.05,"Positive","Escalation","Iran / US",-20,"None","Fear buying","Strong rebound","Strait may close"]
]

columns = [
    "Date","Headline Event","Price","Change_numeric","Impact","Event Category",
    "Key Actors","Supply Impact (mb/d net)","OPEC/IEA/Policy Response",
    "Price Mechanism","Day-on-Day Narrative","Key Quote"
]

df = pd.DataFrame(data, columns=columns)

# ✅ FIX: Create proper Change column
df["Change"] = df["Change_numeric"].apply(lambda x: f"{x:+.2f}%")

# ---------------- CHART + METRICS SIDE BY SIDE ----------------
st.markdown("## Brent Crude Oil Price Trend & Key Metrics")

chart_col, metrics_col = st.columns([4, 1])  # bigger chart

# -------- LEFT: CHART --------
with chart_col:
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
            "Change"
        ]
    )

    fig.update_traces(
        line=dict(color="#13008D", width=3),
        marker=dict(size=6),
    )

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Price ($/Barrel)",
        annotations=[]
    )

    # Smart callouts
    for i in range(len(df)):
        change = df["Change_numeric"].iloc[i]

        if change > 5 or change < -5:
            color = "#00FFAA" if change > 0 else "#FF4B4B"

            fig.add_annotation(
                x=df["Date"].iloc[i],
                y=df["Price"].iloc[i],
                text=f"{df['Change'].iloc[i]}<br>{str(df['Key Quote'].iloc[i])[:50]}...",
                showarrow=True,
                arrowhead=2,
                arrowcolor=color,
                ax=0,
                ay=-80 if change > 0 else 80,
                bgcolor="rgba(0,0,0,0.7)",
                bordercolor=color,
                borderwidth=1,
                font=dict(size=10, color="white"),
            )

    st.plotly_chart(fig, use_container_width=True)


# -------- RIGHT: METRICS --------
with metrics_col:
    st.markdown("### Key Metrics")

    highest = df['Price'].max()
    lowest = df['Price'].min()
    average = round(df['Price'].mean(), 2)

    # 🔴 Highest (RED)
    st.markdown(f"""
    <div style="padding:12px;border-radius:10px;background-color:#1a0f0f;text-align:center;margin-bottom:10px;">
        <h6 style="color:white;margin:0;">Highest</h6>
        <h3 style="color:#ff4d4d;margin:0;">${highest}</h3>
    </div>
    """, unsafe_allow_html=True)

    # 🟢 Lowest (GREEN)
    st.markdown(f"""
    <div style="padding:12px;border-radius:10px;background-color:#0f1a0f;text-align:center;margin-bottom:10px;">
        <h6 style="color:white;margin:0;">Lowest</h6>
        <h3 style="color:#00ff88;margin:0;">${lowest}</h3>
    </div>
    """, unsafe_allow_html=True)

    # ⚪ Average (NEUTRAL)
    st.markdown(f"""
    <div style="padding:12px;border-radius:10px;background-color:#111;text-align:center;">
        <h6 style="color:white;margin:0;">Average</h6>
        <h3 style="color:#cccccc;margin:0;">${average}</h3>
    </div>
    """, unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown("## Full Data Table")

st.dataframe(df, use_container_width=True)