from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="SupplyShield AI",
    page_icon="S",
    layout="wide",
)


# ==================================================
# THEME
# ==================================================

st.markdown(
    """
    <style>
        :root {
            --bg: #031410;
            --bg-2: #06261f;
            --panel: rgba(8, 48, 39, 0.82);
            --panel-strong: rgba(7, 61, 49, 0.92);
            --line: rgba(25, 255, 167, 0.22);
            --green: #00f58d;
            --teal: #00d6d6;
            --blue: #1f85ff;
            --amber: #ffc928;
            --red: #ff4f62;
            --text: #effff8;
            --muted: #8fb7a9;
        }

        .stApp {
            background:
                radial-gradient(circle at 73% 2%, rgba(0, 245, 141, 0.18), transparent 30%),
                radial-gradient(circle at 20% 25%, rgba(0, 214, 214, 0.14), transparent 30%),
                linear-gradient(135deg, #020b09 0%, #031410 46%, #071f18 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.1rem;
            padding-bottom: 2rem;
            max-width: 1440px;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(2, 18, 15, 0.98), rgba(5, 31, 25, 0.98)),
                radial-gradient(circle at top, rgba(0, 245, 141, 0.16), transparent 38%);
            border-right: 1px solid rgba(0, 245, 141, 0.2);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: var(--text);
        }

        .hero {
            position: relative;
            min-height: 360px;
            overflow: hidden;
            border: 1px solid rgba(0, 245, 141, 0.22);
            border-radius: 18px;
            background:
                linear-gradient(90deg, rgba(4, 36, 29, 0.96), rgba(5, 52, 42, 0.72)),
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
            background-size: auto, 56px 56px, 56px 56px;
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.45);
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 760px;
            padding: 2.35rem;
        }

        .hero-visual {
            position: absolute;
            right: 4.5%;
            top: 15%;
            width: min(360px, 34vw);
            aspect-ratio: 1;
            border: 1px solid rgba(0, 245, 141, 0.2);
            border-radius: 32px;
            background: rgba(0, 0, 0, 0.14);
            box-shadow: inset 0 0 70px rgba(0, 245, 141, 0.16);
        }

        .planet {
            position: absolute;
            inset: 17%;
            border-radius: 999px;
            background:
                radial-gradient(circle at 35% 40%, rgba(155, 255, 183, 0.95) 0 8%, transparent 9%),
                radial-gradient(circle at 57% 55%, rgba(70, 216, 109, 0.9) 0 10%, transparent 11%),
                radial-gradient(circle at 42% 62%, rgba(79, 197, 89, 0.9) 0 12%, transparent 13%),
                linear-gradient(135deg, #00f58d, #00d6d6 48%, #1f85ff);
            box-shadow: 0 0 55px rgba(0, 245, 141, 0.45);
        }

        .orbit {
            position: absolute;
            inset: 12%;
            border-radius: 999px;
            border: 18px solid rgba(0, 245, 141, 0.34);
            transform: rotate(-18deg);
            filter: drop-shadow(0 0 28px rgba(0, 245, 141, 0.28));
        }

        .node {
            position: absolute;
            width: 13px;
            height: 13px;
            border-radius: 999px;
            background: var(--green);
            box-shadow: 0 0 22px rgba(0, 245, 141, 0.9);
        }

        .node-a { top: 16%; left: 17%; }
        .node-b { right: 18%; top: 28%; background: var(--teal); }
        .node-c { right: 22%; bottom: 17%; background: var(--amber); }

        .eyebrow {
            color: var(--green);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 0.8rem;
        }

        .hero h1 {
            color: var(--text);
            font-size: clamp(2.8rem, 6vw, 5.6rem);
            line-height: 0.9;
            letter-spacing: 0;
            margin: 0;
        }

        .hero p {
            max-width: 650px;
            color: #c8e7db;
            font-size: 1.05rem;
            line-height: 1.65;
            margin: 1rem 0 1.4rem;
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
        }

        .chip {
            border: 1px solid rgba(0, 245, 141, 0.28);
            border-radius: 999px;
            background: rgba(4, 24, 20, 0.76);
            color: #dffff3;
            padding: 0.5rem 0.75rem;
            font-size: 0.82rem;
            box-shadow: 0 0 18px rgba(0, 245, 141, 0.12);
        }

        .section-label {
            margin: 1.35rem 0 0.65rem;
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 850;
            letter-spacing: 0;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .glass-card,
        .status-panel,
        .alert-card,
        .copilot-answer {
            border: 1px solid rgba(0, 245, 141, 0.18);
            border-radius: 14px;
            background:
                linear-gradient(180deg, rgba(8, 54, 44, 0.82), rgba(4, 18, 16, 0.84));
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.05),
                0 22px 55px rgba(0, 0, 0, 0.32);
            padding: 1rem;
        }

        .glass-card { min-height: 134px; }

        .card-label,
        .status-title {
            color: var(--muted);
            font-size: 0.76rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0;
        }

        .card-value {
            color: var(--text);
            font-size: clamp(1.65rem, 2.5vw, 2.35rem);
            font-weight: 900;
            line-height: 1.05;
            margin-top: 0.7rem;
        }

        .card-sub,
        .status-copy,
        .alert-copy {
            color: #a9cbbf;
            font-size: 0.85rem;
            line-height: 1.45;
            margin-top: 0.55rem;
        }

        .neon-green { border-color: rgba(0, 245, 141, 0.38); box-shadow: 0 0 26px rgba(0, 245, 141, 0.12), 0 22px 55px rgba(0,0,0,0.32); }
        .neon-teal { border-color: rgba(0, 214, 214, 0.38); box-shadow: 0 0 26px rgba(0, 214, 214, 0.12), 0 22px 55px rgba(0,0,0,0.32); }
        .neon-amber { border-color: rgba(255, 201, 40, 0.38); box-shadow: 0 0 26px rgba(255, 201, 40, 0.12), 0 22px 55px rgba(0,0,0,0.32); }
        .neon-red { border-color: rgba(255, 79, 98, 0.42); box-shadow: 0 0 26px rgba(255, 79, 98, 0.14), 0 22px 55px rgba(0,0,0,0.32); }
        .neon-blue { border-color: rgba(31, 133, 255, 0.38); box-shadow: 0 0 26px rgba(31, 133, 255, 0.12), 0 22px 55px rgba(0,0,0,0.32); }

        .status-value {
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 850;
            margin-top: 0.4rem;
        }

        .alert-card {
            display: grid;
            grid-template-columns: 10px 1fr auto;
            gap: 0.75rem;
            align-items: center;
            margin-bottom: 0.7rem;
        }

        .alert-dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: var(--red);
            box-shadow: 0 0 18px currentColor;
        }

        .alert-title {
            color: var(--text);
            font-weight: 850;
        }

        .badge {
            color: #042017;
            background: var(--green);
            border-radius: 999px;
            padding: 0.28rem 0.58rem;
            font-size: 0.72rem;
            font-weight: 850;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
        }

        .summary-item {
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.035);
            padding: 0.75rem;
        }

        .summary-k {
            color: var(--muted);
            font-size: 0.73rem;
            font-weight: 850;
            text-transform: uppercase;
        }

        .summary-v {
            color: var(--text);
            font-size: 1rem;
            font-weight: 780;
            margin-top: 0.22rem;
        }

        .copilot-answer {
            color: #dcfff1;
            line-height: 1.6;
            margin-top: 0.8rem;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stPlotlyChart"] {
            border-radius: 14px;
        }

        h1, h2, h3, p, label, span { letter-spacing: 0; }

        @media (max-width: 1000px) {
            .hero-visual { display: none; }
            .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        @media (max-width: 680px) {
            .hero-content { padding: 1.35rem; }
            .metric-grid, .summary-grid { grid-template-columns: 1fr; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# LOAD MODEL & DATA
# ==================================================

ROOT_DIR = Path(__file__).resolve().parents[1]


def first_existing_path(*paths):
    for path in paths:
        if path.exists():
            return path
    return paths[0]


model_path = first_existing_path(
    ROOT_DIR / "Models" / "forecast_model.pkl",
    ROOT_DIR / "models" / "forecast_model.pkl",
    Path.cwd() / "Models" / "forecast_model.pkl",
    Path.cwd() / "models" / "forecast_model.pkl",
)

data_path = first_existing_path(
    ROOT_DIR / "Data" / "tableau_dashboard_master_universidad.csv",
    ROOT_DIR / "data" / "tableau_dashboard_master_universidad.csv",
    Path.cwd() / "Data" / "tableau_dashboard_master_universidad.csv",
    Path.cwd() / "data" / "tableau_dashboard_master_universidad.csv",
)

model = joblib.load(model_path)
df = pd.read_csv(data_path)
sample = df.drop("Total_Inventory_Cost", axis=1).iloc[-1:]
forecast = float(model.predict(sample)[0])


# ==================================================
# EVENT INTELLIGENCE
# ==================================================

EVENTS = {
    "Warehouse Fire": {
        "impact": 0.40,
        "location": "Vietnam Warehouse",
        "feed": "Disaster Feed",
        "delay": 7,
        "suppliers": 4,
        "skus": 17,
        "backup": "Saigon Backup Hub",
        "driver": "Warehouse capacity offline",
    },
    "Warehouse Damage": {
        "impact": 0.34,
        "location": "Bangkok DC",
        "feed": "Facility Sensor",
        "delay": 5,
        "suppliers": 3,
        "skus": 13,
        "backup": "Thai Cross-Dock B",
        "driver": "Dock throughput reduced",
    },
    "AWS Outage": {
        "impact": 0.28,
        "location": "Cloud Control Plane",
        "feed": "Cloud Status",
        "delay": 3,
        "suppliers": 6,
        "skus": 22,
        "backup": "Manual EDI fallback",
        "driver": "Order orchestration delayed",
    },
    "Cyber Attack": {
        "impact": 0.36,
        "location": "Tier-1 Supplier ERP",
        "feed": "Cyber Threat Feed",
        "delay": 6,
        "suppliers": 5,
        "skus": 19,
        "backup": "Pre-approved Supplier Delta",
        "driver": "Supplier systems isolated",
    },
    "Extreme Weather": {
        "impact": 0.32,
        "location": "Vietnam Coast",
        "feed": "Weather API",
        "delay": 6,
        "suppliers": 4,
        "skus": 15,
        "backup": "Inland Rail Route",
        "driver": "Flood and storm risk",
    },
    "Port Congestion": {
        "impact": 0.30,
        "location": "Singapore Port",
        "feed": "Port Congestion Data",
        "delay": 4,
        "suppliers": 3,
        "skus": 14,
        "backup": "Port Klang diversion",
        "driver": "Container dwell time spike",
    },
    "Traffic Disruption": {
        "impact": 0.22,
        "location": "Mumbai Corridor",
        "feed": "Traffic Data",
        "delay": 2,
        "suppliers": 2,
        "skus": 9,
        "backup": "Night dispatch window",
        "driver": "Last-mile route slowdown",
    },
    "Supplier Bankruptcy": {
        "impact": 0.45,
        "location": "Tier-2 Component Supplier",
        "feed": "Financial Risk Feed",
        "delay": 10,
        "suppliers": 7,
        "skus": 26,
        "backup": "Dual-source activation",
        "driver": "Component availability shock",
    },
    "Flood": {
        "impact": 0.25,
        "location": "Chennai Warehouse",
        "feed": "Disaster Feed",
        "delay": 4,
        "suppliers": 3,
        "skus": 11,
        "backup": "Bangalore DC",
        "driver": "Inbound lanes degraded",
    },
}

SUPPLIER_RISK = pd.DataFrame(
    [
        ["Vietnam Supplier", "Vietnam", "Supplier", 10.8231, 106.6297, 92, "High"],
        ["Singapore Port", "Singapore", "Port", 1.2644, 103.8200, 74, "Medium"],
        ["Shanghai Port", "China", "Port", 31.2304, 121.4737, 66, "Medium"],
        ["Mumbai Port", "India", "Port", 18.9388, 72.8354, 28, "Low"],
        ["Bangalore DC", "India", "Warehouse", 12.9716, 77.5946, 34, "Low"],
        ["Rotterdam Port", "Netherlands", "Port", 51.9244, 4.4777, 48, "Medium"],
        ["Texas Fulfillment", "USA", "Warehouse", 29.7604, -95.3698, 39, "Low"],
    ],
    columns=["name", "country", "type", "lat", "lon", "risk", "level"],
)


# ==================================================
# SIDEBAR CONTROLS
# ==================================================

st.sidebar.markdown("## SupplyShield AI")
st.sidebar.caption("Global disruption command center")

page = st.sidebar.radio(
    "Navigation",
    [
        "Command Center",
        "Global Map",
        "Digital Twin",
        "AI Copilot",
        "Architecture",
    ],
    index=0,
)

st.sidebar.markdown("### Event Intelligence")
event = st.sidebar.radio(
    "Select Disruption Event",
    list(EVENTS.keys()),
    index=0,
)

impact_percent = st.sidebar.slider(
    "Disruption Severity (%)",
    0,
    100,
    int(EVENTS[event]["impact"] * 100),
)

demand_surge = st.sidebar.slider(
    "Demand Surge (%)",
    0,
    100,
    20,
)

automation_mode = st.sidebar.toggle("Automated Response Mode", value=True)
event_meta = EVENTS[event]


# ==================================================
# CORE MODEL FLOW
# ==================================================

residual_std = 34.49
lower = forecast - 1.96 * residual_std
upper = forecast + 1.96 * residual_std

adjusted_demand = forecast * (1 + demand_surge / 100)
remaining_supply = adjusted_demand * (1 - impact_percent / 100)
supply_loss = impact_percent
ratio = remaining_supply / adjusted_demand
risk_score = round((1 - ratio) * 100, 1)

if ratio < 0.7:
    risk = "HIGH"
elif ratio < 0.9:
    risk = "MEDIUM"
else:
    risk = "LOW"

risk_color = {
    "HIGH": "#ff4f62",
    "MEDIUM": "#ffc928",
    "LOW": "#00f58d",
}[risk]

if risk == "HIGH":
    recommendation = "Emergency Replenishment"
elif risk == "MEDIUM":
    recommendation = "Increase Safety Stock"
else:
    recommendation = "Normal Operations"

estimated_loss = adjusted_demand - remaining_supply
predicted_revenue_loss = estimated_loss * float(sample["Base_Unit_Price"].iloc[0]) * max(1, event_meta["delay"])
global_risk_score = min(100, round(risk_score + event_meta["delay"] * 3 + event_meta["suppliers"] * 2))
response_action = "Auto-create replenishment order" if risk == "HIGH" else recommendation


# ==================================================
# DATA PRODUCTS
# ==================================================

alerts = [
    {
        "title": event,
        "detail": f"{event_meta['location']} flagged by {event_meta['feed']}",
        "level": risk,
    },
    {
        "title": "Lead Time Anomaly",
        "detail": f"Expected delay increased by {event_meta['delay']} days",
        "level": "MEDIUM" if event_meta["delay"] < 6 else "HIGH",
    },
    {
        "title": "Demand Surge Monitor",
        "detail": f"Demand stress set to {demand_surge}% above forecast",
        "level": "LOW" if demand_surge < 25 else "MEDIUM",
    },
    {
        "title": "Automated Response",
        "detail": response_action if automation_mode else "Human approval required",
        "level": "LOW" if automation_mode else "MEDIUM",
    },
]

heatmap_df = pd.DataFrame(
    [
        ["Vietnam Supplier", "Lead Time", min(100, global_risk_score + 8)],
        ["Vietnam Supplier", "Capacity", min(100, global_risk_score + 3)],
        ["Vietnam Supplier", "Cyber", 48],
        ["Vietnam Supplier", "Weather", 72],
        ["Singapore Port", "Lead Time", 76 if event == "Port Congestion" else 58],
        ["Singapore Port", "Capacity", 82 if event == "Port Congestion" else 61],
        ["Singapore Port", "Cyber", 28],
        ["Singapore Port", "Weather", 44],
        ["Mumbai Port", "Lead Time", 31],
        ["Mumbai Port", "Capacity", 26],
        ["Mumbai Port", "Cyber", 22],
        ["Mumbai Port", "Weather", 29],
        ["Bangalore DC", "Lead Time", 38],
        ["Bangalore DC", "Capacity", 34],
        ["Bangalore DC", "Cyber", 25],
        ["Bangalore DC", "Weather", 41],
    ],
    columns=["Supplier", "Risk Vector", "Risk"],
)

importance = pd.DataFrame(
    {
        "Feature": sample.columns,
        "Importance": model.feature_importances_,
    }
).sort_values("Importance", ascending=False)


# ==================================================
# REUSABLE RENDERERS
# ==================================================

def render_hero():
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">AI active | Supply chain digital twin</div>
                <h1>SupplyShield AI</h1>
                <p>
                    A global risk command center that predicts demand, detects disruption
                    events, simulates operational impact, and recommends automated response
                    before shortages occur.
                </p>
                <div class="chip-row">
                    <span class="chip">Forecast: {forecast:,.0f}</span>
                    <span class="chip">Global risk: {global_risk_score}/100</span>
                    <span class="chip">Scenario: {event}</span>
                    <span class="chip">Mode: {"Auto" if automation_mode else "Approval"}</span>
                </div>
            </div>
            <div class="hero-visual">
                <div class="orbit"></div>
                <div class="planet"></div>
                <div class="node node-a"></div>
                <div class="node node-b"></div>
                <div class="node node-c"></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards():
    high_risk_suppliers = int((SUPPLIER_RISK["risk"] >= 65).sum() + max(0, event_meta["suppliers"] - 3))
    expected_delays = event_meta["delay"]
    esg_score = max(45, 92 - int(global_risk_score * 0.45))
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="glass-card neon-red">
                <div class="card-label">Global Risk Score</div>
                <div class="card-value" style="color:{risk_color};">{global_risk_score}</div>
                <div class="card-sub">Composite forecast + event intelligence score</div>
            </div>
            <div class="glass-card neon-amber">
                <div class="card-label">High Risk Suppliers</div>
                <div class="card-value">{high_risk_suppliers}</div>
                <div class="card-sub">Suppliers requiring review</div>
            </div>
            <div class="glass-card neon-teal">
                <div class="card-label">Expected Delays</div>
                <div class="card-value">{expected_delays}</div>
                <div class="card-sub">Days added by digital twin</div>
            </div>
            <div class="glass-card neon-green">
                <div class="card-label">Predicted Loss</div>
                <div class="card-value">${predicted_revenue_loss / 1000:,.0f}K</div>
                <div class="card-sub">Estimated unmet demand exposure</div>
            </div>
            <div class="glass-card neon-blue">
                <div class="card-label">Resilience Score</div>
                <div class="card-value">{esg_score}</div>
                <div class="card-sub">Operational continuity index</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alerts():
    st.markdown('<div class="section-label">Live Event Intelligence Alerts</div>', unsafe_allow_html=True)
    for alert in alerts:
        color = {"HIGH": "#ff4f62", "MEDIUM": "#ffc928", "LOW": "#00f58d"}[alert["level"]]
        st.markdown(
            f"""
            <div class="alert-card">
                <div class="alert-dot" style="background:{color}; color:{color};"></div>
                <div>
                    <div class="alert-title">{alert["title"]}</div>
                    <div class="alert-copy">{alert["detail"]}</div>
                </div>
                <span class="badge" style="background:{color};">{alert["level"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def plot_supply_impact():
    fig = go.Figure()
    fig.add_bar(
        name="Adjusted Demand",
        x=["Scenario"],
        y=[adjusted_demand],
        marker={"color": "rgba(0, 214, 214, 0.82)", "line": {"color": "#00d6d6", "width": 2}},
    )
    fig.add_bar(
        name="Remaining Supply",
        x=["Scenario"],
        y=[remaining_supply],
        marker={"color": "rgba(0, 245, 141, 0.78)", "line": {"color": "#00f58d", "width": 2}},
    )
    fig.update_layout(
        barmode="group",
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(3,20,16,0.45)",
        font={"color": "#effff8"},
        legend={"orientation": "h", "y": 1.05, "x": 0.55},
        margin={"l": 24, "r": 24, "t": 44, "b": 24},
        xaxis={"gridcolor": "rgba(0,245,141,0.12)"},
        yaxis={"gridcolor": "rgba(0,245,141,0.12)"},
    )
    st.plotly_chart(fig, width="stretch")


def plot_heatmap():
    pivot = heatmap_df.pivot(index="Supplier", columns="Risk Vector", values="Risk")
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[[0, "#00f58d"], [0.5, "#ffc928"], [1, "#ff4f62"]],
            zmin=0,
            zmax=100,
            colorbar={"title": "Risk"},
        )
    )
    fig.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(3,20,16,0.45)",
        font={"color": "#effff8"},
        margin={"l": 20, "r": 20, "t": 28, "b": 20},
    )
    st.plotly_chart(fig, width="stretch")


