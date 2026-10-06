import json
import os

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# SETUP
# ============================================================

KNOWLEDGE_FILE = "financial_knowledge.json"


# ============================================================
# LOAD FINANCIAL KNOWLEDGE
# ============================================================

def load_knowledge():

    if not os.path.exists(KNOWLEDGE_FILE):

        return {
            "documents": []
        }

    try:

        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception:

        return {
            "documents": []
        }

    if not isinstance(data, dict):

        return {
            "documents": []
        }

    documents = data.get(
        "documents",
        []
    )

    if not isinstance(documents, list):

        documents = []

    data["documents"] = documents

    return data


# ============================================================
# HELPERS
# ============================================================

def display_value(value):

    if value is None:
        return "N/A"

    if value == "":
        return "N/A"

    return str(value)


def render_metric(
    title,
    value,
    change=None
):

    with st.container(
        border=True
    ):

        st.caption(
            title
        )

        st.subheader(
            display_value(value)
        )

        if change is not None and change != "":

            st.caption(
                f"Change: {change}"
            )


def render_list(
    items
):

    if not isinstance(
        items,
        list
    ):
        return

    for item in items:

        if isinstance(
            item,
            str
        ):

            text = item

        elif isinstance(
            item,
            dict
        ):

            text = (
                item.get("text")
                or item.get("description")
                or item.get("insight")
                or item.get("risk")
                or item.get("change")
                or ""
            )

        else:

            continue

        if not text:
            continue

        with st.container(
            border=True
        ):

            st.write(
                text
            )


