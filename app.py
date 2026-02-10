import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os
import base64
from typing import Optional

# =============================================================================
# 1. PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="IT Job Trending",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 2. FONT + THEME CSS (SAFE SCOPE)
# =============================================================================
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
:root {
    --gg-font: 'Be Vietnam Pro', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;

    /* Palette: dark blue + light blue + white */
    --gg-navy: #0b1f3b;
    --gg-navy-2: #0a1730;
    --gg-blue: #2563eb;
    --gg-blue-2: #60a5fa;
    --gg-sky: #eff6ff;
    --gg-white: #ffffff;

    --gg-text: #0b1f3b;
    --gg-text-muted: #52627a;
    --gg-border: rgba(11, 31, 59, 0.12);
    --gg-bg: #f7fbff;
    --gg-card: rgba(255,255,255,0.88);

    --gg-shadow: 0 10px 28px rgba(11, 31, 59, 0.10);
    --gg-shadow-strong: 0 18px 50px rgba(11, 31, 59, 0.14);
    --gg-radius: 16px;
}

/* =============================================================================
   Layout safety rules:
   - Never globally style `*` or `[class*="css"]` (Streamlit uses generated classnames).
   - Scope visual styling to main content; keep sidebar rules minimal and safe.
   - Avoid fixed overlays that could cover sidebar/tooltips.
============================================================================= */

/* ===== App background (safe target) ===== */
div[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(900px 420px at 45% -120px, rgba(96,165,250,0.45), rgba(255,255,255,0) 60%),
        radial-gradient(820px 520px at 88% 12%, rgba(37,99,235,0.18), rgba(255,255,255,0) 60%),
        linear-gradient(180deg, var(--gg-bg) 0%, #ffffff 35%, var(--gg-bg) 100%);
}

/* ===== Typography ===== */
div[data-testid="stAppViewContainer"] .main,
section[data-testid="stSidebar"] {
    font-family: var(--gg-font);
    color: var(--gg-text);
}
/* Form & section labels in main content: always dark and bold for readability */
div[data-testid="stAppViewContainer"] .main label {
    color: var(--gg-text);
    font-weight: 700;
}
div[data-testid="stAppViewContainer"] .main .stMarkdown p,
div[data-testid="stAppViewContainer"] .main .stMarkdown span {
    color: var(--gg-text);
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
    border-right: 1px solid var(--gg-border);
}

/* Keep sidebar text readable without forcing every element via !important */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: var(--gg-text);
}

/* Sidebar radio */
section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid transparent;
    transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(96, 165, 250, 0.16);
    color: var(--gg-blue) !important;
    border-color: rgba(37, 99, 235, 0.22);
    transform: translateY(-1px);
}

/* Sidebar brand card */
.gg-sidebar-brand {
    border-radius: 16px;
    padding: 16px 14px;
    margin: 10px 0 6px 0;
    background:
        radial-gradient(420px 160px at 50% -20px, rgba(96,165,250,0.50), rgba(255,255,255,0) 60%),
        linear-gradient(135deg, rgba(11,31,59,0.04) 0%, rgba(37,99,235,0.05) 100%);
    border: 1px solid var(--gg-border);
    box-shadow: 0 10px 24px rgba(11,31,59,0.08);
}
.gg-sidebar-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}
.gg-sidebar-logo img {
    width: 54px;
    height: 54px;
    object-fit: contain;
    border-radius: 16px;
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(11,31,59,0.10);
    box-shadow: 0 14px 30px rgba(11,31,59,0.10);
}
.gg-sidebar-title {
    text-align: center;
    font-weight: 900;
    letter-spacing: 0.12em;
    color: var(--gg-navy);
    margin: 0;
    font-size: 0.95rem;
}
.gg-sidebar-subtitle {
    text-align: center;
    color: var(--gg-text-muted);
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 6px 0 0 0;
    font-size: 0.70rem;
}