def plot_world_map():
    colors = {"High": "#ff4f62", "Medium": "#ffc928", "Low": "#00f58d"}
    fig = go.Figure()
    for level, data in SUPPLIER_RISK.groupby("level"):
        fig.add_trace(
            go.Scattergeo(
                lon=data["lon"],
                lat=data["lat"],
                text=data["name"] + "<br>Risk: " + data["risk"].astype(str) + "%",
                mode="markers",
                name=level,
                marker={
                    "size": data["risk"] / 3 + 10,
                    "color": colors[level],
                    "line": {"color": "#effff8", "width": 1},
                    "opacity": 0.86,
                },
            )
        )
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#083429",
        showocean=True,
        oceancolor="#02110e",
        showcountries=True,
        countrycolor="rgba(0,245,141,0.22)",
        showcoastlines=True,
        coastlinecolor="rgba(0,245,141,0.25)",
    )
    fig.update_layout(
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#effff8"},
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        legend={"orientation": "h", "y": 0.02, "x": 0.02},
    )
    st.plotly_chart(fig, width="stretch")


def plot_network():
    labels = [
        "Tier-2 Raw Material",
        "Tier-1 Supplier",
        "Port / Logistics",
        "Warehouse",
        "Distribution Center",
        "Retail Demand",
        "Backup Supplier",
    ]
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node={
                    "pad": 20,
                    "thickness": 18,
                    "line": {"color": "rgba(0,245,141,0.35)", "width": 1},
                    "label": labels,
                    "color": ["#00f58d", "#ffc928", "#ff4f62", "#00d6d6", "#1f85ff", "#effff8", "#00f58d"],
                },
                link={
                    "source": [0, 1, 2, 3, 4, 6],
                    "target": [1, 2, 3, 4, 5, 4],
                    "value": [8, 8, 7, 6, 6, 3],
                    "color": [
                        "rgba(0,245,141,0.28)",
                        "rgba(255,201,40,0.32)",
                        "rgba(255,79,98,0.42)",
                        "rgba(0,214,214,0.28)",
                        "rgba(31,133,255,0.28)",
                        "rgba(0,245,141,0.22)",
                    ],
                },
            )
        ]
    )
    fig.update_layout(
        height=410,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#effff8", "size": 12},
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
    )
    st.plotly_chart(fig, width="stretch")


