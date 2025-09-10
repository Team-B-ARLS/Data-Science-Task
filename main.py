import streamlit as st
import pandas as pd
import time
import google.generativeai as genai
from backend import predict_campaign_revenue, to_excel
from streamlit_lottie import st_lottie
import requests

# ======================== Configure Gemini API ========================
API_KEY = "AIzaSyDTRWw-qd1bk6Hj2JZxSVISyLXTq6LCalQ"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Marketing Analytics Predictor", layout="wide", page_icon="📊")

# ======================== Load Lottie Animations (safe) ========================
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

ai_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
revenue_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_k86wxpgr.json")

# ======================== Custom CSS ========================
st.markdown("""
<style>
    :root {
        --accent1: #0078D7;
        --accent2: #00A3FF;
        --glass-bg: rgba(0,30,60,0.36);
    }
    html, body {
        background: linear-gradient(180deg, #041028 0%, #071937 100%);
        color: #e6f0fa;
        font-family: 'Poppins', sans-serif;
    }

    /* General Glass Card */
    .glass-card {
        padding: 1.25rem;
        border-radius: 16px;
        background: var(--glass-bg);
        border: 1.25px solid rgba(0,163,255,0.14);
        box-shadow: 0 8px 30px rgba(0,10,30,0.6);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin: 0.9rem 0;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover { transform: translateY(-4px); box-shadow: 0 18px 45px rgba(0,163,255,0.12); }

    /* Predict & Download Button Glow (applies to both regular and download buttons) */
    .stButton > button, .stDownloadButton > button {
        border-radius: 12px !important;
        border: none !important;
        background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        padding: 0.85rem 1.8rem !important;
        cursor: pointer !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease !important;
        box-shadow: 0 0 18px rgba(0,163,255,0.6) !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 0 34px rgba(0,163,255,1) !important;
    }

    /* KPI Revenue Card */
    .kpi-card {
        text-align: center;
        padding: 1.6rem;
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(2,30,60,0.6), rgba(2,30,60,0.45));
        border: 1px solid rgba(0,163,255,0.18);
        box-shadow: 0 6px 26px rgba(0,163,255,0.12);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,163,255,0.18); }
    .kpi-card h2 { font-size: 1.2rem; color: #cfeeff; margin: 0; }
    .kpi-card h1 { font-size: 2.6rem; margin: 0.4rem 0; color: #e9fbff; text-shadow: 0 0 18px rgba(0,163,255,0.9); }

    /* Mini KPI */
    .mini-kpi {
        text-align: center;
        padding: 0.9rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(0,163,255,0.08);
        box-shadow: 0 6px 24px rgba(0,10,30,0.5);
    }
    .mini-kpi h4 { margin: 0; font-size: 0.95rem; color: #cfeeff; }
    .mini-kpi p { margin: 0.35rem 0 0; font-size: 1.15rem; font-weight:700; color: #eaf7ff; }

    /* AI Suggestions Card */
    .ai-card {
        padding: 1rem;
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(0,70,120,0.2), rgba(0,70,120,0.08));
        border: 1px solid rgba(0,163,255,0.12);
        box-shadow: 0 10px 30px rgba(0,163,255,0.06);
    }
    .ai-card:hover { box-shadow: 0 14px 40px rgba(0,163,255,0.12); transform: translateY(-3px); }

    /* small spacing fix */
    .stHeader { margin-bottom: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ======================== Page Header ========================
st.markdown("<h1 style='text-align:center; color:#e9fbff; margin-bottom:0.2rem;'>🚀 Marketing Analytics Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#a9cfe8; margin-top:0;'>✨ Enter your campaign details to forecast revenue and receive AI-powered optimization strategies ✨</p>", unsafe_allow_html=True)
st.markdown("---")

# ======================== Lottie Header (safe) ========================
if ai_animation:
    try:
        st_lottie(ai_animation, height=180, key="ai_header")
    except Exception:
        pass

# ======================== Input Fields ========================
with st.container():
    # st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.header("🎯 Campaign Input Parameters")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        status = st.selectbox("Campaign Status 🚦", ["Active", "Completed"])
        channel = st.selectbox("Marketing Channel 📺", ["Facebook", "Google", "Instagram", "LinkedIn", "YouTube"])
        objective = st.selectbox("Campaign Objective 🎯", ["Awareness", "Leads", "Sales", "Traffic"])
        audience = st.selectbox("Target Audience 👥", ["Adults", "Professionals", "Seniors", "Youth"])
        geo = st.selectbox("Geographical Target 🌍", ["India", "SEA", "UK", "US"])
        creative_type = st.selectbox("Creative Type 🎨", ["Carousel", "Image", "Video"])
    with col2:
        budget = st.number_input("💰 Total Budget ($)", 100, 1_000_000, 5000, step=100, format="%d")
        spend = st.number_input("📉 Spend Till Date ($)", 0, 1_000_000, 1000, step=50, format="%d")
        impressions = st.number_input("👀 Impressions Till Date", 0, 5_000_000, 5000, step=100, format="%d")
        clicks = st.number_input("🖱️ Clicks Till Date", 0, 100_000, 100, step=10, format="%d")
        conversions = st.number_input("✅ Conversions Till Date", 0, 10_000, 10, step=1, format="%d")
        duration = st.number_input("⏳ Total Campaign Duration (days)", 1, 365, 30, format="%d")
        duration_till_date = st.number_input("📅 Duration Till Date (days)", 0, 365, 10, format="%d")
    st.markdown("</div>", unsafe_allow_html=True)

# ======================== Prediction ========================
if st.button("✨ Predict Revenue & Generate Insights"):
    user_input = {
        "Status": status, "Channel": channel, "Objective": objective,
        "Audience": audience, "Geo": geo, "Creative_Type": creative_type,
        "Budget": float(budget), "Spend_Till_Date": float(spend), "Impressions_Till_Date": int(impressions),
        "Clicks_Till_Date": int(clicks), "Conversions_Till_Date": int(conversions),
        "Campaign_Duration": int(duration), "Duration_Till_Date": int(duration_till_date),
    }

    st.header("📈 Prediction Results & AI Analysis")
    progress_bar = st.progress(0, text="Analyzing campaign data...")

    # Predict (ensure numeric)
    predicted_revenue = predict_campaign_revenue(user_input)
    try:
        predicted_revenue = float(predicted_revenue)
    except Exception:
        predicted_revenue = 0.0

    # brief progress animation
    for p in range(0, 81, 8):
        time.sleep(0.03)
        progress_bar.progress(p, text="Forecasting revenue...")

    # ======================== Revenue KPI Card inside Box ========================
    # st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    # st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
    st.subheader("💵 Predicted Total Revenue")
    revenue_placeholder = st.empty()
    # smoother, bounded 50-step animation (works for very large numbers without heavy CPU)
    for step in range(0, 51):
        display_val = predicted_revenue * (step / 50)
        revenue_placeholder.markdown(f"<h1>${display_val:,.2f}</h1>", unsafe_allow_html=True)
        time.sleep(0.015)
    # ensure final exact value
    revenue_placeholder.markdown(f"<h1>${predicted_revenue:,.2f}</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Mini KPI Row (Budget, Spend, CTR)
    colA, colB, colC = st.columns([1,1,1], gap="small")
    with colA:
        st.markdown(f"""
            <div class="mini-kpi">
                <h4>💰 Total Budget</h4>
                <p>${float(budget):,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    with colB:
        st.markdown(f"""
            <div class="mini-kpi">
                <h4>📉 Spend Till Date</h4>
                <p>${float(spend):,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    with colC:
        ctr = (clicks / impressions * 100) if impressions > 0 else 0.0
        st.markdown(f"""
            <div class="mini-kpi">
                <h4>🖱️ CTR</h4>
                <p>{ctr:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close glass-card

    # small progress bump
    for p in range(81, 96, 3):
        time.sleep(0.02)
        progress_bar.progress(p, text="Preparing AI insights...")

    # ======================== AI Suggestions ========================
    st.subheader("💡 AI Optimization Report")
    if revenue_animation:
        try:
            st_lottie(revenue_animation, height=140, key="loading_ai")
        except Exception:
            pass

    with st.spinner("🤖 Generating insights..."):
        model_gemini = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Campaign Data: {pd.Series(user_input).to_string()}
        Predicted Final Revenue: ${predicted_revenue:,.2f}
        Provide:
        - Executive Summary
        - 3 Actionable Suggestions
        - Issues & Improvements Table
        """
        response = model_gemini.generate_content(prompt)
        progress_bar.progress(100, text="Done!")

        st.markdown(f"<div class='ai-card'>{response.text}</div>", unsafe_allow_html=True)

    # ======================== Campaign Summary ========================
    st.subheader("📋 Campaign Summary")
    summary_df = pd.DataFrame([user_input])
    summary_df["Predicted_Revenue"] = predicted_revenue
    # st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.dataframe(summary_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ======================== Download ========================
    excel_data = to_excel(summary_df)
    st.download_button("📥 Download Results", excel_data, "campaign_prediction.xlsx")