/* ===== Cards ===== */
.gg-card {
    background: var(--gg-card);
    border: 1px solid var(--gg-border);
    border-radius: var(--gg-radius);
    padding: 24px;
    box-shadow: var(--gg-shadow);
    margin-bottom: 24px;
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
    backdrop-filter: blur(10px);
}
.gg-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--gg-shadow-strong);
    border-color: rgba(37, 99, 235, 0.22);
}

/* ===== Hero ===== */
.gg-hero {
    position: relative;
    text-align: center;
    background:
        radial-gradient(700px 260px at 50% -35px, rgba(96,165,250,0.55), rgba(255,255,255,0) 60%),
        linear-gradient(135deg, rgba(11,31,59,0.06) 0%, rgba(37,99,235,0.07) 100%),
        rgba(255,255,255,0.82);
    border: 1px solid rgba(11,31,59,0.10);
    border-radius: calc(var(--gg-radius) + 6px);
    padding: 34px 26px;
    box-shadow: var(--gg-shadow);
    margin-bottom: 32px;
    overflow: hidden;
    animation: gg-fade-in 520ms ease both;
}
.gg-hero::after {
    content: "";
    position: absolute;
    inset: -80px -120px auto auto;
    width: 260px;
    height: 260px;
    background: radial-gradient(circle at 30% 30%, rgba(37,99,235,0.28), rgba(255,255,255,0) 60%);
    transform: rotate(14deg);
    pointer-events: none;
}
.gg-hero-inner {
    max-width: 980px;
    margin: 0 auto;
    position: relative;
}

.gg-hero-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
}
.gg-hero-logo img {
    width: 92px;
    height: 92px;
    object-fit: contain;
    border-radius: 22px;
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(11,31,59,0.10);
    box-shadow: 0 18px 48px rgba(11,31,59,0.15);
    animation: gg-float 3.8s ease-in-out infinite;
}

.gg-hero h1 {
    color: var(--gg-text);
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.02em;
}

.gg-hero p {
    color: var(--gg-text-muted);
    font-size: 1.05rem;
    font-weight: 500;
}

.gg-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.66);
    border: 1px solid rgba(11,31,59,0.10);
    color: var(--gg-text);
    font-weight: 700;
    box-shadow: 0 10px 24px rgba(11,31,59,0.08);
    backdrop-filter: blur(10px);
}

/* ===== Key metrics custom cards ===== */
.gg-kpi-row {
    margin-bottom: 12px;
}
.gg-kpi-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, #ffffff 0%, #eff6ff 55%, #dbeafe 100%);
    border: 1px solid rgba(37, 99, 235, 0.30);
    box-shadow: 0 16px 38px rgba(15, 23, 42, 0.20);
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}
.gg-kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--gg-shadow-strong);
    border-color: rgba(37, 99, 235, 0.45);
}
.gg-kpi-icon {
    width: 44px;
    height: 44px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at 30% 20%, #60a5fa, #1d4ed8);
    color: #ffffff;
    font-size: 1.4rem;
    flex-shrink: 0;
    box-shadow: 0 12px 26px rgba(37, 99, 235, 0.55);
}
.gg-kpi-content {
    display: flex;
    flex-direction: column;
}
.gg-kpi-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-weight: 700;
    color: #0b1f3b;
    margin-bottom: 4px;
}
.gg-kpi-value {
    font-size: 1.5rem;
    font-weight: 900;
    color: #1d4ed8;
    line-height: 1.1;
}

/* ===== Charts ===== */
div[data-testid="stAppViewContainer"] .main div[data-testid="stPlotlyChart"] {
    background: var(--gg-card);
    border: 1px solid var(--gg-border);
    border-radius: 14px;
    padding: 16px;
    box-shadow: var(--gg-shadow);
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
    overflow: hidden;
}
div[data-testid="stAppViewContainer"] .main div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--gg-shadow-strong);
    border-color: rgba(37, 99, 235, 0.20);
}
/* Data / table headers: keep high contrast */
div[data-testid="stAppViewContainer"] .main .stDataFrame table thead tr th,
div[data-testid="stAppViewContainer"] .main .stTable table thead tr th {
    color: var(--gg-text);
    font-weight: 700;
}

