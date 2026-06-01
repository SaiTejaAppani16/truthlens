import streamlit as st
import requests

API_URL = "https://truthlens-siwz.onrender.com"

st.set_page_config(
    page_title="TruthLens",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700;900&display=swap');

:root {
    --orange: #FF4500;
    --orange-dim: #cc3700;
    --bg: #080808;
    --surface: #0f0f0f;
    --border: #1c1c1c;
    --text: #e8e8e8;
    --muted: #555555;
    --green: #00e676;
    --yellow: #ffd600;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: var(--bg);
    background-image: 
        radial-gradient(ellipse at 20% 0%, rgba(255,69,0,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(255,69,0,0.04) 0%, transparent 60%);
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── HERO ── */
.hero {
    padding: 56px 0 32px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}

.eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 4px;
    color: var(--orange);
    text-transform: uppercase;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px;
    height: 1px;
    background: var(--orange);
}

.logo-wrap {
    overflow: hidden;
    margin-bottom: 8px;
}

.logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(72px, 14vw, 130px);
    line-height: 0.9;
    letter-spacing: 6px;
    color: transparent;
    -webkit-text-stroke: 1.5px var(--orange);
    animation: fill-logo 0.8s cubic-bezier(0.16,1,0.3,1) 0.3s forwards;
    display: block;
}

@keyframes fill-logo {
    0%   { color: transparent; -webkit-text-stroke: 1.5px var(--orange); letter-spacing: 20px; opacity: 0.3; }
    60%  { color: transparent; -webkit-text-stroke: 1.5px var(--orange); }
    100% { color: var(--orange); -webkit-text-stroke: 1.5px transparent; letter-spacing: 6px; opacity: 1; }
}

.logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 12px;
    animation: fadein 1s ease 1s both;
}

@keyframes fadein {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: none; }
}

/* ── TICKER ── */
.ticker-wrap {
    overflow: hidden;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 8px 0;
    margin: 24px 0 32px 0;
    animation: fadein 1s ease 1.2s both;
}

.ticker {
    display: inline-block;
    white-space: nowrap;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
    animation: scroll-ticker 30s linear infinite;
}

.ticker span { color: var(--orange); margin: 0 6px; }

@keyframes scroll-ticker {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}

/* ── MODE TABS ── */
.mode-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 12px;
}

div[data-testid="stRadio"] {
    animation: fadein 0.6s ease 1.4s both;
}

div[data-testid="stRadio"] > div {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    padding: 10px 20px !important;
    border-radius: 2px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    color: var(--orange) !important;
    border-color: var(--orange) !important;
    background: rgba(255,69,0,0.06) !important;
}

/* ── INPUTS ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(255,69,0,0.1) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: var(--muted) !important;
    font-size: 12px !important;
}

/* ── BUTTON ── */
div[data-testid="stButton"] button {
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    padding: 16px 32px !important;
    width: 100% !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stButton"] button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.15) 50%, transparent 100%);
    transform: translateX(-100%);
    transition: transform 0.4s ease;
}

div[data-testid="stButton"] button:hover {
    background: var(--orange-dim) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,69,0,0.35) !important;
}

div[data-testid="stButton"] button:hover::after {
    transform: translateX(100%);
}

div[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

/* ── VERDICT ── */
.verdict {
    border-radius: 2px;
    padding: 28px 32px;
    margin: 28px 0;
    animation: verdict-in 0.5s cubic-bezier(0.16,1,0.3,1) forwards;
    position: relative;
    overflow: hidden;
}

.verdict::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
}

.verdict-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 8px;
    opacity: 0.7;
}

.verdict-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 48px;
    letter-spacing: 4px;
    line-height: 1;
}

.verdict-score {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    margin-top: 8px;
    opacity: 0.8;
}

.verdict-credible {
    background: rgba(0,230,118,0.05);
    border: 1px solid rgba(0,230,118,0.2);
    color: var(--green);
}
.verdict-credible::before { background: var(--green); }

.verdict-suspicious {
    background: rgba(255,214,0,0.05);
    border: 1px solid rgba(255,214,0,0.2);
    color: var(--yellow);
}
.verdict-suspicious::before { background: var(--yellow); }

.verdict-misleading {
    background: rgba(255,69,0,0.05);
    border: 1px solid rgba(255,69,0,0.2);
    color: var(--orange);
}
.verdict-misleading::before { background: var(--orange); }

@keyframes verdict-in {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: none; }
}

/* ── METRICS ── */
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    padding: 20px !important;
    transition: border-color 0.2s ease !important;
}

div[data-testid="metric-container"]:hover {
    border-color: var(--orange) !important;
}

div[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 40px !important;
    color: var(--text) !important;
}

/* ── EXPANDER ── */
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    margin-bottom: 8px !important;
    transition: border-color 0.2s ease !important;
}

div[data-testid="stExpander"]:hover {
    border-color: rgba(255,69,0,0.4) !important;
}

div[data-testid="stExpander"] summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: var(--text) !important;
}

