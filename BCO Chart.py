import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

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

st.markdown("## Brent Crude Oil")

chart_col, metrics_col = st.columns([4, 1])

# -------- LEFT: CHART --------
with chart_col:

    fig = px.line(
        df,
        x="Date",
        y="Price",
        title="Brent Crude Oil Prices Over Time"
    )

    # clean thin line, no dots
    fig.update_traces(
        line=dict(color="#0E2D5C", width=1.2),
        mode="lines",
        customdata=df[[
            "Headline Event",
            "Day-on-Day Narrative"
        ]],
        hovertemplate=
            "<b>Date:</b> %{x}<br>" +
            "<b>Price:</b> $%{y}<br>" +
            "<b>Event:</b> %{customdata[0]}<br>" +
            "<b>Narrative:</b> %{customdata[1]}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Price ($/Barrel)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# -------- RIGHT: METRICS --------
with metrics_col:

    # Title
    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <h4 style="margin:0;">Key Metrics</h4>
    </div>
    """, unsafe_allow_html=True)

    # --- CALCULATIONS ---
    max_increase = df["Change_numeric"].max()
    max_decrease = df["Change_numeric"].min()

    # --- DISPLAY ---
    st.metric(
        label="Increase",
        value=f"{max_increase:.2f}% ↑"
    )

    st.metric(
        label="Decrease",
        value=f"{abs(max_decrease):.2f}% ↓"
    )

# ---------------- TABLE ----------------
st.markdown("## Full Data Table")

st.dataframe(df, use_container_width=True)

# ---------------- MAP ----------------
st.markdown("## Global Strategic Waterways Map")

import folium
from folium.plugins import LocateControl, MiniMap, MousePosition

# ─── DATA ──────────────────────────────────────────────────────────────────────
waterways = [
    {
        "name": "Strait of Hormuz",
        "lat": 26.5667, "lon": 56.2500,
        "oil_flow": "20–21 million bbl/day",
        "width": "39 km (21 nautical miles)",
        "location_desc": "Between Iran and Oman, connecting the Gulf to the Arabian Sea",
        "significance": "World's most vital energy chokepoint; sole maritime exit for ~20% of global oil and LNG. Currently CLOSED by Iran (March 2026).",
        "status": "CLOSED",
        "status_color": "#FF0000",
        "risk_level": "CRITICAL",
        "trade_share": "~20% of global oil",
        "current_event": "Iran declared closure on 2 March 2026 following US-Israel Operation Epic Fury. Tanker traffic dropped 90%. Brent crude surged above $100/bbl.",
        "icon_color": "red",
        "icon": "warning-sign"
    },
    {
        "name": "Strait of Malacca",
        "lat": 2.5000, "lon": 101.3667,
        "oil_flow": "23 million bbl/day",
        "width": "2.8 km (1.5 nautical miles)",
        "location_desc": "Between Malaysia, Singapore and Indonesia, linking the Indian Ocean to the South China Sea",
        "significance": "World's busiest oil transit chokepoint. ~40% of global trade and 80% of China's oil imports pass through here.",
        "status": "OPEN",
        "status_color": "#00AA00",
        "risk_level": "MODERATE",
        "trade_share": "~40% of global trade",
        "current_event": "Currently operational but experiencing higher traffic as vessels avoid Hormuz. Regional tension remains due to South China Sea disputes.",
        "icon_color": "green",
        "icon": "ship"
    },
    {
        "name": "Bab al-Mandeb Strait",
        "lat": 12.5833, "lon": 43.3333,
        "oil_flow": "4 million bbl/day",
        "width": "32 km (17 nautical miles)",
        "location_desc": "Between Yemen and Djibouti, linking the Red Sea to the Gulf of Aden",
        "significance": "Gateway to the Suez Canal. ~12% of global trade flows daily. Houthi attacks disrupted traffic from 2023-2025.",
        "status": "HIGH RISK",
        "status_color": "#FF6600",
        "risk_level": "HIGH",
        "trade_share": "~12% of global trade",
        "current_event": "Houthi attacks have largely ceased with Iran's attentions diverted but risk remains elevated. Maersk has suspended Gulf transits and reroutes via Cape of Good Hope.",
        "icon_color": "orange",
        "icon": "warning-sign"
    },
    {
        "name": "Suez Canal",
        "lat": 30.7000, "lon": 32.3500,
        "oil_flow": "5 million bbl/day",
        "width": "225 m (740 ft)",
        "location_desc": "Divides the Sinai Peninsula from Egypt, connecting the Mediterranean to the Red Sea",
        "significance": "Shortens Asia-Europe journey by ~8,900 km. Opened 1869. Famous 2021 blockage by Ever Given for 6 days.",
        "status": "REDUCED",
        "status_color": "#FF6600",
        "risk_level": "HIGH",
        "trade_share": "~12-15% of global trade",
        "current_event": "Traffic significantly reduced as shipping lines avoid the Hormuz-Red Sea corridor. Maersk and Hapag-Lloyd have suspended Suez Canal transits in March 2026.",
        "icon_color": "orange",
        "icon": "exclamation-sign"
    },
    {
        "name": "Cape of Good Hope",
        "lat": -34.3568, "lon": 18.4730,
        "oil_flow": "9 million bbl/day",
        "width": "Open Ocean",
        "location_desc": "Off the southwestern tip of the Cape Peninsula in South Africa",
        "significance": "Alternative route bypassing Middle East. Used by ships too large for Suez. Adds 10-14 days and 3,000-4,000 nm to Asia-Europe journeys.",
        "status": "SURGE",
        "status_color": "#0080FF",
        "risk_level": "LOW",
        "trade_share": "Rapidly growing — now 11%+ of global trade rerouting",
        "current_event": "Cape Town Port records 112% surge in diverted vessels (March 2026). SAMSA on high alert. Transit up 35%+ vs. 7-day averages. Hapag-Lloyd, Maersk, CMA CGM all rerouting here.",
        "icon_color": "blue",
        "icon": "arrow-up"
    },
    {
        "name": "Taiwan Strait",
        "lat": 24.2500, "lon": 119.5000,
        "oil_flow": "N/A (container focus)",
        "width": "130 km (70 nautical miles)",
        "location_desc": "Separates mainland China from Taiwan, connecting the South China Sea to the East China Sea",
        "significance": "Over 20% of global maritime trade by value annually. Nearly half the global container fleet passes here. Most advanced semiconductors transited here.",
        "status": "TENSE",
        "status_color": "#FF6600",
        "risk_level": "HIGH",
        "trade_share": ">20% of global maritime trade by value",
        "current_event": "China has increased military exercises amid global focus on Middle East. Risk of Taiwan contingency elevated as US forces engaged in Gulf.",
        "icon_color": "orange",
        "icon": "flag"
    },
    {
        "name": "Panama Canal",
        "lat": 9.0800, "lon": -79.6800,
        "oil_flow": "2–3 million bbl/day",
        "width": "222 m (730 ft)",
        "location_desc": "Cuts through Panama, connecting the Caribbean Sea to the Pacific Ocean",
        "significance": "Conduit for 40% of US container traffic. Handles >95% of US LPG exports to Asia. Opened 1914 with lock system.",
        "status": "OPERATIONAL",
        "status_color": "#00AA00",
        "risk_level": "MODERATE",
        "trade_share": "~5% of global trade",
        "current_event": "Recovering from 2024-2025 drought restrictions. Seeing unexpected 8-10% toll revenue boost as some Asia-US West Coast traffic reroutes via Pacific. Geopolitical pressure from US tariff threats on Panama.",
        "icon_color": "green",
        "icon": "transfer"
    },
    {
        "name": "Strait of Gibraltar",
        "lat": 35.9500, "lon": -5.4833,
        "oil_flow": "5–6 million bbl/day",
        "width": "13 km (7 nautical miles)",
        "location_desc": "Between Spain and Morocco, linking the Atlantic Ocean to the Mediterranean Sea",
        "significance": "Only natural maritime link between Atlantic and Mediterranean. Western entry point for all Suez-bound shipping.",
        "status": "OPEN",
        "status_color": "#00AA00",
        "risk_level": "LOW",
        "trade_share": "Gateway to Mediterranean and Suez routes",
        "current_event": "Operational but throughput has declined as Suez Canal traffic drops. Atlantic-facing ports Rotterdam and Hamburg now capturing more Cape-routed traffic.",
        "icon_color": "green",
        "icon": "globe"
    },
    {
        "name": "Turkish Straits (Bosphorus)",
        "lat": 41.1100, "lon": 29.0500,
        "oil_flow": "3–4 million bbl/day",
        "width": "700 m (2,300 ft)",
        "location_desc": "Through Istanbul, linking the Black Sea to the Mediterranean",
        "significance": "Comprising Bosphorus and Dardanelles. Only maritime link between Black Sea and Mediterranean. Vital for Russian and Caspian oil exports.",
        "status": "OPEN",
        "status_color": "#00AA00",
        "risk_level": "MODERATE",
        "trade_share": "Key Russian & Caspian oil transit",
        "current_event": "Turkey approved passage of a Turkish ship through Hormuz on 13 March 2026. Istanbul straits operational; Russia rerouting some oil via Black Sea due to overall market shifts.",
        "icon_color": "green",
        "icon": "transfer"
    },
    {
        "name": "Danish Straits",
        "lat": 55.6500, "lon": 10.6000,
        "oil_flow": "5 million bbl/day",
        "width": "3.7 km (2 nautical miles)",
        "location_desc": "Separates Denmark from Sweden, connecting the Baltic Sea to the North Sea",
        "significance": "Primary exit for Russian oil from Baltic ports. Crucial link for Northern Europe to global markets.",
        "status": "OPEN",
        "status_color": "#00AA00",
        "risk_level": "MODERATE",
        "trade_share": "Key Russian Baltic oil exit",
        "current_event": "Operational. Increased scrutiny on Russian Baltic crude flows amid broader Middle East conflict. NATO monitoring of Baltic sea increased.",
        "icon_color": "green",
        "icon": "map-marker"
    },
]

# ─── COLOUR SCHEME ──────────────────────────────────────────────────────────────
STATUS_COLOURS = {
    "CLOSED":      "#FF0000",
    "HIGH RISK":   "#FF6600",
    "TENSE":       "#FF9900",
    "REDUCED":     "#FFAA00",
    "SURGE":       "#0080FF",
    "OPERATIONAL": "#00AA00",
    "OPEN":        "#00CC44",
}

RISK_COLOURS = {
    "CRITICAL": "#FF0000",
    "HIGH":     "#FF6600",
    "MODERATE": "#FFAA00",
    "LOW":      "#00AA00",
}

# ─── MAP SETUP ─────────────────────────────────────────────────────────────────
m = folium.Map(
    location=[20, 30],
    zoom_start=3,
    tiles=None,
    control_scale=True,
)

# Dark tile layer
folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    name="Dark Map",
    max_zoom=19
).add_to(m)

# Satellite layer
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite",
    max_zoom=19
).add_to(m)

# ─── FEATURE GROUPS ───────────────────────────────────────────────────────────
fg_critical = folium.FeatureGroup(name="🔴 Critical / Closed", show=True)
fg_high     = folium.FeatureGroup(name="🟠 High Risk / Reduced", show=True)
fg_open     = folium.FeatureGroup(name="🟢 Open / Operational", show=True)
fg_special  = folium.FeatureGroup(name="🔵 Special Events (Surge / Tense)", show=True)

group_map = {
    "CLOSED":      fg_critical,
    "HIGH RISK":   fg_high,
    "REDUCED":     fg_high,
    "TENSE":       fg_high,
    "SURGE":       fg_special,
    "OPERATIONAL": fg_open,
    "OPEN":        fg_open,
}

# ─── MARKERS ─────────────────────────────────────────────────────────────────
for ww in waterways:
    status_col = STATUS_COLOURS.get(ww["status"], "#AAAAAA")
    risk_col   = RISK_COLOURS.get(ww["risk_level"], "#AAAAAA")

    popup_html = f"""
    <div style="font-family:'Segoe UI',sans-serif;width:340px;background:#1a1a2e;color:#e0e0e0;border-radius:10px;padding:15px;box-shadow:0 4px 15px rgba(0,0,0,0.5);">
      <h3 style="margin:0 0 8px;color:#FFD700;font-size:15px;border-bottom:1px solid #444;padding-bottom:6px;">
        {ww['name']}
      </h3>
      <div style="margin-bottom:8px;">
        <span style="background:{status_col};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold;">
          {ww['status']}
        </span>
        <span style="background:{risk_col};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold;margin-left:6px;">
          RISK: {ww['risk_level']}
        </span>
      </div>
      <table style="width:100%;font-size:12px;border-collapse:collapse;">
        <tr style="border-bottom:1px solid #333;">
          <td style="padding:4px 0;color:#AAA;width:38%;">Location</td>
          <td style="padding:4px 0;">{ww['location_desc']}</td>
        </tr>
        <tr style="border-bottom:1px solid #333;">
          <td style="padding:4px 0;color:#AAA;">Width</td>
          <td style="padding:4px 0;">{ww['width']}</td>
        </tr>
        <tr style="border-bottom:1px solid #333;">
          <td style="padding:4px 0;color:#AAA;">Oil Flow</td>
          <td style="padding:4px 0;">{ww['oil_flow']}</td>
        </tr>
        <tr style="border-bottom:1px solid #333;">
          <td style="padding:4px 0;color:#AAA;">Trade Share</td>
          <td style="padding:4px 0;">{ww['trade_share']}</td>
        </tr>
        <tr style="border-bottom:1px solid #333;">
          <td style="padding:4px 0;color:#AAA;">Significance</td>
          <td style="padding:4px 0;">{ww['significance']}</td>
        </tr>
        <tr>
          <td style="padding:4px 0;color:#FFD700;vertical-align:top;">Now</td>
          <td style="padding:4px 0;color:#FFD700;">{ww['current_event']}</td>
        </tr>
      </table>
    </div>
    """

    # Pulsing circle for closed / critical
    if ww["status"] == "CLOSED":
        folium.CircleMarker(
            location=[ww["lat"], ww["lon"]],
            radius=22,
            color=status_col,
            fill=True,
            fill_color=status_col,
            fill_opacity=0.15,
            weight=2,
            popup=folium.Popup(popup_html, max_width=360),
            tooltip=f"<b>{ww['name']}</b> — {ww['status']}",
        ).add_to(fg_critical)

    folium.CircleMarker(
        location=[ww["lat"], ww["lon"]],
        radius=10,
        color=status_col,
        fill=True,
        fill_color=status_col,
        fill_opacity=0.8,
        weight=2,
        popup=folium.Popup(popup_html, max_width=360),
        tooltip=f"<b>{ww['name']}</b> — {ww['status']}",
    ).add_to(group_map.get(ww["status"], fg_open))

    # Label
    folium.Marker(
        location=[ww["lat"] + 1.5, ww["lon"]],
        icon=folium.DivIcon(
            html=f'<div style="font-family:Segoe UI,sans-serif;font-size:10px;font-weight:bold;color:#FFD700;text-shadow:0 0 4px #000,0 0 4px #000;white-space:nowrap;">{ww["name"]}</div>',
            icon_size=(200, 20),
            icon_anchor=(100, 10),
        ),
        popup=folium.Popup(popup_html, max_width=360),
    ).add_to(group_map.get(ww["status"], fg_open))

# ─── SHIPPING ROUTES (approximate great-circle arcs) ────────────────────────
routes = [
    {
        "name": "Asia–Europe via Suez (disrupted)",
        "coords": [[1.3, 103.8],[7.0,80],[12.5,43.5],[26,37],[29.9,32.5],[32,32],[36,30],[40,25],[43,16],[45,12],[51,30],[54,38],[55,45],[51.9,4.5]],
        "color": "#FF6600",
        "dash": "8,8",
        "weight": 2,
        "tooltip": "Asia–Europe Suez Route (DISRUPTED — most carriers now avoiding)"
    },
    {
        "name": "Asia–Europe via Cape of Good Hope (active surge)",
        "coords": [[1.3,103.8],[-5,100],[-15,90],[-25,70],[-34,18.5],[-30,15],[-20,10],[-5,5],[5,-5],[15,-15],[35.9,-5.5],[45,-5],[51.9,4.5]],
        "color": "#00AAFF",
        "dash": None,
        "weight": 3,
        "tooltip": "Asia–Europe Cape of Good Hope Route (ACTIVE — traffic +35% and surging)"
    },
    {
        "name": "Persian Gulf exports (Hormuz — CLOSED)",
        "coords": [[26,50],[26.5,56.2],[22,60],[15,55]],
        "color": "#FF0000",
        "dash": "5,5",
        "weight": 3,
        "tooltip": "Persian Gulf Oil Exports through Hormuz — EFFECTIVELY CLOSED"
    },
    {
        "name": "Asia–Americas via Panama",
        "coords": [[1.3,103.8],[10,130],[20,140],[30,150],[10,-80],[9,-79.7],[18,-75],[25,-75],[40,-70],[51,0]],
        "color": "#AAFFAA",
        "dash": None,
        "weight": 2,
        "tooltip": "Asia–Americas via Panama Canal"
    },
]

fg_routes = folium.FeatureGroup(name="Shipping Routes", show=True)
for route in routes:
    folium.PolyLine(
        locations=route["coords"],
        color=route["color"],
        weight=route["weight"],
        opacity=0.75,
        dash_array=route.get("dash"),
        tooltip=route["tooltip"],
    ).add_to(fg_routes)

# ─── ADD ALL LAYERS ───────────────────────────────────────────────────────────
fg_routes.add_to(m)
fg_critical.add_to(m)
fg_high.add_to(m)
fg_special.add_to(m)
fg_open.add_to(m)

# ─── PLUGINS ─────────────────────────────────────────────────────────────────
MiniMap(toggle_display=True, tile_layer="CartoDB dark_matter").add_to(m)
MousePosition().add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

# ─── CUSTOM HEADER / LEGEND ──────────────────────────────────────────────────
legend_html = """
<div id="map-header" style="
    position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:9999;
    background:rgba(10,10,30,0.92);border:1px solid #FFD700;border-radius:10px;
    padding:10px 20px;text-align:center;font-family:'Segoe UI',sans-serif;pointer-events:none;">
  <div style="color:#FFD700;font-size:16px;font-weight:bold;letter-spacing:2px;">
    GLOBAL STRATEGIC WATERWAYS — LIVE STATUS
  </div>
  <div style="color:#AAA;font-size:11px;margin-top:3px;">
    March 2026 | US-Israel-Iran War Impact on Global Shipping
  </div>
</div>

<div id="legend" style="
    position:fixed;bottom:30px;left:15px;z-index:9999;
    background:rgba(10,10,30,0.92);border:1px solid #444;border-radius:10px;
    padding:12px 16px;font-family:'Segoe UI',sans-serif;font-size:12px;color:#DDD;
    min-width:200px;">
  <div style="color:#FFD700;font-weight:bold;margin-bottom:8px;">STATUS LEGEND</div>
  <div><span style="color:#FF0000;">● </span> CLOSED — Hormuz blocked</div>
  <div><span style="color:#FF6600;">● </span> HIGH RISK / DISRUPTED</div>
  <div><span style="color:#0080FF;">● </span> TRAFFIC SURGE (rerouting)</div>
  <div><span style="color:#00AA00;">● </span> OPEN / OPERATIONAL</div>
  <hr style="border-color:#444;margin:8px 0;">
  <div style="color:#FFD700;font-weight:bold;margin-bottom:4px;">OIL PRICE (Mar 2026)</div>
  <div>Brent: ~$102/bbl 🔺</div>
  <div>WTI: ~$96/bbl 🔺</div>
  <div style="color:#FF6600;font-size:10px;margin-top:4px;">+40% since Feb 28 strikes</div>
</div>

<div id="alert-box" style="
    position:fixed;bottom:30px;right:15px;z-index:9999;
    background:rgba(100,0,0,0.9);border:2px solid #FF0000;border-radius:10px;
    padding:12px 16px;font-family:'Segoe UI',sans-serif;font-size:12px;color:#FFF;
    max-width:260px;animation:blink 2s infinite;">
  <div style="color:#FFD700;font-weight:bold;margin-bottom:6px;">ACTIVE CRISIS</div>
  <div><b>Strait of Hormuz CLOSED</b></div>
  <div style="color:#FFB0B0;margin-top:4px;">
    Iran declared closure 2 Mar 2026.<br>
    90% traffic drop. 170 ships stranded.<br>
    20% of world oil supply disrupted.<br>
    Cape of Good Hope traffic +112%.
  </div>
</div>

<style>
@keyframes blink {
  0%,100% { border-color:#FF0000; }
  50%      { border-color:#FF8800; }
}
</style>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# display map in Streamlit
st_folium(m, width="stretch", height=700)