import streamlit as st
import time
import textwrap
import pandas as pd
import data_engine
import analyze
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Captain Analyst",
    page_icon="🧢",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #172554 0%,
                #0f172a 35%,
                #020617 100%
            );
    }

    /* Remove unnecessary top spacing */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Main title */
    .captain-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .captain-subtitle {
        text-align: center;
        font-size: 19px;
        color: #94a3b8;
        margin-bottom: 35px;
    }

    /* Captain badge */
    .captain-badge {
        width: 100px;
        height: 100px;
        margin: 0 auto 20px auto;
        border-radius: 50%;
        background: linear-gradient(
            145deg,
            #2563eb,
            #1e3a8a
        );
        border: 3px solid #60a5fa;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        box-shadow:
            0 0 35px rgba(37, 99, 235, 0.35);
    }

    /* Greeting */
    .greeting {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(96, 165, 250, 0.25);
        border-radius: 18px;
        padding: 28px;
        margin: 20px 0;
        text-align: center;
    }

    .greeting-title {
        font-size: 25px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    .greeting-text {
        font-size: 17px;
        color: #cbd5e1;
        line-height: 1.7;
    }

    /* Mission card */
    .mission-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 25px;
        margin: 20px 0;
    }

    .mission-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 700;
    }

    .mission-text {
        color: #94a3b8;
        font-size: 15px;
    }

    /* Status */
    .status-box {
        background: rgba(30, 41, 59, 0.75);
        border-radius: 14px;
        padding: 18px;
        margin: 10px 0;
        color: #e2e8f0;
        border-left: 4px solid #3b82f6;
    }

    /* Success */
    .success-box {
        background: rgba(6, 78, 59, 0.35);
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 18px;
        padding: 30px;
        text-align: center;
        margin: 25px 0;
    }

    .success-title {
        color: #6ee7b7;
        font-size: 28px;
        font-weight: 800;
    }

    .success-text {
        color: #cbd5e1;
        font-size: 16px;
    }

    /* Mission stages */
    .stage {
        background: rgba(15, 23, 42, 0.75);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        border: 1px solid rgba(148, 163, 184, 0.12);
    }

    .stage-complete {
        border-left: 4px solid #34d399;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        font-size: 16px;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.75);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }

    </style>
    """
    )


# =========================================================
# SESSION STATE
# =========================================================

if "mission_started" not in st.session_state:
    st.session_state.mission_started = False

if "mission_complete" not in st.session_state:
    st.session_state.mission_complete = False

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None


# =========================================================
# HEADER
# =========================================================

st.html(
    '<div class="captain-badge">🧢</div>'
)

st.html(
    '<div class="captain-title">Captain Analyst</div>'
)

st.html(
    '<div class="captain-subtitle">'
    'Your Data. My Mission.'
    '</div>'
)


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.mission_started:

    st.html(
        """
        <div class="greeting">

            <div class="greeting-title">
                👋 Hi! I'm Captain Analyst.
            </div>

            <div class="greeting-text">
                Your data mission starts here.<br><br>
                Upload your dataset and I'll navigate it
                from raw data to meaningful insights.
            </div>

        </div>
        """
    )




    st.html(
        """
        <div class="mission-card">

            <div class="mission-title">
                🎯 Your Mission
            </div>

            <div class="mission-text">
                Captain Analyst can inspect your data,
                clean it, explore patterns, generate
                visualizations, discover insights,
                recommend dashboards and prepare reports.
            </div>

        </div>
        """
    )

    st.subheader("📂 Upload Your Dataset")

    st.write(
        "Upload your CSV or Excel file to begin the mission."
    )

    uploaded_file = st.file_uploader(
        "Drop your dataset here",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        st.session_state.uploaded_name = (
            uploaded_file.name
        )

        st.session_state["uploaded_file"] = uploaded_file
        st.success(
            f"🎯 Mission target received: "
            f"{uploaded_file.name}"
        )

        if st.button(
            "🚀 Start Mission",
            type="primary",
            width="stretch"
        ):

            st.session_state.mission_started = True

            st.rerun()


# =========================================================
# MISSION IN PROGRESS
# =========================================================

elif (
    st.session_state.mission_started
    and not st.session_state.mission_complete
):

    st.html(
        """
        <div class="greeting">

            <div class="greeting-title">
                🎯 Mission Accepted!
            </div>

            <div class="greeting-text">
                I've received your dataset.<br>
                Let's see what your data is hiding.
            </div>

        </div>
        """
        
    )

    st.html(
        f"""
        <div class="mission-card">

            <div class="mission-title">
                📁 Mission File
            </div>

            <div class="mission-text">
                {st.session_state.uploaded_name}
            </div>

        </div>
        """
        
    )

    st.subheader("🧭 Mission Progress")

    progress_bar = st.progress(0)

    status_placeholder = st.empty()

    stages = [
        (
            10,
            "📂",
            "Dataset loaded",
            "I've received and inspected the dataset."
        ),
        (
            25,
            "🧹",
            "Data quality check",
            "Checking missing values and data quality."
        ),
        (
            40,
            "🔎",
            "Exploring the dataset",
            "Examining numerical and categorical patterns."
        ),
        (
            58,
            "📊",
            "Running EDA",
            "Searching for important relationships."
        ),
        (
            72,
            "📈",
            "Generating visualizations",
            "Creating charts that explain the data."
        ),
        (
            85,
            "🧠",
            "Generating intelligence",
            "Turning patterns into meaningful insights."
        ),
        (
            95,
            "🎨",
            "Designing dashboard",
            "Preparing a dashboard recommendation."
        ),
        (
            100,
            "🎖️",
            "Mission complete",
            "Your analysis is ready."
        )
    ]

    # =========================================================
    # REAL DATA PROCESSING
    # =========================================================

    uploaded_file = st.session_state["uploaded_file"]

    progress_bar.progress(10)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>📂 Dataset loaded</strong>
            <br>
            <span style="color:#94a3b8;">
                Captain Analyst has received your dataset.
            </span>
        </div>
        """
    )

    time.sleep(0.5)


    # ---------------------------------------------------------
    # Load Dataset
    # ---------------------------------------------------------

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)


    # ---------------------------------------------------------
    # Dataset Understanding
    # ---------------------------------------------------------

    progress_bar.progress(25)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>🔎 Understanding dataset</strong>
            <br>
            <span style="color:#94a3b8;">
                I'm inspecting columns, data types and structure.
            </span>
        </div>
        """
    )

    profile = data_engine.understand_dataset(df)

    time.sleep(0.5)


    # ---------------------------------------------------------
    # Data Cleaning
    # ---------------------------------------------------------

    progress_bar.progress(40)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>🧹 Cleaning dataset</strong>
            <br>
            <span style="color:#94a3b8;">
                I'm checking missing values and preparing the data.
            </span>
        </div>
        """
    )

    cleaned_df, cleaned_profile = (
        data_engine.clean_dataset(
            df,
            profile
        )
    )

    time.sleep(0.5)


    # ---------------------------------------------------------
    # Save Results
    # ---------------------------------------------------------

    st.session_state["df"] = df

    st.session_state["cleaned_df"] = cleaned_df

    st.session_state["profile"] = profile

    st.session_state["cleaned_profile"] = cleaned_profile

    # ---------------------------------------------------------
    # EDA ANALYSIS
    # ---------------------------------------------------------

    progress_bar.progress(60)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>📊 Running EDA</strong>
            <br>
            <span style="color:#94a3b8;">
                Captain Analyst is exploring patterns and relationships.
            </span>
        </div>
        """
    )

    # Numerical Analysis
    numerical_results = (
        analyze.analyze_numerical_columns(
            cleaned_df
        )
    )

    # Categorical Analysis
    categorical_results = (
        analyze.analyze_categorical_columns(
            cleaned_df
        )
    )

    # Outlier Analysis
    outlier_results = (
        analyze.analyze_outliers(
            cleaned_df
        )
    )

    # Correlation Analysis
    correlation_results = (
        analyze.analyze_correlations(
            cleaned_df
        )
    )

    # Relationship Analysis
    relationship_results = (
        analyze.analyze_relationships(
            cleaned_df
        )
    )

    # Target Analysis
    target_results = (
        analyze.analyze_target(
            cleaned_df
        )
    )


    # Store EDA results
    st.session_state["numerical_results"] = numerical_results
    st.session_state["categorical_results"] = categorical_results
    st.session_state["outlier_results"] = outlier_results
    st.session_state["correlation_results"] = correlation_results
    st.session_state["relationship_results"] = relationship_results
    st.session_state["target_results"] = target_results


    # ---------------------------------------------------------
    # Continue Mission
    # ---------------------------------------------------------

    progress_bar.progress(55)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>🔎 Data preparation complete</strong>
            <br>
            <span style="color:#94a3b8;">
                The cleaned dataset is ready for analysis.
            </span>
        </div>
        """
    )

    time.sleep(0.7)


    progress_bar.progress(100)

    status_placeholder.html(
        """
        <div class="status-box">
            <strong>🎯 Data preparation complete</strong>
            <br>
            <span style="color:#94a3b8;">
                Captain Analyst is ready for the analysis stage.
            </span>
        </div>
        """
    )

    time.sleep(0.7)

    st.session_state.mission_complete = True

    st.rerun()