.gg-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--gg-navy);
    font-weight: 900;
    letter-spacing: -0.01em;
    margin: 6px 0 10px 0;
    font-size: 1.08rem;
}

/* ===== Buttons ===== */
div[data-testid="stAppViewContainer"] .main .stButton > button {
    background: linear-gradient(135deg, var(--gg-blue) 0%, #1e40af 100%);
    color: #ffffff;
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 0.75rem 1.5rem;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    letter-spacing: 0.02em;
}
div[data-testid="stAppViewContainer"] .main .stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.35);
    transform: translateY(-2px);
    border-color: rgba(255,255,255,0.25);
}
div[data-testid="stAppViewContainer"] .main .stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

/* ===== Footer ===== */
.gg-footer {
    margin-top: 36px;
    padding: 14px 0;
    text-align: center;
    font-size: 0.85rem;
    color: var(--gg-text-muted);
    border-top: 1px solid var(--gg-border);
}
.gg-footer a {
    color: var(--gg-blue);
    text-decoration: none;
}

/* ===== Motion (subtle) ===== */
@keyframes gg-fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes gg-float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
    100% { transform: translateY(0px); }
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# 3. HELPERS
# =============================================================================
@st.cache_data
def load_data():
    path = "data/vietnam_it_jobs_cleaned.csv"
    return pd.read_csv(path) if os.path.exists(path) else None


@st.cache_resource
def load_model():
    path = "models/salary_model.pkl"
    return joblib.load(path) if os.path.exists(path) else None


@st.cache_data
def logo_uri(path="images/logo.png") -> Optional[str]:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


GG_PLOTLY_FONT = "Be Vietnam Pro, sans-serif"


def gg_plotly_layout(fig, title_x: Optional[str] = None, title_y: Optional[str] = None):
    """UI-only Plotly layout defaults for a cohesive look (does not change data)."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=18, r=18, t=12, b=18),
        font=dict(family=GG_PLOTLY_FONT, color="#0b1f3b"),
        hovermode="x unified",
    )
    fig.update_xaxes(
        title=title_x, 
        showgrid=True, 
        gridcolor="rgba(11,31,59,0.1)",
        title_font=dict(size=14, color="#0b1f3b"),
        tickfont=dict(color="#0b1f3b")
    )
    fig.update_yaxes(
        title=title_y, 
        showgrid=True, 
        gridcolor="rgba(11,31,59,0.1)",
        title_font=dict(size=14, color="#0b1f3b"),
        tickfont=dict(color="#0b1f3b")
    )
    return fig


df = load_data()
model = load_model()

# =============================================================================
# 4. SIDEBAR
# =============================================================================
with st.sidebar:
    logo = logo_uri()
    st.markdown(
        f"""
        <div class="gg-sidebar-brand">
            <div class="gg-sidebar-logo">
                {f"<img src='{logo}' alt='GearGen logo' />" if logo else ""}
            </div>
            <div class="gg-sidebar-title">GEARGEN</div>
            <div class="gg-sidebar-subtitle">Vietnam IT Job Trending</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio("Menu", ["📊 Phân tích thị trường", "🔮 Dự đoán mức lương"], label_visibility="collapsed")

    st.divider()

    # --- Advanced Filters ---
    st.markdown("### 🎯 Bộ lọc nâng cao")
    
    # 1. Location Filter
    selected_loc = st.selectbox(
        "Địa điểm",
        ["Tất cả địa điểm"] + sorted(df["Location"].unique())
    )

    # 2. Salary Range Filter
    min_sal = int(df["Avg_Salary_Million"].min())
    max_sal = int(df["Avg_Salary_Million"].max())
    salary_range = st.slider(
        "Mức lương (Triệu VNĐ)",
        min_value=min_sal,
        max_value=max_sal,
        value=(min_sal, max_sal)
    )

    # 3. Skills Filter
    all_skills = sorted(list(set(df["Skills"].str.split(",").explode().str.strip().unique())))
    selected_skills = st.multiselect("Kỹ năng", all_skills)

