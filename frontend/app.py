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
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
    min-height: 100vh;
}

/* SVG Logo Animation */
.logo-svg text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 110px;
    fill: transparent;
    stroke: #FF6B35;
    stroke-width: 2px;
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    animation: draw 2.5s ease forwards, fill-in 1s ease 2.5s forwards;
    letter-spacing: 8px;
}

@keyframes draw {
    to { stroke-dashoffset: 0; }
}

@keyframes fill-in {
    to {
        fill: #FF6B35;
        stroke: transparent;
    }
}

/* Pulsing underline */
.logo-underline {
    width: 80px;
    height: 4px;
    background: #FF6B35;
    border-radius: 2px;
    margin: 10px 0 20px 0;
    animation: pulse-width 2s ease-in-out infinite;
    animation-delay: 3s;
    opacity: 0;
    animation-fill-mode: forwards;
}

@keyframes pulse-width {
    0% { width: 80px; opacity: 1; }
    50% { width: 160px; opacity: 0.7; }
    100% { width: 80px; opacity: 1; }
}

@keyframes fadeIn {
    to { opacity: 1; }
}

.tagline {
    font-size: 12px;
    color: #777777;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    opacity: 0;
    animation: fadeIn 1s ease 3s forwards;
}

.hero-text {
    font-size: 17px;
    color: #aaaaaa;
    margin-bottom: 30px;
    opacity: 0;
    animation: fadeIn 1s ease 3.2s forwards;
}

/* Input styling */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 20px rgba(255, 107, 53, 0.2) !important;
}

/* Radio buttons */
div[data-testid="stRadio"] label {
    color: #cccccc !important;
    font-size: 15px !important;
}

/* Animated button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #FF6B35, #e55a25) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 14px 40px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    transform: translateY(0px) !important;
    box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3) !important;
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 35px rgba(255, 107, 53, 0.5) !important;
    background: linear-gradient(135deg, #ff7d4d, #FF6B35) !important;
    letter-spacing: 4px !important;
}

div[data-testid="stButton"] button:active {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4) !important;
}

/* Verdict cards */
.verdict-credible {
    background: linear-gradient(135deg, #0d2a1a, #1a3a2a);
    border: 1px solid #00cc66;
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #00cc66;
    margin: 20px 0;
    animation: slideIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    box-shadow: 0 0 40px rgba(0, 204, 102, 0.15);
    letter-spacing: 2px;
}

.verdict-suspicious {
    background: linear-gradient(135deg, #2a2a0d, #3a3a1a);
    border: 1px solid #ffcc00;
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #ffcc00;
    margin: 20px 0;
    animation: slideIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    box-shadow: 0 0 40px rgba(255, 204, 0, 0.15);
    letter-spacing: 2px;
}

.verdict-misleading {
    background: linear-gradient(135deg, #2a0d0d, #3a1a1a);
    border: 1px solid #FF6B35;
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #FF6B35;
    margin: 20px 0;
    animation: slideIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    box-shadow: 0 0 40px rgba(255, 107, 53, 0.15);
    letter-spacing: 2px;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(40px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

/* Metric boxes */
div[data-testid="metric-container"] {
    background: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 12px !important;
    padding: 16px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(255, 107, 53, 0.1) !important;
    border-color: #FF6B35 !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stExpander"]:hover {
    border-color: #FF6B35 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.1) !important;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1f1f1f;
    margin: 30px 0;
}

h1, h2, h3, h4 {
    color: #ffffff !important;
}

p, label {
    color: #cccccc !important;
}

.footer {
    text-align: center;
    color: #333333;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 40px;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Hero Section with SVG animated logo
st.markdown("""
<div style="padding: 40px 0 10px 0;">
    <svg class="logo-svg" width="100%" height="130" viewBox="0 0 700 120">
        <text x="50%" y="100" text-anchor="middle">TRUTHLENS</text>
    </svg>
    <div class="logo-underline"></div>
    <div class="tagline">AI-Powered Misinformation Detector</div>
    <div class="hero-text">Fact-check any news article or ask a question about current events.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

mode = st.radio("", ["Analyze an article", "Ask a question"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)


def display_results(result):
    score = result["overall_score"]
    verdict = result["overall_verdict"]

    if verdict == "CREDIBLE":
        st.markdown(
            f'<div class="verdict-credible">✅ {verdict} — {score}/100</div>',
            unsafe_allow_html=True
        )
    elif verdict == "SUSPICIOUS":
        st.markdown(
            f'<div class="verdict-suspicious">⚠️ {verdict} — {score}/100</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="verdict-misleading">❌ {verdict} — {score}/100</div>',
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Supported", result["supported"])
    col2.metric("❌ Contradicted", result["contradicted"])
    col3.metric("⚠️ Insufficient", result["insufficient"])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Claim-by-Claim Breakdown")

    for i, claim in enumerate(result["claim_results"], 1):
        with st.expander(f"Claim {i}: {claim['claim'][:80]}..."):
            if claim["verdict"] == "SUPPORTED":
                st.success(f"✅ {claim['verdict']}")
            elif claim["verdict"] == "CONTRADICTED":
                st.error(f"❌ {claim['verdict']}")
            else:
                st.warning(f"⚠️ {claim['verdict']}")

            st.write(f"**Confidence:** {claim['confidence']}%")
            st.write(f"**Explanation:** {claim['explanation']}")
            st.markdown("**Evidence used:**")
            for evidence in claim["evidence"]:
                st.caption(f"• {evidence}")


if mode == "Analyze an article":
    input_type = st.radio("Input type", ["URL", "Text"], horizontal=True)

    if input_type == "URL":
        user_input = st.text_input("", placeholder="https://www.bbc.com/news/article...")
    else:
        user_input = st.text_area("", placeholder="Paste article text here...", height=200)

    if st.button("ANALYZE", type="primary"):
        if not user_input:
            st.error("Please enter a URL or text.")
        else:
            with st.spinner("Analyzing article..."):
                try:
                    if input_type == "URL":
                        response = requests.post(
                            f"{API_URL}/analyze",
                            json={"url": user_input}
                        )
                    else:
                        response = requests.post(
                            f"{API_URL}/analyze",
                            json={"text": user_input}
                        )
                    result = response.json()
                    display_results(result)
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    question = st.text_input("", placeholder="Is the Iran negotiation going well?")

    if st.button("SEARCH & ANALYZE", type="primary"):
        if not question:
            st.error("Please enter a question.")
        else:
            with st.spinner("Searching news and analyzing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/question",
                        json={"question": question}
                    )
                    result = response.json()
                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    display_results(result)
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<div class="footer">Built by Sai Teja Appani &nbsp;·&nbsp; MS CS @ University of Florida</div>',
    unsafe_allow_html=True
)