# =========================================================
# MISSION COMPLETE
# =========================================================

else:

    st.html(
        """
        <div class="success-box">

            <div class="success-title">
                🎖️ MISSION COMPLETE
            </div>

            <br>

            <div class="success-text">
                Captain Analyst has successfully
                completed the data mission.
            </div>

        </div>
        """
    )


    # =====================================================
    # ANALYZED DATASET
    # =====================================================

    st.html(
        f"""
        <div class="mission-card">

            <div class="mission-title">
                📁 Analyzed Dataset
            </div>

            <div class="mission-text">
                {st.session_state.uploaded_name}
            </div>

        </div>
        """
    )


    # =====================================================
    # MISSION RESULTS
    # =====================================================

    st.subheader("🏆 Mission Results")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.html(
            """
            <div class="stage stage-complete">

                🧹 <strong>Data Cleaning</strong>

                <br>

                <span style="color:#94a3b8;">
                    Completed
                </span>

            </div>
            """
        )


    with col2:

        st.html(
            """
            <div class="stage stage-complete">

                🔎 <strong>EDA</strong>

                <br>

                <span style="color:#94a3b8;">
                    Completed
                </span>

            </div>
            """
        )


    with col3:

        st.html(
            """
            <div class="stage stage-complete">

                🤖 <strong>AI Insights</strong>

                <br>

                <span style="color:#94a3b8;">
                    Generated
                </span>

            </div>
            """
        )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.html(
            """
            <div class="stage stage-complete">

                📈 <strong>Visualizations</strong>

                <br>

                <span style="color:#94a3b8;">
                    Generated
                </span>

            </div>
            """
        )


    with col2:

        st.html(
            """
            <div class="stage stage-complete">

                📊 <strong>Dashboard</strong>

                <br>

                <span style="color:#94a3b8;">
                    Ready
                </span>

            </div>
            """
        )


    with col3:

        st.html(
            """
            <div class="stage stage-complete">

                📝 <strong>Report</strong>

                <br>

                <span style="color:#94a3b8;">
                    Ready
                </span>

            </div>
            """
        )


    # =====================================================
    # EXPLORATION MENU
    # =====================================================

    st.divider()


    st.html(
        """
        <div class="greeting">

            <div class="greeting-title">
                🧭 What would you like to explore?
            </div>

            <div class="greeting-text">
                Your mission results are ready.
            </div>

        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    # =====================================================
    # EXPLORE EDA
    # =====================================================

    with col1:

        if st.button(
            "🔎 Explore EDA",
            width="stretch"
        ):

            st.subheader(
                "🔎 Exploratory Data Analysis"
            )

            st.write(
                "Captain Analyst's automated EDA results."
            )


            if "numerical_results" in st.session_state:

                with st.expander(
                    "🔢 Numerical Analysis",
                    expanded=True
                ):

                    st.write(
                        st.session_state[
                            "numerical_results"
                        ]
                    )


            if "categorical_results" in st.session_state:

                with st.expander(
                    "🔤 Categorical Analysis"
                ):

                    st.write(
                        st.session_state[
                            "categorical_results"
                        ]
                    )


            if "outlier_results" in st.session_state:

                with st.expander(
                    "📦 Outlier Analysis"
                ):

                    st.write(
                        st.session_state[
                            "outlier_results"
                        ]
                    )


            if "correlation_results" in st.session_state:

                with st.expander(
                    "🔗 Correlation Analysis"
                ):

                    st.write(
                        st.session_state[
                            "correlation_results"
                        ]
                    )


            if "relationship_results" in st.session_state:

                with st.expander(
                    "📈 Relationship Analysis"
                ):

                    st.write(
                        st.session_state[
                            "relationship_results"
                        ]
                    )


            if "target_results" in st.session_state:

                with st.expander(
                    "🎯 Target Analysis"
                ):

                    st.write(
                        st.session_state[
                            "target_results"
                        ]
                    )


    # =====================================================
    # AI INSIGHTS
    # =====================================================

    with col2:

        if st.button(
            "🧠 View Insights",
            width="stretch"
        ):

            st.html(
                """
                <div class="section-title">
                    🧠 Captain Analyst Insights
                </div>

                <div class="section-text">
                    Captain Analyst has analyzed your dataset
                    and identified important patterns and findings.
                </div>
                """
            )

            cleaned_df = st.session_state.get(
                "cleaned_df"
            )

            if cleaned_df is not None:

                # =================================================
                # GENERATE INSIGHTS
                # =================================================

                with st.spinner(
                    "Captain Analyst is generating insights..."
                ):

                    insights = analyze.generate_insights(
                        cleaned_df
                    )


                # =================================================
                # KEY INSIGHTS
                # =================================================

                st.html(
                    """
                    <div class="section-title">
                        💡 Key Insights
                    </div>
                    """
                )

                if insights:

                    for insight in insights:

                        st.info(
                            f"💡 {insight}"
                        )

                else:

                    st.warning(
                        "No significant insights were generated."
                    )


                # =================================================
                # VISUAL INTELLIGENCE
                # =================================================

                st.divider()

                st.html(
                    """
                    <div class="section-title">
                        📊 Visual Intelligence
                    </div>

                    <div class="section-text">
                        Explore the visual patterns discovered
                        during the analysis.
                    </div>
                    """
                )


                # =================================================
                # DYNAMIC VISUALS FROM THE CURRENT UPLOADED DATASET
                # =================================================

                st.caption(
                    "These visuals are created from the dataset uploaded for this mission, "
                    "not from previously saved chart images."
                )

                numeric_cols = cleaned_df.select_dtypes(include=["number"]).columns.tolist()
                categorical_cols = cleaned_df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()

                # Categorical distributions
                shown_visuals = 0
                for column in categorical_cols:
                    if cleaned_df[column].nunique(dropna=True) < 2 or cleaned_df[column].nunique(dropna=True) > 15:
                        continue
                    counts = cleaned_df[column].fillna("Missing").astype(str).value_counts().head(12)
                    if counts.empty:
                        continue
                    st.markdown(f"**{column}: category distribution**")
                    st.bar_chart(counts.rename("Record count"))
                    shown_visuals += 1
                    if shown_visuals >= 3:
                        break

                # Numeric distributions
                numeric_shown = 0
                for column in numeric_cols:
                    values = pd.to_numeric(cleaned_df[column], errors="coerce").dropna()
                    if values.empty or values.nunique() < 2:
                        continue
                    st.markdown(f"**{column}: value distribution**")
                    histogram = pd.cut(values, bins=min(10, max(3, values.nunique())), duplicates="drop").value_counts().sort_index()
                    histogram.index = histogram.index.astype(str)
                    st.bar_chart(histogram.rename("Record count"))
                    numeric_shown += 1
                    if numeric_shown >= 2:
                        break

                # Numeric metric by category
                metric_candidates = [
                    c for c in numeric_cols
                    if cleaned_df[c].nunique(dropna=True) > 2
                ]
                if categorical_cols and metric_candidates:
                    category = next((c for c in categorical_cols if 2 <= cleaned_df[c].nunique(dropna=True) <= 12), None)
                    metric = metric_candidates[0]
                    if category is not None:
                        grouped = cleaned_df.groupby(category, dropna=False)[metric].mean().sort_values(ascending=False).head(12)
                        if not grouped.empty:
                            st.markdown(f"**Average {metric} by {category}**")
                            st.bar_chart(grouped.rename(f"Average {metric}"))

                if not categorical_cols and not numeric_cols:
                    st.info("No suitable numeric or categorical columns were found for visualizations.")

            else:

                st.error(
                    "Cleaned dataset is not available."
                )


    # =====================================================
    # DYNAMIC DASHBOARD RECOMMENDATIONS
    # =====================================================

    with col3:

        if st.button(
            "📊 View Dashboard",
            width="stretch"
        ):
            st.session_state["show_dashboard"] = True

        # Keep the dashboard visible across Streamlit widget reruns.
        if st.session_state.get("show_dashboard", False):

            st.html(
                """
                <div class="section-title">📊 Captain Analyst Dashboard</div>
                <div class="section-text">
                    Report-ready KPIs, chart recommendations, X/Y axes and filters are
                    generated from the dataset uploaded for this mission.
                </div>
                """
            )

            cleaned_df = st.session_state.get("cleaned_df")

            if cleaned_df is None or cleaned_df.empty:
                st.error("Cleaned dataset is not available. Please start a new mission and upload a dataset.")
            else:
                df_dashboard = cleaned_df.copy()
                numeric_cols = df_dashboard.select_dtypes(include=["number"]).columns.tolist()
                categorical_cols = df_dashboard.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()

                # Identify a likely outcome only from outcome-style names.
                # Sales/revenue/profit are metrics, not automatically target columns.
                target_column = None
                target_keywords = ["churn", "attrition", "outcome", "target", "label", "converted", "conversion", "default", "survived"]
                for column in df_dashboard.columns:
                    name = str(column).strip().lower().replace("_", " ").replace("-", " ")
                    if any(word in name for word in target_keywords) and df_dashboard[column].nunique(dropna=True) <= 10:
                        target_column = column
                        break

                st.html(
                    f"""
                    <div class="mission-card">
                        <div class="mission-title">🎯 Dataset Overview</div>
                        <div class="mission-text">
                            Dataset: {st.session_state.get('uploaded_name') or 'Uploaded dataset'} ·
                            {len(df_dashboard):,} rows · {len(df_dashboard.columns):,} columns
                        </div>
                    </div>
                    """
                )

                # KPI cards are calculated from this dataset only.
                kpis = [{"label": "Total Records", "value": f"{len(df_dashboard):,}"},
                        {"label": "Total Columns", "value": f"{len(df_dashboard.columns):,}"}]
                metric_keywords = ["sales", "revenue", "profit", "amount", "price", "income", "quantity", "orders"]
                metric_column = next(
                    (c for c in numeric_cols if any(k in str(c).lower() for k in metric_keywords)
                     and df_dashboard[c].nunique(dropna=True) > 2),
                    None
                )
                if metric_column is not None:
                    total_value = pd.to_numeric(df_dashboard[metric_column], errors="coerce").sum()
                    kpis.append({"label": f"Total {metric_column}", "value": f"{total_value:,.2f}"})
                    avg_value = pd.to_numeric(df_dashboard[metric_column], errors="coerce").mean()
                    if pd.notna(avg_value):
                        kpis.append({"label": f"Average {metric_column}", "value": f"{avg_value:,.2f}"})
                else:
                    useful_numeric = [c for c in numeric_cols if df_dashboard[c].nunique(dropna=True) > 2]
                    if useful_numeric:
                        metric = useful_numeric[0]
                        average = pd.to_numeric(df_dashboard[metric], errors="coerce").mean()
                        if pd.notna(average):
                            kpis.append({"label": f"Average {metric}", "value": f"{average:,.2f}"})
                if target_column is not None:
                    target_values = df_dashboard[target_column].value_counts(dropna=True)
                    if not target_values.empty:
                        kpis.append({"label": f"Most common {target_column}", "value": str(target_values.index[0])[:24]})
                        kpis.append({"label": f"{target_column} categories", "value": f"{df_dashboard[target_column].nunique(dropna=True):,}"})

                st.markdown("### 🎯 Key Performance Indicators")
                for offset in range(0, min(len(kpis), 6), 3):
                    row = kpis[offset:offset + 3]
                    cols = st.columns(len(row))
                    for idx, kpi in enumerate(row):
                        with cols[idx]:
                            st.markdown(
                                f"""
                                <div style="
                                    border: 1px solid rgba(148,163,184,0.3);
                                    border-radius: 12px;
                                    padding: 16px 10px;
                                    min-height: 110px;
                                    width: 100%;
                                    box-sizing: border-box;
                                    text-align: center;
                                ">
                                    <div style="
                                        color: #cbd5e1;
                                        font-size: 14px;
                                        margin-bottom: 12px;
                                        overflow-wrap: anywhere;
                                    ">
                                        {kpi["label"]}
                                    </div>
                                    <div style="
                                        color: white;
                                        font-size: 27px;
                                        font-weight: 700;
                                        line-height: 1.3;
                                        white-space: normal;
                                        overflow-wrap: anywhere;
                                        word-break: break-word;
                                    ">
                                        {kpi["value"]}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                                    

                st.divider()
                st.markdown("### 🧰 Suggested Dashboard Filters")
                filter_columns = [c for c in categorical_cols if 2 <= df_dashboard[c].nunique(dropna=True) <= 20][:5]
                if filter_columns:
                    filter_cols = st.columns(min(3, len(filter_columns)))
                    for idx, column in enumerate(filter_columns):
                        options = sorted(df_dashboard[column].dropna().astype(str).unique().tolist())
                        with filter_cols[idx % len(filter_cols)]:
                            selected = st.multiselect(f"Filter: {column}", options, key=f"dash_filter_{column}")
                        if selected:
                            df_dashboard = df_dashboard[df_dashboard[column].astype(str).isin(selected)]
                    st.caption(f"Chart previews below use {len(df_dashboard):,} records after filters.")
                else:
                    st.caption("No low-cardinality categorical columns were found for simple slicers.")

                st.divider()
                st.markdown("### 📈 Recommended Charts for Reports")
                st.caption("These are report-design suggestions only. The dashboard recommends what to plot and which fields to place on each axis; the actual exploratory visuals remain in View Insights.")

                recommendations = []

                # Business metric by category, e.g. Region vs Total Sales.
                business_metric = next(
                    (c for c in numeric_cols if any(k in str(c).lower() for k in metric_keywords)
                     and df_dashboard[c].nunique(dropna=True) > 2),
                    None
                )
                useful_categories = [c for c in categorical_cols if 2 <= df_dashboard[c].nunique(dropna=True) <= 15]
                useful_numeric = [c for c in numeric_cols if df_dashboard[c].nunique(dropna=True) > 2]

                if business_metric and useful_categories:
                    category = next((c for c in useful_categories if any(k in str(c).lower() for k in ["region", "category", "product", "segment", "country", "city", "store", "department"])), useful_categories[0])
                    recommendations.append({
                        "title": f"{category} vs Total {business_metric}",
                        "type": "Bar chart",
                        "x": category,
                        "y": f"Sum of {business_metric}",
                        "question": f"Which {category} groups contribute the most {business_metric}?",
                        "kind": "sum_by_category",
                        "category": category,
                        "metric": business_metric
                    })

                if target_column is not None and useful_categories and target_column != useful_categories[0]:
                    category = next((c for c in useful_categories if c != target_column), None)
                    if category:
                        recommendations.append({
                            "title": f"{category} vs {target_column}",
                            "type": "Stacked bar / count comparison",
                            "x": category,
                            "y": f"Record count, split by {target_column}",
                            "question": f"How does {target_column} vary across {category} groups?",
                            "kind": "target_crosstab",
                            "category": category,
                            "metric": target_column
                        })

                if useful_categories:
                    category = useful_categories[0]
                    recommendations.append({
                        "title": f"Distribution of {category}",
                        "type": "Bar chart",
                        "x": category,
                        "y": "Record count",
                        "question": f"Which {category} values are most common?",
                        "kind": "category_count",
                        "category": category,
                        "metric": None
                    })

                if useful_categories and useful_numeric:
                    category = useful_categories[0]
                    metric = next((c for c in useful_numeric if c != business_metric), useful_numeric[0])
                    recommendations.append({
                        "title": f"{category} vs Average {metric}",
                        "type": "Bar chart",
                        "x": category,
                        "y": f"Average {metric}",
                        "question": f"How does the average {metric} differ by {category}?",
                        "kind": "mean_by_category",
                        "category": category,
                        "metric": metric
                    })

                if len(useful_numeric) >= 2:
                    recommendations.append({
                        "title": f"{useful_numeric[0]} vs {useful_numeric[1]}",
                        "type": "Scatter plot",
                        "x": useful_numeric[0],
                        "y": useful_numeric[1],
                        "question": f"Is there a relationship between {useful_numeric[0]} and {useful_numeric[1]}?",
                        "kind": "scatter",
                        "category": useful_numeric[0],
                        "metric": useful_numeric[1]
                    })

                # Keep recommendations unique and cap the first release to 5 clear suggestions.
                unique_recommendations = []
                seen_titles = set()
                for rec in recommendations:
                    if rec["title"] not in seen_titles:
                        unique_recommendations.append(rec)
                        seen_titles.add(rec["title"])
                unique_recommendations = unique_recommendations[:5]

                if not unique_recommendations:
                    st.info("This dataset does not yet contain enough suitable numeric or categorical columns to recommend charts. Try a dataset with category and numeric fields.")
                else:
                    for number, rec in enumerate(unique_recommendations, start=1):
                        with st.container(border=True):
                            st.markdown(f"**{number}. {rec['title']}**")
                            st.write(f"**Recommended chart:** {rec['type']}")
                            st.write(f"**X-axis:** `{rec['x']}`")
                            st.write(f"**Y-axis:** `{rec['y']}`")
                            st.write(f"**Business question:** {rec['question']}")



                st.divider()
                st.success("Dashboard recommendations are ready for this uploaded dataset.")
    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.divider()
    st.subheader("📝 Download Your Analysis Report")
    st.write(
        "Download a portable HTML report that you can open in a browser "
        "and print or save as PDF. You can also download the cleaned dataset as CSV."
    )

    report_df = st.session_state.get("cleaned_df")

    if report_df is not None and not report_df.empty:
        from datetime import datetime
        from html import escape

        dataset_name = st.session_state.get("uploaded_name") or "Uploaded dataset"
        numeric_report_cols = report_df.select_dtypes(include=["number"]).columns.tolist()
        missing_report = report_df.isna().sum().rename("Missing values").to_frame()
        missing_report = missing_report[missing_report["Missing values"] > 0]

        if numeric_report_cols:
            numeric_summary_html = report_df[numeric_report_cols].describe().round(2).to_html(
                classes="data-table", border=0
            )
        else:
            numeric_summary_html = "<p>No numeric columns were available for summary statistics.</p>"

        if not missing_report.empty:
            missing_html = missing_report.to_html(classes="data-table", border=0)
        else:
            missing_html = "<p>No missing values were found in the cleaned dataset.</p>"

        try:
            report_insights = analyze.generate_insights(report_df)
            if report_insights:
                insights_html = "<ul>" + "".join(
                    f"<li>{escape(str(item))}</li>" for item in report_insights
                ) + "</ul>"
            else:
                insights_html = "<p>No automatic insights were generated.</p>"
        except Exception:
            insights_html = "<p>Automatic insights were unavailable when this report was generated.</p>"

        report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Captain Analyst Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 36px auto; padding: 0 20px; max-width: 1100px; color: #172033; line-height: 1.55; }}
h1 {{ color: #1d4ed8; }} h2 {{ margin-top: 30px; color: #1e3a8a; }}
.summary {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.metric {{ border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px 18px; min-width: 150px; }}
.metric strong {{ display: block; font-size: 23px; overflow-wrap: anywhere; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0 22px; font-size: 13px; }}
th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: left; overflow-wrap: anywhere; }}
th {{ background: #eff6ff; }}
@media print {{ body {{ margin: 12mm; }} }}
</style>
</head>
<body>
<h1>🧢 Captain Analyst — Analysis Report</h1>
<p><strong>Dataset:</strong> {escape(str(dataset_name))}<br>
<strong>Generated:</strong> {datetime.now().strftime('%d %B %Y, %I:%M %p')}<br>
<strong>Report data:</strong> cleaned dataset</p>
<h2>Dataset Overview</h2>
<div class="summary">
<div class="metric"><strong>{len(report_df):,}</strong>Records</div>
<div class="metric"><strong>{len(report_df.columns):,}</strong>Columns</div>
<div class="metric"><strong>{len(numeric_report_cols):,}</strong>Numeric columns</div>
<div class="metric"><strong>{int(report_df.isna().sum().sum()):,}</strong>Remaining missing cells</div>
</div>
<h2>Automated Insights</h2>
{insights_html}
<h2>Numeric Summary Statistics</h2>
{numeric_summary_html}
<h2>Missing Values</h2>
{missing_html}
<h2>Column List</h2>
<p>{escape(', '.join(map(str, report_df.columns)))}</p>
<hr><p>Generated by Captain Analyst.</p>
<p>To save as PDF: open this HTML file in a browser, press Ctrl+P, and choose “Save as PDF”.</p>
</body></html>"""

        download_col1, download_col2 = st.columns(2)
        with download_col1:
            st.download_button(
                "📄 Download HTML Analysis Report",
                data=report_html,
                file_name="captain_analyst_report.html",
                mime="text/html",
                width="stretch",
                key="download_html_report"
            )
        with download_col2:
            st.download_button(
                "📊 Download Cleaned Dataset (CSV)",
                data=report_df.to_csv(index=False).encode("utf-8-sig"),
                file_name="captain_analyst_cleaned_data.csv",
                mime="text/csv",
                width="stretch",
                key="download_cleaned_csv"
            )
    else:
        st.info("Upload and process a dataset before downloading a report.")

    # =====================================================
    # START NEW MISSION
    # =====================================================

    st.write("")


    if st.button(
        "🔄 Start New Mission",
        width="stretch"
    ):

        st.session_state.mission_started = False

        st.session_state.mission_complete = False

        st.session_state["show_dashboard"] = False

        # Clear old dashboard filters so they cannot affect the next dataset.
        for state_key in list(st.session_state.keys()):
            if state_key.startswith("dash_filter_"):
                del st.session_state[state_key]

        st.session_state.uploaded_name = None

        st.session_state.pop(
            "uploaded_file",
            None
        )

        st.rerun()