/* ── DIVIDER ── */
.rule {
    border: none;
    border-top: 1px solid var(--border);
    margin: 36px 0;
}

/* ── SECTION LABEL ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── FOOTER ── */
.footer {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    text-align: center;
    padding: 32px 0 48px;
    border-top: 1px solid var(--border);
    margin-top: 48px;
}

h1,h2,h3 { color: var(--text) !important; }
p, label { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="eyebrow">Verification Engine</div>
    <div class="logo-wrap">
        <span class="logo">TRUTHLENS</span>
    </div>
    <div class="logo-sub">AI-Powered Misinformation Detector</div>
</div>

<div class="ticker-wrap">
    <div class="ticker">
        FACT&nbsp;·&nbsp;CHECK&nbsp;·&nbsp;VERIFY&nbsp;·&nbsp;ANALYZE&nbsp;<span>◆</span>&nbsp;
        RAG&nbsp;PIPELINE&nbsp;<span>◆</span>&nbsp;CHROMADB&nbsp;<span>◆</span>&nbsp;
        CLAUDE&nbsp;API&nbsp;<span>◆</span>&nbsp;NEWSAPI&nbsp;<span>◆</span>&nbsp;
        REAL&nbsp;TIME&nbsp;ANALYSIS&nbsp;<span>◆</span>&nbsp;
        FACT&nbsp;·&nbsp;CHECK&nbsp;·&nbsp;VERIFY&nbsp;·&nbsp;ANALYZE&nbsp;<span>◆</span>&nbsp;
        RAG&nbsp;PIPELINE&nbsp;<span>◆</span>&nbsp;CHROMADB&nbsp;<span>◆</span>&nbsp;
        CLAUDE&nbsp;API&nbsp;<span>◆</span>&nbsp;NEWSAPI&nbsp;<span>◆</span>&nbsp;
        REAL&nbsp;TIME&nbsp;ANALYSIS&nbsp;<span>◆</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MODE ──
st.markdown('<div class="mode-label">Select Mode</div>', unsafe_allow_html=True)
mode = st.radio("", ["Analyze an article", "Ask a question"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)


def display_results(result):
    score = result["overall_score"]
    verdict = result["overall_verdict"]

    if verdict == "CREDIBLE":
        cls = "verdict-credible"
        icon = "✓"
    elif verdict == "SUSPICIOUS":
        cls = "verdict-suspicious"
        icon = "⚠"
    else:
        cls = "verdict-misleading"
        icon = "✕"

    st.markdown(f"""
    <div class="verdict {cls}">
        <div class="verdict-label">Verdict</div>
        <div class="verdict-text">{icon}&nbsp;{verdict}</div>
        <div class="verdict-score">Credibility Score — {score} / 100</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Supported", result["supported"])
    col2.metric("Contradicted", result["contradicted"])
    col3.metric("Insufficient", result["insufficient"])

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Claim Analysis</div>', unsafe_allow_html=True)

    for i, claim in enumerate(result["claim_results"], 1):
        with st.expander(f"#{i:02d} — {claim['claim'][:75]}..."):
            if claim["verdict"] == "SUPPORTED":
                st.success(f"✓ {claim['verdict']}")
            elif claim["verdict"] == "CONTRADICTED":
                st.error(f"✕ {claim['verdict']}")
            else:
                st.warning(f"⚠ {claim['verdict']}")
            st.write(f"**Confidence:** {claim['confidence']}%")
            st.write(f"**Explanation:** {claim['explanation']}")
            st.markdown("**Evidence:**")
            for e in claim["evidence"]:
                st.caption(f"› {e}")


if mode == "Analyze an article":
    input_type = st.radio("Input type", ["URL", "Text"], horizontal=True)
    if input_type == "URL":
        user_input = st.text_input("", placeholder="paste article url here...")
    else:
        user_input = st.text_area("", placeholder="paste article text here...", height=180)

    if st.button("RUN ANALYSIS", type="primary"):
        if not user_input:
            st.error("Please enter a URL or text.")
        else:
            with st.spinner("Running analysis..."):
                try:
                    key = "url" if input_type == "URL" else "text"
                    response = requests.post(f"{API_URL}/analyze", json={key: user_input})
                    display_results(response.json())
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    question = st.text_input("", placeholder="is the iran negotiation going well?")
    if st.button("SEARCH & ANALYZE", type="primary"):
        if not question:
            st.error("Please enter a question.")
        else:
            with st.spinner("Searching and analyzing..."):
                try:
                    response = requests.post(f"{API_URL}/question", json={"question": question})
                    result = response.json()
                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown('<hr class="rule">', unsafe_allow_html=True)
                    display_results(result)
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("""
<div class="footer">
    Built by Sai Teja Appani &nbsp;·&nbsp; MS CS @ University of Florida &nbsp;·&nbsp; 
    <a href="https://github.com/SaiTejaAppani16/truthlens" 
       style="color:#FF4500;text-decoration:none;">GitHub</a>
</div>
""", unsafe_allow_html=True)