def get_document_name(
    document
):

    return (
        document.get("company")
        or document.get("file_name")
        or "Unknown document"
    )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard(
    knowledge
):

    documents = knowledge.get(
        "documents",
        []
    )


    if not documents:

        st.warning(
            "No financial document summaries are available."
        )

        return


    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "Investment Intelligence"
    )

    st.caption(
        "Dashboard generated from financial document summaries"
    )


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown(
            "## Investment Intelligence"
        )

        st.caption(
            "Financial document summaries"
        )

        st.divider()

        page = st.radio(
            "Dashboard",
            [
                "Overview",
                "Financial Performance",
                "Business Performance",
                "Risk Analysis",
                "AI Insights",
                "Source Documents"
            ]
        )

        st.divider()

        st.caption(
            f"{len(documents)} document summary(s)"
        )


    # ========================================================
    # COMPANY SELECTOR
    # ========================================================

    company_names = []

    for document in documents:

        if not isinstance(
            document,
            dict
        ):
            continue

        company_names.append(
            get_document_name(
                document
            )
        )


    if not company_names:

        st.warning(
            "No usable financial documents are available."
        )

        return


    selected_company = st.selectbox(
        "Company",
        company_names
    )


    selected_index = company_names.index(
        selected_company
    )

    document = documents[
        selected_index
    ]


    # ========================================================
    # DOCUMENT DATA
    # ========================================================

    financials = document.get(
        "financials",
        {}
    )

    historical = document.get(
        "historical",
        []
    )

    segments = document.get(
        "segment_breakdown",
        []
    )

    drivers = document.get(
        "operating_drivers",
        []
    )

    guidance = document.get(
        "management_guidance",
        []
    )

    risks = document.get(
        "risks",
        []
    )

    insights = document.get(
        "investment_insights",
        []
    )

    changes = document.get(
        "recent_changes",
        []
    )

    outlook = document.get(
        "outlook",
        []
    )

    summary = document.get(
        "summary",
        ""
    )

    file_name = document.get(
        "file_name",
        selected_company
    )

    drive_link = document.get(
        "drive_link",
        ""
    )


    # ========================================================
    # COMPANY HEADER
    # ========================================================

    meta = []

    industry = document.get(
        "industry"
    )

    country = document.get(
        "country"
    )

    reporting_period = document.get(
        "reporting_period"
    )

    if industry:

        meta.append(
            str(industry)
        )

    if country:

        meta.append(
            str(country)
        )

    if reporting_period:

        meta.append(
            f"Reporting period: {reporting_period}"
        )


    with st.container(
        border=True
    ):

        st.subheader(
            selected_company
        )

        if meta:

            st.caption(
                " · ".join(meta)
            )


    # ========================================================
    # OVERVIEW
    # ========================================================

    if page == "Overview":

        st.subheader(
            "Investment Overview"
        )


        columns = st.columns(
            5
        )


        metrics = [

            (
                "Revenue",
                financials.get(
                    "revenue"
                ),
                financials.get(
                    "revenue_change"
                )
            ),

            (
                "Net Income",
                financials.get(
                    "net_income"
                ),
                financials.get(
                    "net_income_change"
                )
            ),

            (
                "Operating Income",
                financials.get(
                    "operating_income"
                ),
                financials.get(
                    "operating_income_change"
                )
            ),

            (
                "EPS",
                financials.get(
                    "eps"
                ),
                financials.get(
                    "eps_change"
                )
            ),

            (
                "Free Cash Flow",
                financials.get(
                    "free_cash_flow"
                ),
                financials.get(
                    "free_cash_flow_change"
                )
            )
        ]


        for column, metric in zip(
            columns,
            metrics
        ):

            with column:

                render_metric(
                    metric[0],
                    metric[1],
                    metric[2]
                )


        # ====================================================
        # HISTORICAL PERFORMANCE
        # ====================================================

        if historical:

            rows = []

            for item in historical:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                period = (
                    item.get("period")
                    or item.get("year")
                    or item.get("date")
                )

                if not period:
                    continue

                row = {
                    "Period": str(
                        period
                    )
                }

                for key in [
                    "revenue",
                    "net_income",
                    "operating_income",
                    "ebitda"
                ]:

                    value = item.get(
                        key
                    )

                    if value is None:
                        continue

                    try:

                        row[key] = float(
                            value
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        continue

                rows.append(
                    row
                )


            if rows:

                df = pd.DataFrame(
                    rows
                )


                chart_columns = [
                    column
                    for column in [
                        "revenue",
                        "net_income",
                        "operating_income",
                        "ebitda"
                    ]
                    if column in df.columns
                ]


                if chart_columns:

                    st.subheader(
                        "Historical Performance"
                    )


                    rename_map = {

                        "revenue":
                            "Revenue",

                        "net_income":
                            "Net Income",

                        "operating_income":
                            "Operating Income",

                        "ebitda":
                            "EBITDA"
                    }


                    chart_df = df[
                        ["Period"] + chart_columns
                    ].rename(
                        columns=rename_map
                    )


                    fig = px.line(
                        chart_df,
                        x="Period",
                        y=[
                            rename_map[column]
                            for column in chart_columns
                        ],
                        markers=True
                    )


                    fig.update_layout(
                        height=400,
                        hovermode="x unified",
                        legend_title=None
                    )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


        # ====================================================
        # BUSINESS MIX
        # ====================================================

        if segments:

            segment_rows = []

            for item in segments:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                name = (
                    item.get("name")
                    or item.get("segment")
                )

                value = (
                    item.get("value")
                    if item.get("value") is not None
                    else item.get("revenue")
                )

                if value is None:

                    value = item.get(
                        "income"
                    )

                if not name or value is None:
                    continue

                try:

                    segment_rows.append(
                        {
                            "Segment": name,
                            "Value": float(
                                value
                            )
                        }
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue


            if segment_rows:

                segment_df = pd.DataFrame(
                    segment_rows
                )


                st.subheader(
                    "Business Mix"
                )


                fig = px.pie(
                    segment_df,
                    names="Segment",
                    values="Value",
                    hole=0.55
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


    # ========================================================
    # FINANCIAL PERFORMANCE
    # ========================================================

    elif page == "Financial Performance":

        st.subheader(
            "Financial Performance"
        )


        rows = []

        for item in historical:

            if not isinstance(
                item,
                dict
            ):
                continue

            period = (
                item.get("period")
                or item.get("year")
                or item.get("date")
            )

            if not period:
                continue

            row = {
                "Period": str(
                    period
                )
            }


            for key in [
                "revenue",
                "net_income",
                "operating_income",
                "ebitda",
                "eps",
                "free_cash_flow"
            ]:

                value = item.get(
                    key
                )

                if value is None:
                    continue

                try:

                    row[key] = float(
                        value
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue


            rows.append(
                row
            )


        if not rows:

            st.info(
                "Historical financial data is not available in the summary."
            )

        else:

            df = pd.DataFrame(
                rows
            )


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            for metric in [
                "revenue",
                "net_income",
                "operating_income",
                "ebitda",
                "eps",
                "free_cash_flow"
            ]:

                if metric not in df.columns:
                    continue


                chart_df = df[
                    ["Period", metric]
                ].dropna()


                if chart_df.empty:
                    continue


                label = metric.replace(
                    "_",
                    " "
                ).title()


                fig = px.line(
                    chart_df,
                    x="Period",
                    y=metric,
                    markers=True,
                    title=f"{label} Trend"
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


    # ========================================================
    # BUSINESS PERFORMANCE
    # ========================================================

    elif page == "Business Performance":

        st.subheader(
            "Business Performance"
        )


        if segments:

            rows = []

            for item in segments:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                name = (
                    item.get("name")
                    or item.get("segment")
                )

                value = (
                    item.get("value")
                    if item.get("value") is not None
                    else item.get("revenue")
                )

                if value is None:

                    value = item.get(
                        "income"
                    )

                if not name or value is None:
                    continue

                try:

                    rows.append(
                        {
                            "Segment": name,
                            "Value": float(
                                value
                            )
                        }
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    continue


            if rows:

                df = pd.DataFrame(
                    rows
                )


                left, right = st.columns(
                    2
                )


                with left:

                    fig = px.bar(
                        df,
                        x="Segment",
                        y="Value",
                        text_auto=True
                    )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


                with right:

                    fig = px.pie(
                        df,
                        names="Segment",
                        values="Value",
                        hole=0.55
                    )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


        else:

            st.info(
                "Business segment information is not available in the summary."
            )


        if drivers:

            st.subheader(
                "Key Business Drivers"
            )

            render_list(
                drivers
            )


        if guidance:

            st.subheader(
                "Management Guidance"
            )

            render_list(
                guidance
            )


    # ========================================================
    # RISK ANALYSIS
    # ========================================================

    elif page == "Risk Analysis":

        st.subheader(
            "Risk Analysis"
        )


        if not risks:

            st.info(
                "Risk information is not available in the summary."
            )

        else:

            for risk in risks:

                if isinstance(
                    risk,
                    dict
                ):

                    name = (
                        risk.get("name")
                        or risk.get("risk")
                        or "Risk"
                    )

                    level = risk.get(
                        "level",
                        "Not specified"
                    )

                    description = (
                        risk.get("description")
                        or risk.get("text")
                        or ""
                    )


                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{name}**"
                        )

                        st.write(
                            f"Risk level: {level}"
                        )

                        if description:

                            st.write(
                                description
                            )


                elif isinstance(
                    risk,
                    str
                ):

                    with st.container(
                        border=True
                    ):

                        st.write(
                            risk
                        )


    # ========================================================
    # AI INSIGHTS
    # ========================================================

    elif page == "AI Insights":

        st.subheader(
            "AI Insights"
        )


        if summary:

            with st.container(
                border=True
            ):

                st.write(
                    summary
                )


        if insights:

            st.subheader(
                "Key Insights"
            )

            render_list(
                insights
            )


        if changes:

            st.subheader(
                "Recent Material Changes"
            )

            render_list(
                changes
            )


        if outlook:

            st.subheader(
                "Outlook"
            )

            render_list(
                outlook
            )


    # ========================================================
    # SOURCE DOCUMENT
    # ========================================================

    elif page == "Source Documents":

        st.subheader(
            "Source Document"
        )


        with st.container(
            border=True
        ):

            st.write(
                f"📄 {file_name}"
            )


            if drive_link:

                st.markdown(
                    f"[Open document]({drive_link})"
                )

            else:

                st.info(
                    "Drive link not available."
                )