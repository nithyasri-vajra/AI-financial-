import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import html


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Investment Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1550px;
        padding: 2rem 2.5rem 3rem 2.5rem;
    }

    .dashboard-title {
        font-size: 30px;
        font-weight: 700;
        color: #101828;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 14px;
        color: #667085;
        margin-bottom: 25px;
    }

    .company-header {
        background: #ffffff;
        border: 1px solid #eaecf0;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 22px;
    }

    .company-name {
        font-size: 22px;
        font-weight: 700;
        color: #101828;
    }

    .company-meta {
        margin-top: 5px;
        font-size: 13px;
        color: #667085;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #eaecf0;
        border-radius: 14px;
        padding: 18px;
        min-height: 125px;
    }

    .metric-title {
        color: #667085;
        font-size: 13px;
        margin-bottom: 9px;
    }

    .metric-value {
        color: #101828;
        font-size: 25px;
        font-weight: 700;
    }

    .metric-change-positive {
        color: #12b76a;
        font-size: 12px;
        margin-top: 7px;
    }

    .metric-change-negative {
        color: #f04438;
        font-size: 12px;
        margin-top: 7px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 650;
        color: #101828;
        margin-top: 28px;
        margin-bottom: 13px;
    }

    .risk-card {
        background: #fff8f7;
        border: 1px solid #fecdca;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .change-card {
        background: #f8faff;
        border: 1px solid #d1e0ff;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .source-card {
        background: #f9fafb;
        border: 1px solid #eaecf0;
        border-radius: 10px;
        padding: 13px 16px;
        margin-bottom: 8px;
    }

    .insight-card {
        background: #f8faff;
        border: 1px solid #d1e0ff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def safe_value(value):
    """
    Display value coming from the analysed Drive data.
    No financial value is created here.
    """

    if value is None or value == "":
        return "N/A"

    return str(value)


def escape(value):
    return html.escape(str(value))


def change_html(value):

    if value is None or value == "":
        return ""

    try:

        number = float(value)

        if number >= 0:

            return (
                f'<div class="metric-change-positive">'
                f'↑ {number}%'
                f'</div>'
            )

        return (
            f'<div class="metric-change-negative">'
            f'↓ {abs(number)}%'
            f'</div>'
        )

    except Exception:

        return (
            f'<div class="metric-change-positive">'
            f'{escape(value)}'
            f'</div>'
        )


# ============================================================
# NORMALIZE DATA
# ============================================================

def normalize_companies(analysis_data):

    if not analysis_data:
        return {}

    # Multiple-company format:
    #
    # {
    #   "Company A": {...},
    #   "Company B": {...}
    # }

    if isinstance(analysis_data, dict):

        if "company" in analysis_data:

            company_name = analysis_data.get(
                "company",
                "Company"
            )

            return {
                company_name: analysis_data
            }

        return analysis_data

    return {}


# ============================================================
# KPI CARD
# ============================================================

def metric_card(title, value, change=None):

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                {escape(title)}
            </div>

            <div class="metric-value">
                {escape(safe_value(value))}
            </div>

            {change_html(change)}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard(analysis_data):

    # --------------------------------------------------------
    # Prepare company data
    # --------------------------------------------------------

    companies = normalize_companies(
        analysis_data
    )

    if not companies:

        st.warning(
            "No financial data is available for the dashboard."
        )

        return


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        '<div class="dashboard-title">'
        'Investment Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Financial performance, valuation context and risk overview'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown(
            "## Investment Intelligence"
        )

        st.caption(
            "Financial document analysis"
        )

        st.divider()

        page = st.radio(
            "Dashboard",
            [
                "Overview",
                "Financial Performance",
                "Risk Analysis",
                "AI Insights",
                "Source Documents"
            ]
        )

        st.divider()

        st.caption(
            f"{len(companies)} compan{'y' if len(companies) == 1 else 'ies'} available"
        )


    # ========================================================
    # COMPANY SELECTOR
    # ========================================================

    company_names = list(
        companies.keys()
    )

    selected_company = st.selectbox(
        "Company",
        company_names
    )

    company_data = companies.get(
        selected_company,
        {}
    )


    # ========================================================
    # COMPANY INFORMATION
    # ========================================================

    sector = company_data.get(
        "sector",
        "Not available"
    )

    country = company_data.get(
        "country",
        "Not available"
    )

    period = company_data.get(
        "reporting_period",
        "Latest available"
    )


    st.markdown(
        f"""
        <div class="company-header">

            <div class="company-name">
                {escape(selected_company)}
            </div>

            <div class="company-meta">
                {escape(sector)}
                &nbsp; · &nbsp;
                {escape(country)}
                &nbsp; · &nbsp;
                Reporting period: {escape(period)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    financials = company_data.get(
        "financials",
        {}
    )


    # ========================================================
    # OVERVIEW
    # ========================================================

    if page == "Overview":

        st.markdown(
            '<div class="section-title">'
            'Financial Overview'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            metric_card(
                "Revenue",
                financials.get("revenue"),
                financials.get("revenue_change")
            )

        with c2:

            metric_card(
                "Net Income",
                financials.get("net_income"),
                financials.get("net_income_change")
            )

        with c3:

            metric_card(
                "EPS",
                financials.get("eps"),
                financials.get("eps_change")
            )

        with c4:

            metric_card(
                "Total Assets",
                financials.get("total_assets")
            )

        with c5:

            metric_card(
                "Cash",
                financials.get("cash")
            )


        # ----------------------------------------------------
        # PERFORMANCE + SEGMENTS
        # ----------------------------------------------------

        left, right = st.columns(
            [1.7, 1]
        )


        # ====================================================
        # PERFORMANCE GRAPH
        # ====================================================

        with left:

            st.markdown(
                '<div class="section-title">'
                'Financial Performance'
                '</div>',
                unsafe_allow_html=True
            )

            historical = company_data.get(
                "historical",
                []
            )

            if historical:

                df = pd.DataFrame(
                    historical
                )

                if "period" in df.columns:

                    chart_columns = []

                    if "revenue" in df.columns:
                        chart_columns.append(
                            "revenue"
                        )

                    if "net_income" in df.columns:
                        chart_columns.append(
                            "net_income"
                        )

                    if chart_columns:

                        chart_df = df[
                            ["period"] + chart_columns
                        ].copy()

                        chart_df = chart_df.rename(
                            columns={
                                "revenue": "Revenue",
                                "net_income": "Net Income"
                            }
                        )

                        chart_df = chart_df.set_index(
                            "period"
                        )

                        st.line_chart(
                            chart_df,
                            height=360,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "Historical financial data is not available."
                        )

                else:

                    st.info(
                        "Historical periods are not available."
                    )

            else:

                st.info(
                    "Historical financial data is not available."
                )


        # ====================================================
        # SEGMENT DONUT
        # ====================================================

        with right:

            st.markdown(
                '<div class="section-title">'
                'Business Segment Mix'
                '</div>',
                unsafe_allow_html=True
            )

            segments = company_data.get(
                "segment_breakdown",
                []
            )

            valid_segments = []

            for segment in segments:

                if (
                    segment.get("name")
                    and segment.get("value") is not None
                ):

                    valid_segments.append(
                        segment
                    )

            if valid_segments:

                segment_df = pd.DataFrame(
                    valid_segments
                )

                fig = px.pie(
                    segment_df,
                    names="name",
                    values="value",
                    hole=0.58
                )

                fig.update_layout(
                    height=360,
                    margin=dict(
                        l=5,
                        r=5,
                        t=10,
                        b=5
                    ),
                    legend=dict(
                        orientation="h",
                        y=-0.1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "Business segment data is not available."
                )


        # ----------------------------------------------------
        # FINANCIAL POSITION
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Financial Position'
            '</div>',
            unsafe_allow_html=True
        )

        balance = []

        for key, label in [
            ("total_assets", "Assets"),
            ("total_debt", "Debt"),
            ("cash", "Cash")
        ]:

            value = financials.get(
                key
            )

            if value is not None:

                balance.append(
                    {
                        "Metric": label,
                        "Value": value
                    }
                )

        if balance:

            balance_df = pd.DataFrame(
                balance
            )

            fig = px.bar(
                balance_df,
                x="Metric",
                y="Value",
                text_auto=True
            )

            fig.update_layout(
                height=320,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),
                xaxis_title=None,
                yaxis_title=None
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Financial position data is not available."
            )


        # ----------------------------------------------------
        # MULTI COMPANY COMPARISON
        # ----------------------------------------------------

        if len(companies) > 1:

            st.markdown(
                '<div class="section-title">'
                'Company Comparison'
                '</div>',
                unsafe_allow_html=True
            )

            comparison = []

            for name, data in companies.items():

                company_financials = data.get(
                    "financials",
                    {}
                )

                comparison.append(
                    {
                        "Company": name,
                        "Revenue": company_financials.get(
                            "revenue"
                        ),
                        "Net Income": company_financials.get(
                            "net_income"
                        )
                    }
                )

            comparison_df = pd.DataFrame(
                comparison
            )

            comparison_df = comparison_df.dropna(
                subset=["Revenue"],
                how="all"
            )

            if not comparison_df.empty:

                fig = px.bar(
                    comparison_df,
                    x="Company",
                    y=[
                        "Revenue",
                        "Net Income"
                    ],
                    barmode="group"
                )

                fig.update_layout(
                    height=380,
                    xaxis_title=None,
                    yaxis_title=None
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


    # ========================================================
    # FINANCIAL PERFORMANCE
    # ========================================================

    elif page == "Financial Performance":

        st.markdown(
            '<div class="section-title">'
            'Financial Performance'
            '</div>',
            unsafe_allow_html=True
        )

        historical = company_data.get(
            "historical",
            []
        )

        if not historical:

            st.info(
                "Historical financial data is not available."
            )

        else:

            df = pd.DataFrame(
                historical
            )


            # Revenue
            if "revenue" in df.columns:

                revenue_df = df[
                    ["period", "revenue"]
                ].dropna()

                if not revenue_df.empty:

                    revenue_df = revenue_df.rename(
                        columns={
                            "period": "Period",
                            "revenue": "Revenue"
                        }
                    )

                    fig = px.line(
                        revenue_df,
                        x="Period",
                        y="Revenue",
                        markers=True,
                        title="Revenue Trend"
                    )

                    fig.update_layout(
                        height=400
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


            # Net Income
            if "net_income" in df.columns:

                income_df = df[
                    ["period", "net_income"]
                ].dropna()

                if not income_df.empty:

                    income_df = income_df.rename(
                        columns={
                            "period": "Period",
                            "net_income": "Net Income"
                        }
                    )

                    fig = px.bar(
                        income_df,
                        x="Period",
                        y="Net Income",
                        title="Net Income Trend"
                    )

                    fig.update_layout(
                        height=400
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


            st.markdown(
                '<div class="section-title">'
                'Historical Financial Data'
                '</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # ========================================================
    # RISK ANALYSIS
    # ========================================================

    elif page == "Risk Analysis":

        st.markdown(
            '<div class="section-title">'
            'Risk Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        risks = company_data.get(
            "risks",
            []
        )

        if not risks:

            st.info(
                "Risk information is not available in the documents."
            )

        else:

            for risk in risks:

                name = risk.get(
                    "name",
                    "Risk"
                )

                level = risk.get(
                    "level",
                    "Not specified"
                )

                description = risk.get(
                    "description",
                    ""
                )

                st.markdown(
                    f"""
                    <div class="risk-card">

                        <b>{escape(name)}</b>

                        <br><br>

                        Risk level:
                        <b>{escape(level)}</b>

                        <br><br>

                        {escape(description)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # AI INSIGHTS
    # ========================================================

    elif page == "AI Insights":

        st.markdown(
            '<div class="section-title">'
            'Financial Insights'
            '</div>',
            unsafe_allow_html=True
        )

        insights = company_data.get(
            "investment_insights",
            []
        )

        if insights:

            for insight in insights:

                st.markdown(
                    f"""
                    <div class="insight-card">
                        {escape(insight)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No financial insights were found."
            )


        st.markdown(
            '<div class="section-title">'
            'Recent Changes'
            '</div>',
            unsafe_allow_html=True
        )

        changes = company_data.get(
            "recent_changes",
            []
        )

        if changes:

            for change in changes:

                st.markdown(
                    f"""
                    <div class="change-card">
                        {escape(change)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No recent financial changes were found."
            )


    # ========================================================
    # SOURCE DOCUMENTS
    # ========================================================

    elif page == "Source Documents":

        st.markdown(
            '<div class="section-title">'
            'Source Documents'
            '</div>',
            unsafe_allow_html=True
        )

        documents = company_data.get(
            "documents",
            []
        )

        if documents:

            for document in documents:

                if isinstance(document, dict):

                    name = document.get(
                        "name",
                        "Document"
                    )

                    link = document.get(
                        "link",
                        ""
                    )

                else:

                    name = document
                    link = ""


                if link:

                    st.markdown(
                        f"""
                        <div class="source-card">

                            📄 <b>{escape(name)}</b>

                            <br><br>

                            <a href="{escape(link)}"
                               target="_blank">
                               Open document
                            </a>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="source-card">
                            📄 <b>{escape(name)}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.info(
                "No source documents are available."
            )