def copilot_response(question):
    q = question.lower()
    if "spike" in q or "caused" in q or "why" in q:
        return (
            f"Today's risk spike is mainly driven by {event}: {event_meta['driver']}. "
            f"The digital twin estimates a {event_meta['delay']}-day delay, "
            f"{event_meta['skus']} affected SKUs, and ${predicted_revenue_loss:,.0f} in exposure."
        )
    if "supplier" in q or "vulnerable" in q:
        top = SUPPLIER_RISK.sort_values("risk", ascending=False).iloc[0]
        return (
            f"The most vulnerable node is {top['name']} with {top['risk']}% risk. "
            f"Recommended mitigation: activate {event_meta['backup']} and increase safety stock for high-margin SKUs."
        )
    if "worsens" in q or "what happens" in q or "simulate" in q:
        worsened_loss = predicted_revenue_loss * 1.35
        return (
            f"If the disruption worsens, expected delay may rise to {event_meta['delay'] + 2} days, "
            f"affected SKUs may increase to {event_meta['skus'] + 5}, and exposure can reach "
            f"${worsened_loss:,.0f}. Trigger: {response_action}."
        )
    return (
        f"SupplyShield is tracking {event_meta['location']} from {event_meta['feed']}. "
        f"Current recommendation is {recommendation}, with backup path: {event_meta['backup']}."
    )


