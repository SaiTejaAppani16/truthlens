import streamlit as st
import requests

API_URL = "https://truthlens-siwz.onrender.com"

st.set_page_config(
    page_title="TruthLens",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 TruthLens")
st.subheader("AI-Powered Misinformation Detector")
st.markdown("Fact-check any news article or ask a question about current events.")

mode = st.radio("What do you want to do?", ["Analyze an article", "Ask a question"])

if mode == "Analyze an article":
    input_type = st.radio("Input type", ["URL", "Text"])

    if input_type == "URL":
        user_input = st.text_input("Enter article URL")
    else:
        user_input = st.text_area("Paste article text", height=200)

    if st.button("Analyze", type="primary"):
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
                    score = result["overall_score"]
                    verdict = result["overall_verdict"]

                    if verdict == "CREDIBLE":
                        st.success(f"✅ {verdict} — Score: {score}/100")
                    elif verdict == "SUSPICIOUS":
                        st.warning(f"⚠️ {verdict} — Score: {score}/100")
                    else:
                        st.error(f"❌ {verdict} — Score: {score}/100")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Supported", result["supported"])
                    col2.metric("Contradicted", result["contradicted"])
                    col3.metric("Insufficient", result["insufficient"])

                    st.markdown("---")
                    st.subheader("Claim-by-Claim Breakdown")

                    for i, claim in enumerate(result["claim_results"], 1):
                        with st.expander(f"Claim {i}: {claim['claim'][:80]}..."):
                            if claim["verdict"] == "SUPPORTED":
                                st.success(f"Verdict: {claim['verdict']}")
                            elif claim["verdict"] == "CONTRADICTED":
                                st.error(f"Verdict: {claim['verdict']}")
                            else:
                                st.warning(f"Verdict: {claim['verdict']}")

                            st.write(f"**Confidence:** {claim['confidence']}%")
                            st.write(f"**Explanation:** {claim['explanation']}")
                            st.markdown("**Evidence used:**")
                            for evidence in claim["evidence"]:
                                st.caption(f"• {evidence}")

                except Exception as e:
                    st.error(f"Error connecting to API: {e}")

else:
    question = st.text_input("Ask a question about current events",
                             placeholder="Is the Iran negotiation going well?")

    if st.button("Search & Analyze", type="primary"):
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
                    score = result["overall_score"]
                    verdict = result["overall_verdict"]

                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown("---")

                    if verdict == "CREDIBLE":
                        st.success(f"✅ {verdict} — Score: {score}/100")
                    elif verdict == "SUSPICIOUS":
                        st.warning(f"⚠️ {verdict} — Score: {score}/100")
                    else:
                        st.error(f"❌ {verdict} — Score: {score}/100")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Supported", result["supported"])
                    col2.metric("Contradicted", result["contradicted"])
                    col3.metric("Insufficient", result["insufficient"])

                    st.markdown("---")
                    st.subheader("Claim-by-Claim Breakdown")

                    for i, claim in enumerate(result["claim_results"], 1):
                        with st.expander(f"Claim {i}: {claim['claim'][:80]}..."):
                            if claim["verdict"] == "SUPPORTED":
                                st.success(f"Verdict: {claim['verdict']}")
                            elif claim["verdict"] == "CONTRADICTED":
                                st.error(f"Verdict: {claim['verdict']}")
                            else:
                                st.warning(f"Verdict: {claim['verdict']}")

                            st.write(f"**Confidence:** {claim['confidence']}%")
                            st.write(f"**Explanation:** {claim['explanation']}")
                            st.markdown("**Evidence used:**")
                            for evidence in claim["evidence"]:
                                st.caption(f"• {evidence}")

                except Exception as e:
                    st.error(f"Error: {e}")