# =============================================================================
# 5. MAIN
# =============================================================================
df_view = df
if page == "📊 Phân tích thị trường" and df is not None:
    # Filter by Location
    if selected_loc != "Tất cả địa điểm":
        df_view = df_view[df_view["Location"] == selected_loc]
    
    # Filter by Salary
    df_view = df_view[
        (df_view["Avg_Salary_Million"] >= salary_range[0]) & 
        (df_view["Avg_Salary_Million"] <= salary_range[1])
    ]

    # Filter by Skills
    if selected_skills:
        # Filter rows that contain ANY of the selected skills
        # Case-insensitive matching
        pattern = "|".join([os.path.normcase(s) for s in selected_skills]) 
        # Actually dataset skills are already lower/cleaned but let's be safe
        df_view = df_view[df_view["Skills"].apply(lambda x: any(s in x for s in selected_skills))]


logo = logo_uri()

if page == "📊 Phân tích thị trường":
    st.markdown(
        f"""
        <div class="gg-hero">
            <div class="gg-hero-inner">
                <div class="gg-hero-logo">
                    {f"<img src='{logo}' alt='GearGen logo'>" if logo else ""}
                </div>
                <h1>GearGen · Vietnam IT Job Trending</h1>
                <p>Phân tích thị trường · Xu hướng tuyển dụng, mức lương và kỹ năng nổi bật (2024)</p>
                <div class="gg-chip">📊 Phân tích thị trường IT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_view is not None:
        total_jobs = len(df_view)
        avg_salary = df_view["Avg_Salary_Million"].mean()
        top_location = df_view["Location"].mode()[0]
        skills_series = df_view["Skills"].str.split(",").explode().str.strip()
        top_skill = skills_series.mode()[0].title() if not skills_series.empty else "N/A"

        st.markdown("<div class='gg-kpi-row'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                f"""
                <div class="gg-kpi-card">
                    <div class="gg-kpi-icon">📂</div>
                    <div class="gg-kpi-content">
                        <div class="gg-kpi-label">Tổng tin tuyển dụng</div>
                        <div class="gg-kpi-value">{total_jobs:,}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="gg-kpi-card">
                    <div class="gg-kpi-icon">💰</div>
                    <div class="gg-kpi-content">
                        <div class="gg-kpi-label">Lương trung bình</div>
                        <div class="gg-kpi-value">{avg_salary:.1f}M</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""
                <div class="gg-kpi-card">
                    <div class="gg-kpi-icon">📍</div>
                    <div class="gg-kpi-content">
                        <div class="gg-kpi-label">Khu vực lớn nhất</div>
                        <div class="gg-kpi-value">{top_location}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f"""
                <div class="gg-kpi-card">
                    <div class="gg-kpi-icon">🔥</div>
                    <div class="gg-kpi-content">
                        <div class="gg-kpi-label">Kỹ năng Hot</div>
                        <div class="gg-kpi-value">{top_skill}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")

        # --- ROW 1: Top Skills & Salary by Location ---
        col_skill, col_loc = st.columns([1.5, 1])

        with col_skill:
            st.markdown('<div class="gg-section-title">🚀 Top Kỹ năng được yêu cầu</div>', unsafe_allow_html=True)
            if not skills_series.empty:
                # Calculate top skills
                top_skills = skills_series.value_counts().head(10).reset_index()
                top_skills.columns = ["Skill", "Count"]

                fig = px.bar(
                    top_skills, 
                    x="Count", 
                    y="Skill", 
                    orientation='h',
                    text="Count",
                    color="Count",
                    color_continuous_scale="blues"
                )
                fig.update_traces(textposition="outside")
                # Invert y-axis to show top skill at top
                fig.update_layout(yaxis=dict(autorange="reversed"))
                gg_plotly_layout(fig, title_x="Số lượng tin tuyển dụng", title_y=None)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Chưa có dữ liệu kỹ năng.")

        with col_loc:
            st.markdown('<div class="gg-section-title">📍 Mức lương theo Địa điểm</div>', unsafe_allow_html=True)
            # Calculate salary by location
            salary_by_loc = df_view.groupby("Location")["Avg_Salary_Million"].mean().sort_values(ascending=False).reset_index()
            
            fig = px.bar(
                salary_by_loc,
                x="Location",
                y="Avg_Salary_Million",
                text_auto=".1f",
                color="Avg_Salary_Million",
                color_continuous_scale="blues"
            )
            gg_plotly_layout(fig, title_x=None, title_y="Triệu VNĐ")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("")

        # --- ROW 2: Salary Distribution & Boxplot ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="gg-section-title">💰 Phân phối mức lương</div>', unsafe_allow_html=True)
            fig = px.histogram(
                df_view, 
                x="Avg_Salary_Million", 
                nbins=20,
                color_discrete_sequence=["#3b82f6"]
            )
            fig.update_traces(marker_line_color="white", marker_line_width=1, opacity=0.9)
            gg_plotly_layout(fig, title_x="Mức lương (Triệu VNĐ)", title_y="Số lượng tin")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            st.markdown('<div class="gg-section-title">🏆 Lương theo kinh nghiệm</div>', unsafe_allow_html=True)
            fig = px.box(
                df_view, 
                x="Experience", 
                y="Avg_Salary_Million",
                color="Experience",
                color_discrete_sequence=px.colors.qualitative.Safe,
                category_orders={"Experience": ["Fresher", "Junior", "Senior", "Lead", "Manager"]}
            )
            gg_plotly_layout(fig, title_x=None, title_y="Mức lương (Triệu VNĐ)")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # --- ROW 3: Raw Data View ---
        st.markdown("")
        with st.expander("🔍 Xem dữ liệu chi tiết", expanded=False):
            st.dataframe(
                df_view[["Job Title", "Company", "Location", "Salary", "Skills", "Experience", "Posted Date"]],
                use_container_width=True,
                hide_index=True
            )

elif page == "🔮 Dự đoán mức lương":
    st.markdown(
        """
        <div class="gg-hero">
            <div class="gg-hero-inner">
                <h1>GearGen · Vietnam IT Job Trending</h1>
                <p>Ước tính mức lương dựa trên dữ liệu thị trường · Nhanh, rõ ràng, dễ dùng</p>
                <div class="gg-chip">🔮 Dự đoán mức lương IT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if model and df is not None:
        l, c, r = st.columns([1, 1.25, 1])
        with c:
           
            st.markdown("<div class='gg-section-title'>📝 Nhập thông tin</div>", unsafe_allow_html=True)

            exp = st.selectbox("Kinh nghiệm", ["Fresher", "Junior", "Senior", "Lead", "Manager"])
            loc = st.selectbox("Địa điểm", sorted(df["Location"].unique()))
            title = st.selectbox("Vị trí", sorted(df["Job Title"].unique()))

            if st.button("🚀 Dự đoán mức lương"):
                pred = model.predict(pd.DataFrame([{
                    "Experience": exp,
                    "Location": loc,
                    "Job Title": title
                }]))[0]

                st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
                st.success(f"Mức lương ước tính: {pred:.1f} triệu VNĐ")

            st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# 6. FOOTER
# =============================================================================
st.markdown(
    """
    <div class="gg-footer">
        © 2025 <strong>Trung tâm Công nghệ GearGen</strong> ·
        <a href="#">Privacy Policy</a> ·
        <a href="#">Support</a>
    </div>
    """,
    unsafe_allow_html=True,
)