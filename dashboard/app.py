import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import random

st.set_page_config(
    page_title="IOB NeuralGuard | SOC",
    layout="wide",
    page_icon="https://www.iob.in/favicon.ico"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background-color: #0b0e13; }
.block-container { padding: 0 1.5rem 1rem 1.5rem !important; }
[data-testid="stSidebar"] { background-color: #0e1219 !important; border-right: 1px solid #1e2530 !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
div[data-testid="stMetric"] {
    background: #111621; border: 1px solid #1e2530;
    border-radius: 4px; padding: 12px 16px !important;
}
div[data-testid="stMetric"] label {
    color: #4a5568 !important; font-size: 0.68rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase; letter-spacing: 0.1em;
}
div[data-testid="stMetricValue"] {
    color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.55rem !important; font-weight: 500 !important;
}
div[data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important; }
.stDataFrame { border: 1px solid #1e2530 !important; border-radius: 4px !important; }
iframe { border-radius: 4px; }
div[data-testid="stCaption"] p {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #2d3748; letter-spacing: 0.04em;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# SIDEBAR — split into small blocks to avoid Streamlit render limits
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:

    # Logo
    st.markdown("""
<div style="padding:18px 16px 14px 16px; border-bottom:1px solid #1e2530; margin-bottom:4px;">
  <div style="display:flex; align-items:center; gap:12px;">
    <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
      <rect width="40" height="40" rx="6" fill="#0f3460"/>
      <text x="20" y="23" text-anchor="middle" font-family="Inter,sans-serif"
        font-weight="600" font-size="13" fill="#ffffff" letter-spacing="1.2">IOB</text>
      <rect x="6" y="29" width="28" height="2" rx="1" fill="#e8a020"/>
    </svg>
    <div>
      <div style="color:#e2e8f0; font-size:0.88rem; font-weight:600;">NeuralGuard</div>
      <div style="color:#3a7bd5; font-size:0.6rem; letter-spacing:0.14em; font-family:'JetBrains Mono',monospace; margin-top:2px;">FRAUD INTELLIGENCE v1.0</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Engine Status label
    st.markdown("""
<div style="padding:12px 16px 6px 16px;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:0.59rem; color:#374151;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:8px; border-left:2px solid #1e3a5f; padding-left:6px;">
    Engine Status
  </div>
</div>
""", unsafe_allow_html=True)

    # Engine rows — each one separately so Streamlit doesn't choke
    def engine_row(label, tag, color_bg, color_border, color_dot, color_text, color_tag):
        st.markdown(f"""
<div style="margin:0 16px 4px 16px; display:flex; align-items:center; gap:8px;
  padding:6px 10px; background:{color_bg}; border:1px solid {color_border}; border-radius:3px;">
  <div style="width:6px; height:6px; border-radius:50%; background:{color_dot}; flex-shrink:0;"></div>
  <span style="font-family:'JetBrains Mono',monospace; font-size:0.67rem; color:{color_text};">{label}</span>
  <span style="margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:0.59rem; color:{color_tag};">{tag}</span>
</div>
""", unsafe_allow_html=True)

    engine_row("FastAPI Orchestrator", ":8000",   "#0b1a0e","#1a3320","#22c55e","#86efac","#166534")
    engine_row("Apache Kafka",         "INGEST",  "#0b1a0e","#1a3320","#22c55e","#86efac","#166534")
    engine_row("Redis Speed Gate",     "&lt;2ms", "#0b1a0e","#1a3320","#22c55e","#86efac","#166534")
    engine_row("Mule Hunter (Neo4j)",  "ONLINE",  "#0b1a0e","#1a3320","#22c55e","#86efac","#166534")
    engine_row("Voice Shield (Librosa)","ONLINE", "#0b1a0e","#1a3320","#22c55e","#86efac","#166534")

    # Active Rule Engines label
    st.markdown("""
<div style="padding:12px 16px 6px 16px; margin-top:6px; border-top:1px solid #1e2530;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:0.59rem; color:#374151;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:8px; border-left:2px solid #78350f; padding-left:6px;">
    Active Rule Engines
  </div>
</div>
""", unsafe_allow_html=True)

    engine_row("Velocity Gate (Redis)",       "5/min",  "#12100a","#2a2310","#f59e0b","#fcd34d","#78350f")
    engine_row("Spectral Flatness (Librosa)", "123Pay", "#12100a","#2a2310","#f59e0b","#fcd34d","#78350f")
    engine_row("Star Topology (Neo4j)",       "RING",   "#12100a","#2a2310","#f59e0b","#fcd34d","#78350f")

    # Protected Channels
    st.markdown("""
<div style="padding:12px 16px 6px 16px; margin-top:6px; border-top:1px solid #1e2530;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:0.59rem; color:#374151;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:10px; border-left:2px solid #1e3a5f; padding-left:6px;">
    Protected IOB Channels
  </div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:0.64rem; color:#4b5563; line-height:2;">
    UPI / 123Pay &nbsp;&nbsp;&nbsp;&nbsp;(NPCI Gateway)<br>
    IOB Nanban &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Mobile App)<br>
    IOB NetBanking &nbsp;(Retail + Corp)<br>
    ATM / POS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(FSS Switch)<br>
    Branch Teller &nbsp;&nbsp;(Finacle Core)<br>
    NEFT / RTGS / IMPS
  </div>
</div>
""", unsafe_allow_html=True)

    # Fail-Open
    st.markdown("""
<div style="margin:10px 16px 16px 16px; border-top:1px solid #1e2530; padding-top:10px;">
  <div style="display:flex; align-items:center; gap:8px; padding:8px 10px;
    background:#0b1a0e; border:1px solid #166534; border-radius:3px;">
    <div style="width:6px; height:6px; border-radius:50%; background:#22c55e; flex-shrink:0;"></div>
    <div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:0.67rem; color:#86efac;">Fail-Open: ACTIVE</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:0.59rem; color:#166534; margin-top:2px;">
        Timeout &gt;200ms &#8594; auto ALLOW
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:14px;
  padding:14px 0 12px 0; border-bottom:1px solid #1e2530; margin-bottom:14px;">
  <svg width="36" height="36" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
    <rect width="36" height="36" rx="5" fill="#0f3460"/>
    <text x="18" y="21" text-anchor="middle" font-family="Inter,sans-serif"
      font-weight="600" font-size="11" fill="#ffffff" letter-spacing="1">IOB</text>
    <rect x="5" y="27" width="26" height="1.8" rx="0.9" fill="#e8a020"/>
  </svg>
  <div style="border-right:1px solid #1e2530; padding-right:14px;">
    <div style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Indian Overseas Bank</div>
    <div style="font-size:0.59rem; color:#374151; letter-spacing:0.1em;
      font-family:'JetBrains Mono',monospace; text-transform:uppercase; margin-top:2px;">
      Chennai HQ &nbsp;·&nbsp; Treasury &amp; Risk Division
    </div>
  </div>
  <div>
    <span style="font-size:1.25rem; font-weight:300; color:#94a3b8;">NeuralGuard</span>
    <span style="font-size:1.25rem; font-weight:300; color:#334155;"> — Active Threat Intelligence</span>
  </div>
  <div style="margin-left:auto; display:flex; align-items:center; gap:7px;
    padding:5px 12px; border:1px solid #166534; border-radius:3px; background:#0b1a0e;">
    <div style="width:5px; height:5px; border-radius:50%; background:#22c55e;"></div>
    <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#4ade80; letter-spacing:0.1em;">LIVE</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────
CHANNELS = ['UPI / 123Pay','IOB Nanban','IOB NetBanking','ATM (FSS Switch)','Branch (Finacle)','NEFT / RTGS / IMPS']
THREAT_TYPES = ['None','Mule Ring','Velocity Spike','Voice Deepfake','Account Takeover']
ENGINES = ['Velocity Gate (Redis)','Mule Hunter (Neo4j)','Voice Shield (Librosa)','AI Router (Llama 3)']

def gen(n=120):
    now = pd.Timestamp.now()
    return pd.DataFrame({
        'Timestamp':   pd.date_range(end=now, periods=n, freq='30S'),
        'Channel':     np.random.choice(CHANNELS, n, p=[0.35,0.20,0.15,0.15,0.05,0.10]),
        'Amount_INR':  np.random.randint(500, 200000, n),
        'Risk_Score':  np.random.randint(10, 100, n),
        'Status':      np.random.choice(['ALLOWED','BLOCKED'], n, p=[0.83,0.17]),
        'Threat_Type': np.random.choice(THREAT_TYPES, n, p=[0.83,0.05,0.05,0.04,0.03]),
        'Latency_ms':  np.random.randint(18, 185, n),
        'Sender_Acct': [f"IOB{random.randint(10000000000,99999999999)}" for _ in range(n)],
        'Engine':      np.random.choice(ENGINES, n, p=[0.5,0.25,0.15,0.10]),
    })

def chart_layout(**extra):
    base = dict(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0e1219',
        font=dict(family="JetBrains Mono", color="#4b5563", size=10),
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor='#1e2530', linecolor='#1e2530', tickfont=dict(size=9)),
        yaxis=dict(gridcolor='#1e2530', linecolor='#1e2530', tickfont=dict(size=9)),
    )
    base.update(extra)
    return base

def section(label):
    st.markdown(f"""
<div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#374151;
  text-transform:uppercase; letter-spacing:0.14em; margin-bottom:8px;
  padding-left:8px; border-left:2px solid #1e3a5f;">
  {label}
</div>""", unsafe_allow_html=True)

placeholder = st.empty()

# ─────────────────────────────────────────────────────────────────────
# LIVE LOOP
# ─────────────────────────────────────────────────────────────────────
while True:
    df  = gen()
    blocked  = df[df['Status'] == 'BLOCKED']
    tps      = random.randint(1100, 1400)
    avg_lat  = int(df['Latency_ms'].mean())

    with placeholder.container():

        # KPIs
        k1,k2,k3,k4,k5 = st.columns(5)
        k1.metric("Live TPS",               f"{tps:,}",            delta=f"{random.randint(-30,60)}")
        k2.metric("Engine Latency",         f"{avg_lat} ms",       delta=f"{random.randint(-8,8)} ms",   delta_color="inverse")
        k3.metric("Threats Blocked (2H)",   len(blocked),          delta=f"+{random.randint(1,4)}",      delta_color="inverse")
        k4.metric("Mule Rings Detected",    random.randint(2,5),   delta="+1",                           delta_color="inverse")
        k5.metric("Fail-Open Triggers",     "0",                   delta="0")

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Charts
        c1,c2,c3 = st.columns([2.2,1.4,1.4])

        with c1:
            section("IOB Omni-Channel Traffic vs. Threat Interceptions")
            ch = df.groupby(['Channel','Status']).size().reset_index(name='Count')
            fig1 = px.bar(ch, x="Channel", y="Count", color="Status",
                color_discrete_map={"ALLOWED":"#1f6b45","BLOCKED":"#991b1b"},
                template="plotly_dark", barmode="group")
            fig1.update_layout(**chart_layout(
                legend=dict(orientation="h", y=1.1, font=dict(size=9))))
            fig1.update_traces(marker_line_width=0)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            section("Threat Vector Distribution")
            threats = df[df['Threat_Type'] != 'None']
            fig2 = px.pie(threats, names='Threat_Type', hole=0.6,
                color_discrete_sequence=['#7f1d1d','#78350f','#1e3a5f','#3b1e63'],
                template="plotly_dark")
            fig2.update_traces(
                textposition='inside', textinfo='percent+label',
                textfont=dict(size=8, color="#9ca3af"),
                marker=dict(line=dict(color='#0e1219', width=2)))
            fig2.update_layout(**chart_layout(showlegend=False,
                annotations=[dict(text=f"<b>{len(threats)}</b><br>alerts",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(color="#6b7280", family="JetBrains Mono", size=10))]))
            st.plotly_chart(fig2, use_container_width=True)

        with c3:
            section("Risk Score Distribution")
            fig3 = go.Figure()
            fig3.add_trace(go.Histogram(x=df[df['Status']=='BLOCKED']['Risk_Score'],
                name='Blocked', marker_color='#7f1d1d', opacity=0.9, nbinsx=15))
            fig3.add_trace(go.Histogram(x=df[df['Status']=='ALLOWED']['Risk_Score'],
                name='Allowed', marker_color='#1f6b45', opacity=0.5, nbinsx=15))
            fig3.update_layout(**chart_layout(barmode='overlay',
                legend=dict(orientation="h", y=1.1, font=dict(size=9)),
                xaxis=dict(title=dict(text="Risk Score", font=dict(size=9)), gridcolor='#1e2530', tickfont=dict(size=9)),
                yaxis=dict(title=dict(text="Count",      font=dict(size=9)), gridcolor='#1e2530', tickfont=dict(size=9))))
            fig3.update_traces(marker_line_width=0)
            st.plotly_chart(fig3, use_container_width=True)

        # Alert banner
        st.markdown("""
<div style="display:flex; align-items:center; gap:16px; background:#0f0505;
  border:1px solid #7f1d1d; border-left:3px solid #dc2626; border-radius:3px;
  padding:10px 16px; margin-bottom:10px;">
  <div style="flex-shrink:0;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem;
      color:#ef4444; letter-spacing:0.1em; text-transform:uppercase; font-weight:600;">
      &#9888;&nbsp; Critical &mdash; Mule Ring Active
    </div>
    <div style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#9ca3af; margin-top:4px;">
      Hub account&nbsp;
      <code style="background:#1e1010; padding:1px 5px; border-radius:2px;
        color:#fca5a5; font-family:'JetBrains Mono',monospace; font-size:0.75rem;">IOB98412XXXXXX</code>
      &nbsp;funnelling into 7 satellite accounts &nbsp;&middot;&nbsp;
      <span style="color:#d97706;">Mule Hunter (Neo4j)</span> confirmed Star Topology
      &nbsp;&middot;&nbsp; SAR auto-drafted for RBI
    </div>
  </div>
  <div style="margin-left:auto; text-align:right; white-space:nowrap; flex-shrink:0;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#374151;">Decision: 47ms</div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#166534; margin-top:2px;">Fail-Open: Safe</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Event log
        section("Live Interception Feed — IOB Payment Switch")

        recent = df.sort_values('Timestamp', ascending=False).head(15)[[
            'Timestamp','Channel','Sender_Acct','Amount_INR',
            'Risk_Score','Engine','Threat_Type','Status','Latency_ms'
        ]].copy()
        recent['Timestamp']  = recent['Timestamp'].dt.strftime('%H:%M:%S')
        recent['Amount_INR'] = recent['Amount_INR'].apply(lambda x: f"\u20b9{x:,}")
        recent['Latency_ms'] = recent['Latency_ms'].apply(lambda x: f"{x}ms")

        styled = recent.style \
            .applymap(lambda v: 'color:#ef4444;font-weight:600' if v=='BLOCKED' else 'color:#22c55e;',         subset=['Status']) \
            .applymap(lambda v: 'color:#f59e0b;font-weight:500' if v!='None'    else 'color:#374151;',         subset=['Threat_Type']) \
            .applymap(lambda _: 'color:#3b82f6;font-family:JetBrains Mono,monospace;font-size:0.75rem',        subset=['Engine']) \
            .applymap(lambda _: 'font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#4b5563',        subset=['Timestamp','Latency_ms','Risk_Score']) \
            .applymap(lambda _: 'font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#6b7280',        subset=['Sender_Acct'])

        st.dataframe(styled, use_container_width=True, height=350)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.caption(
            f"IOB NeuralGuard v1.0  ·  Sidecar — Zero impact on Finacle Core  ·  "
            f"Air-Gapped · RBI Compliant  ·  All decisions <200ms  ·  "
            f"Refresh {pd.Timestamp.now().strftime('%H:%M:%S')} IST"
        )

    time.sleep(4)