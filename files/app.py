import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import json
import io
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 { font-size: 2.5rem; font-weight: 700; margin: 0; }
    .main-header p  { font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem; }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-card h3 { color: #667eea; font-size: 0.85rem; text-transform: uppercase;
                      letter-spacing: 1px; margin: 0 0 0.3rem; }
    .metric-card .value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0; }

    .insight-box {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border: 1px solid #e0e5ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .insight-box h4 { color: #5a67d8; margin-top: 0; }

    .chat-message {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .user-message   { background: #667eea; color: white; margin-left: 20%; }
    .ai-message     { background: #f8f9ff; border: 1px solid #e0e5ff; margin-right: 20%; }

    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }

    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a2e;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Data Analyst</h1>
    <p>Upload your data → Get instant AI-powered insights, visualizations & answers</p>
</div>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
if "df"           not in st.session_state: st.session_state.df           = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "insights"     not in st.session_state: st.session_state.insights     = None
if "file_name"    not in st.session_state: st.session_state.file_name    = ""

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.secrets.get("GOOGLE_API_KEY", "")
    st.markdown("---")
    st.markdown("### 📁 Upload Data")
    uploaded = st.file_uploader("CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded)
            else:
                st.session_state.df = pd.read_excel(uploaded)
            st.session_state.file_name = uploaded.name
            st.success(f"✅ Loaded {uploaded.name}")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        st.markdown(f"**Rows:** {df.shape[0]:,}")
        st.markdown(f"**Columns:** {df.shape[1]}")
        st.markdown(f"**Missing:** {df.isnull().sum().sum():,}")

    st.markdown("---")
    st.markdown("### 🛠️ Tools")
    st.markdown("- 📈 Auto Visualizations\n- 🔍 Statistical Analysis\n- 💬 Chat with Data\n- 📄 AI Report")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_data_summary(df: pd.DataFrame) -> str:
    summary = {
        "shape": df.shape,
        "columns": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "numeric_stats": df.describe().round(2).to_dict() if not df.select_dtypes(include=np.number).empty else {},
        "sample": df.head(5).to_dict(orient="records"),
        "unique_counts": {c: int(df[c].nunique()) for c in df.columns},
    }
    return json.dumps(summary, default=str)


def ask_claude(prompt: str, df: pd.DataFrame, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model   = genai.GenerativeModel("gemini-pro",
                system_instruction="""You are an expert data analyst and statistician.
You have access to a dataset and your job is to provide clear, actionable insights.
Always structure your answers with:
- Key findings (use bullet points)
- Statistical observations
- Business recommendations
- Any anomalies or patterns worth noting
Be concise but thorough. Use emojis to make responses engaging.""")
    summary = get_data_summary(df)
    response = model.generate_content(f"Dataset summary:\n{summary}\n\nQuestion / Task:\n{prompt}")
    return response.text


def generate_auto_insights(df: pd.DataFrame, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model   = genai.GenerativeModel("gemini-pro",
                system_instruction="""You are an expert data analyst. Analyze this dataset and produce a comprehensive report covering:
1. 📊 Dataset Overview
2. 🔍 Key Statistical Insights  
3. 📈 Trends & Patterns
4. ⚠️ Data Quality Issues
5. 💡 Top 5 Business Recommendations
6. 🎯 Next Steps for Analysis
Use markdown formatting with clear sections and bullet points.""")
    summary  = get_data_summary(df)
    response = model.generate_content(f"Please analyze this dataset and provide comprehensive insights:\n{summary}")
    return response.text


# ─── Main Content (tabs) ──────────────────────────────────────────────────────

if st.session_state.df is None:
    # Landing state
    col1, col2, col3 = st.columns(3)
    for col, icon, title, desc in [
        (col1, "📁", "Upload",     "CSV or Excel files supported"),
        (col2, "🤖", "AI Analyze", "Instant insights powered by Claude"),
        (col3, "💬", "Chat",       "Ask questions about your data"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center">
                <div style="font-size:2.5rem">{icon}</div>
                <h3 style="font-size:1.1rem;text-transform:none;margin-top:.5rem">{title}</h3>
                <p style="color:#666;font-size:.9rem">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.info("👈 Upload a dataset from the sidebar to get started!")

    # Demo section
    st.markdown('<div class="section-header">🎯 Features</div>', unsafe_allow_html=True)
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        st.markdown("""
        **📊 Auto Visualizations**
        - Distribution plots, correlations, bar/line charts
        - Interactive Plotly graphs
        - Smart chart type selection

        **🔍 Statistical Analysis**
        - Descriptive stats, correlations
        - Missing value analysis
        - Outlier detection
        """)
    with fcol2:
        st.markdown("""
        **💬 Chat with Your Data**
        - Ask natural language questions
        - Get instant AI answers
        - Context-aware follow-ups

        **📄 AI Report Generation**
        - Comprehensive insights
        - Business recommendations
        - Export-ready summaries
        """)

else:
    df = st.session_state.df
    tabs = st.tabs(["📊 Overview", "📈 Visualizations", "🔍 Statistics", "💬 Chat with AI", "📄 AI Report"])

    # ── Tab 1 – Overview ──────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        metrics = [
            ("Total Rows",    f"{df.shape[0]:,}",              m1),
            ("Columns",       f"{df.shape[1]}",                m2),
            ("Missing Values",f"{df.isnull().sum().sum():,}",  m3),
            ("Numeric Cols",  f"{len(df.select_dtypes(include=np.number).columns)}", m4),
        ]
        for label, value, col in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{label}</h3>
                    <p class="value">{value}</p>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">🔎 Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(20), use_container_width=True)

        # Missing values heatmap
        if df.isnull().sum().sum() > 0:
            st.markdown('<div class="section-header">⚠️ Missing Values</div>', unsafe_allow_html=True)
            missing = df.isnull().sum().reset_index()
            missing.columns = ["Column", "Missing Count"]
            missing = missing[missing["Missing Count"] > 0]
            fig = px.bar(missing, x="Column", y="Missing Count",
                         color="Missing Count", color_continuous_scale="Reds",
                         title="Missing Values per Column")
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2 – Visualizations ────────────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="section-header">📈 Auto Visualizations</div>', unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols     = df.select_dtypes(include="object").columns.tolist()

        if numeric_cols:
            # Distribution grid
            st.markdown("#### Distribution of Numeric Columns")
            n  = len(numeric_cols[:6])
            nc = min(3, n)
            nr = (n + nc - 1) // nc
            fig = make_subplots(rows=nr, cols=nc,
                                subplot_titles=numeric_cols[:6])
            for i, col_name in enumerate(numeric_cols[:6]):
                r, c = divmod(i, nc)
                fig.add_trace(
                    go.Histogram(x=df[col_name], name=col_name,
                                 marker_color="#667eea", opacity=0.7,
                                 showlegend=False),
                    row=r+1, col=c+1
                )
            fig.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)

            # Correlation heatmap
            if len(numeric_cols) > 1:
                st.markdown("#### Correlation Heatmap")
                corr = df[numeric_cols].corr()
                fig  = px.imshow(corr, color_continuous_scale="RdBu_r",
                                 zmin=-1, zmax=1, aspect="auto",
                                 title="Feature Correlation Matrix")
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)

        if cat_cols:
            st.markdown("#### Categorical Column Distributions")
            for col_name in cat_cols[:3]:
                vc = df[col_name].value_counts().head(15)
                fig = px.bar(x=vc.index, y=vc.values,
                             labels={"x": col_name, "y": "Count"},
                             title=f"Distribution: {col_name}",
                             color=vc.values, color_continuous_scale="Viridis")
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)

        # Custom chart
        st.markdown("#### 🎨 Custom Chart Builder")
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            x_col = st.selectbox("X Axis", df.columns.tolist())
        with cc2:
            y_col = st.selectbox("Y Axis", numeric_cols if numeric_cols else df.columns.tolist())
        with cc3:
            chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Box", "Violin"])

        if st.button("Generate Chart"):
            try:
                fig = {
                    "Bar":    px.bar,
                    "Line":   px.line,
                    "Scatter":px.scatter,
                    "Box":    px.box,
                    "Violin": px.violin,
                }[chart_type](df, x=x_col, y=y_col,
                              title=f"{chart_type}: {x_col} vs {y_col}",
                              color_discrete_sequence=["#667eea"])
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")

    # ── Tab 3 – Statistics ────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-header">🔍 Statistical Analysis</div>', unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if numeric_cols:
            st.markdown("#### Descriptive Statistics")
            st.dataframe(df[numeric_cols].describe().round(3), use_container_width=True)

            st.markdown("#### Outlier Detection (IQR Method)")
            outlier_data = []
            for col_name in numeric_cols:
                Q1, Q3 = df[col_name].quantile(0.25), df[col_name].quantile(0.75)
                IQR     = Q3 - Q1
                n_out   = ((df[col_name] < Q1 - 1.5*IQR) | (df[col_name] > Q3 + 1.5*IQR)).sum()
                outlier_data.append({"Column": col_name, "Outliers": int(n_out),
                                     "% of Data": f"{100*n_out/len(df):.1f}%"})
            st.dataframe(pd.DataFrame(outlier_data), use_container_width=True)

        st.markdown("#### Column Details")
        col_detail = pd.DataFrame({
            "Type":    df.dtypes.astype(str),
            "Non-Null":df.count(),
            "Null":    df.isnull().sum(),
            "Unique":  df.nunique(),
        })
        st.dataframe(col_detail, use_container_width=True)

    # ── Tab 4 – Chat ──────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown('<div class="section-header">💬 Chat with Your Data</div>', unsafe_allow_html=True)

        if not api_key:
            st.warning("⚠️ Enter your Anthropic API key in the sidebar to enable AI chat.")
        else:
            # Chat history
            for msg in st.session_state.chat_history:
                css_class = "user-message" if msg["role"] == "user" else "ai-message"
                icon      = "🧑" if msg["role"] == "user" else "🤖"
                st.markdown(f"""
                <div class="chat-message {css_class}">
                    <strong>{icon}</strong> {msg["content"]}
                </div>""", unsafe_allow_html=True)

            # Suggested questions
            st.markdown("#### 💡 Try asking:")
            suggestions = [
                "What are the key insights from this dataset?",
                "Which columns have the most missing values?",
                "What are the top correlations between features?",
                "Identify any outliers or anomalies",
            ]
            scols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with scols[i % 2]:
                    if st.button(suggestion, key=f"sug_{i}"):
                        st.session_state.chat_history.append({"role": "user", "content": suggestion})
                        with st.spinner("AI is analyzing..."):
                            answer = ask_claude(suggestion, df, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                        st.rerun()

            user_q = st.text_input("Ask anything about your data...", key="user_input",
                                   placeholder="e.g., What is the average sales by region?")
            if st.button("Send 🚀") and user_q:
                st.session_state.chat_history.append({"role": "user", "content": user_q})
                with st.spinner("AI is analyzing..."):
                    answer = ask_claude(user_q, df, api_key)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

    # ── Tab 5 – AI Report ─────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-header">📄 AI-Generated Report</div>', unsafe_allow_html=True)

        if not api_key:
            st.warning("⚠️ Enter your Anthropic API key in the sidebar to generate an AI report.")
        else:
            if st.button("🔍 Generate Full AI Report", use_container_width=True):
                with st.spinner("AI is analyzing your entire dataset..."):
                    st.session_state.insights = generate_auto_insights(df, api_key)

            if st.session_state.insights:
                st.markdown(f"""
                <div class="insight-box">
                    <h4>📊 AI Analysis Report — {st.session_state.file_name}</h4>
                    <p style="color:#666;font-size:.85rem">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>""", unsafe_allow_html=True)
                st.markdown(st.session_state.insights)

                # Download
                st.download_button(
                    "📥 Download Report (Markdown)",
                    data=st.session_state.insights,
                    file_name=f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