# ==================================================
# PAGES
# ==================================================

if page == "Command Center":
    render_hero()
    render_metric_cards()

    left, right = st.columns([1.05, 1])
    with left:
        render_alerts()
        st.markdown('<div class="section-label">Supply Impact Analysis</div>', unsafe_allow_html=True)
        plot_supply_impact()
    with right:
        st.markdown('<div class="section-label">Executive Decision Panel</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="status-panel neon-green">
                <div class="status-title">Recommended Automated Response</div>
                <div class="status-value">{response_action}</div>
                <div class="status-copy">
                    Backup supplier: {event_meta['backup']} | Risk level:
                    <span style="color:{risk_color}; font-weight:850;">{risk}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-label">Forecast Confidence</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="status-panel neon-teal">
                <div class="status-title">95% Confidence Range</div>
                <div class="status-value">${lower:,.2f} to ${upper:,.2f}</div>
                <div class="status-copy">Residual standard deviation: {residual_std:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-label">Current Scenario Summary</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="status-panel">
                <div class="summary-grid">
                    <div class="summary-item"><div class="summary-k">Event</div><div class="summary-v">{event}</div></div>
                    <div class="summary-item"><div class="summary-k">Feed</div><div class="summary-v">{event_meta['feed']}</div></div>
                    <div class="summary-item"><div class="summary-k">Affected SKUs</div><div class="summary-v">{event_meta['skus']}</div></div>
                    <div class="summary-item"><div class="summary-k">Suppliers</div><div class="summary-v">{event_meta['suppliers']}</div></div>
                    <div class="summary-item"><div class="summary-k">Remaining Supply</div><div class="summary-v">{remaining_supply:,.0f}</div></div>
                    <div class="summary-item"><div class="summary-k">Unmet Demand</div><div class="summary-v">{estimated_loss:,.0f}</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-label">Risk Heatmap</div>', unsafe_allow_html=True)
    plot_heatmap()

elif page == "Global Map":
    render_hero()
    st.markdown('<div class="section-label">Live Global Supply Network</div>', unsafe_allow_html=True)
    plot_world_map()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="section-label">Supply Chain Network Graph</div>', unsafe_allow_html=True)
        plot_network()
    with c2:
        render_alerts()

elif page == "Digital Twin":
    render_hero()
    st.markdown('<div class="section-label">What-If Digital Twin Simulator</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Expected Delay", f"{event_meta['delay']} days")
    c2.metric("Affected Suppliers", event_meta["suppliers"])
    c3.metric("Affected SKUs", event_meta["skus"])
    c4.metric("Revenue Exposure", f"${predicted_revenue_loss / 1000:,.0f}K")

    left, right = st.columns([1, 1])
    with left:
        st.markdown(
            f"""
            <div class="status-panel neon-amber">
                <div class="status-title">Simulation Output</div>
                <div class="status-value">{event_meta['location']}</div>
                <div class="status-copy">
                    Event driver: {event_meta['driver']}<br>
                    Impact severity: {impact_percent}%<br>
                    Recommended backup: {event_meta['backup']}<br>
                    Automated response: {response_action}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-label">Supply Impact</div>', unsafe_allow_html=True)
        plot_supply_impact()
    with right:
        st.markdown('<div class="section-label">Supplier Risk Heatmap</div>', unsafe_allow_html=True)
        plot_heatmap()

elif page == "AI Copilot":
    render_hero()
    st.markdown('<div class="section-label">Ask SupplyShield AI</div>', unsafe_allow_html=True)
    question = st.text_input(
        "Ask a supply-chain risk question",
        value="What caused today's risk spike?",
        placeholder="Example: Which supplier is most vulnerable?",
    )
    st.markdown(
        f"""
        <div class="copilot-answer">
            <strong>SupplyShield Copilot:</strong><br>
            {copilot_response(question)}
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="section-label">Top Forecast Drivers</div>', unsafe_allow_html=True)
        st.dataframe(importance.head(10), width="stretch", hide_index=True)
    with c2:
        render_alerts()

elif page == "Architecture":
    render_hero()
    st.markdown('<div class="section-label">Winning Architecture Stack</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="status-panel neon-green">
            <div class="status-title">SupplyShield AI Flow</div>
            <div class="status-copy">
                M5-style demand signals -> XGBoost forecasting -> confidence interval ->
                risk classification -> SHAP-ready evidence layer -> event intelligence ->
                supply-chain digital twin -> scenario simulator -> AI recommendation engine ->
                executive command center.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    arch = pd.DataFrame(
        [
            ["Demand Forecasting", "XGBoost model", "Implemented"],
            ["Conformal / Uncertainty", "Residual interval + MAPIE script", "Implemented"],
            ["Risk Classification", "Low / Medium / High triage", "Implemented"],
            ["Event Intelligence", "Weather, cyber, port, traffic, disaster feeds", "Prototype layer"],
            ["Digital Twin", "Delay, SKU, supplier, and loss simulator", "Implemented"],
            ["Global Map", "Supplier, port, warehouse risk pins", "Implemented"],
            ["AI Copilot", "Local decision assistant; API-ready", "Implemented"],
            ["Automated Response", "Recommended action + backup path", "Implemented"],
        ],
        columns=["Capability", "Stack", "Status"],
    )
    st.dataframe(arch, width="stretch", hide_index=True)
    st.markdown('<div class="section-label">Supply Chain Network Graph</div>', unsafe_allow_html=True)
    plot_network()

st.markdown(
    '<div style="color:#8fb7a9; text-align:center; padding:1.1rem 0 0.3rem;">SupplyShield AI | Digital Twin + Event Intelligence + Decision Automation</div>',
    unsafe_allow_html=True,
)
