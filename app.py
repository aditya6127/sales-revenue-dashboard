import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "Sales_Revenue_Dashboard_Dataset.xlsx"
    )

    df.columns = df.columns.str.strip()

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Revenue"] = pd.to_numeric(
        df["Revenue"],
        errors="coerce"
    ).fillna(0)

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    ).fillna(0)

    return df.dropna(
        subset=["Order Date"]
    )


df = load_data()

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN ---------- */

    .stApp {
        background-color: #080d16;
        color: #e2e8f0;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background-color: #060a11 !important;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: #cbd5e1;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #1e293b !important;
    }

    /* ---------- HEADINGS ---------- */

    h1 {
        color: #f8fafc !important;
        font-weight: 750 !important;
    }

    h2 {
        color: #e2e8f0 !important;
    }

    h3 {
        color: #cbd5e1 !important;
    }

    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {
        background-color: #0d1522;
        border: 1px solid #1e293b;
        border-radius: 4px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 24px !important;
        font-weight: 750 !important;
    }

    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #263449 !important;
        color: #e2e8f0 !important;
    }

    /* ---------- DIVIDERS ---------- */

    hr {
        border-color: #1e293b !important;
    }

    /* ---------- TABLE ---------- */

    div[data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## SALES TERMINAL")

    st.caption("BUSINESS INTELLIGENCE")

    st.divider()

    st.caption("NAVIGATION")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Sales",
            "Products",
            "Regions",
            "Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("DATASET STATUS")

    st.write(
        f"Orders  **{df['Order ID'].nunique():,}**"
    )

    st.write(
        f"Products  **{df['Product'].nunique():,}**"
    )

    st.write(
        f"Regions  **{df['Region'].nunique():,}**"
    )

    st.divider()

    st.success("DATA CONNECTED")




# ============================================================
# FILTER SECTION
# ============================================================

st.caption("MARKET FILTERS")

filter1, filter2, filter3 = st.columns(3)

# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

with filter1:

    region_options = sorted(
        df["Region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_region = st.selectbox(
        "REGION",
        ["All Regions"] + region_options
    )

filtered_df = df.copy()

if selected_region != "All Regions":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

# ------------------------------------------------------------
# CATEGORY FILTER
# ------------------------------------------------------------

with filter2:

    category_options = sorted(
        filtered_df["Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "CATEGORY",
        ["All Categories"] + category_options
    )

if selected_category != "All Categories":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# ------------------------------------------------------------
# PRODUCT FILTER
# ------------------------------------------------------------

with filter3:

    product_options = sorted(
        filtered_df["Product"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "PRODUCT",
        ["All Products"] + product_options
    )

if selected_product != "All Products":

    filtered_df = filtered_df[
        filtered_df["Product"] == selected_product
    ]

# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No sales data available for the selected filters."
    )

    st.stop()

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_units = filtered_df["Quantity"].sum()

average_order = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.title(
        "Sales & Revenue Analytics"
    )

    st.caption(
        "Real-time business performance overview"
    )

    st.divider()

    # --------------------------------------------------------
    # KPI STRIP
    # --------------------------------------------------------

    st.caption("MARKET OVERVIEW")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "TOTAL REVENUE",
            f"₹{total_revenue:,.0f}"
        )

    with k2:

        st.metric(
            "TOTAL ORDERS",
            f"{total_orders:,}"
        )

    with k3:

        st.metric(
            "UNITS SOLD",
            f"{total_units:,.0f}"
        )

    with k4:

        st.metric(
            "AVG ORDER VALUE",
            f"₹{average_order:,.0f}"
        )

    # --------------------------------------------------------
    # REVENUE CHART
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Revenue Performance"
    )

    monthly = (
        filtered_df
        .assign(
            Month=filtered_df["Order Date"].dt.to_period("M")
        )
        .groupby(
            "Month",
            as_index=False
        )["Revenue"]
        .sum()
    )

    monthly["Month"] = (
        monthly["Month"]
        .dt
        .to_timestamp()
    )

    monthly = monthly.sort_values(
        "Month"
    )

    fig_revenue = px.area(
        monthly,
        x="Month",
        y="Revenue"
    )

    fig_revenue.update_traces(
        line=dict(
            color="#3b82f6",
            width=2
        ),
        fillcolor="rgba(59,130,246,0.12)",
        hovertemplate=
        "<b>%{x|%b %Y}</b><br>" +
        "Revenue: ₹%{y:,.0f}" +
        "<extra></extra>"
    )

    fig_revenue.update_layout(
        template="plotly_dark",
        height=420,
        paper_bgcolor="#0d1522",
        plot_bgcolor="#0d1522",
        margin=dict(
            l=50,
            r=30,
            t=20,
            b=45
        ),
        xaxis_title="",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    fig_revenue.update_xaxes(
        showgrid=False
    )

    fig_revenue.update_yaxes(
        showgrid=True,
        gridcolor="#1e293b"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REGION + CATEGORY
    # --------------------------------------------------------

    left, right = st.columns(2)

    # REGION

    with left:

        st.subheader(
            "Revenue by Region"
        )

        region_sales = (
            filtered_df
            .groupby(
                "Region",
                as_index=False
            )["Revenue"]
            .sum()
            .sort_values(
                "Revenue",
                ascending=False
            )
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Revenue",
            text_auto=".2s"
        )

        fig_region.update_traces(
            marker_color="#3b82f6",
            marker_line_width=0,
            textposition="outside"
        )

        fig_region.update_layout(
            template="plotly_dark",
            height=350,
            paper_bgcolor="#0d1522",
            plot_bgcolor="#0d1522",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=30
            ),
            xaxis_title="Region",
            yaxis_title="Revenue (₹)"
        )

        fig_region.update_xaxes(
            showgrid=False
        )

        fig_region.update_yaxes(
            showgrid=True,
            gridcolor="#1e293b"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    # CATEGORY

    with right:

        st.subheader(
            "Revenue by Category"
        )

        category_sales = (
            filtered_df
            .groupby(
                "Category",
                as_index=False
            )["Revenue"]
            .sum()
            .sort_values(
                "Revenue",
                ascending=False
            )
        )

        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Revenue",
            text_auto=".2s"
        )

        fig_category.update_traces(
            marker_color="#22c55e",
            marker_line_width=0,
            textposition="outside"
        )

        fig_category.update_layout(
            template="plotly_dark",
            height=350,
            paper_bgcolor="#0d1522",
            plot_bgcolor="#0d1522",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=30
            ),
            xaxis_title="Category",
            yaxis_title="Revenue (₹)"
        )

        fig_category.update_xaxes(
            showgrid=False
        )

        fig_category.update_yaxes(
            showgrid=True,
            gridcolor="#1e293b"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Top Performing Products"
    )

    top_products = (
        filtered_df
        .groupby(
            "Product",
            as_index=False
        )["Revenue"]
        .sum()
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Revenue",
            ascending=True
        )
    )

    fig_products = px.bar(
        top_products,
        x="Revenue",
        y="Product",
        orientation="h",
        text_auto=".2s"
    )

    fig_products.update_traces(
        marker_color="#60a5fa",
        marker_line_width=0
    )

    fig_products.update_layout(
        template="plotly_dark",
        height=430,
        paper_bgcolor="#0d1522",
        plot_bgcolor="#0d1522",
        margin=dict(
            l=20,
            r=40,
            t=20,
            b=30
        ),
        xaxis_title="Revenue (₹)",
        yaxis_title=""
    )

    fig_products.update_xaxes(
        showgrid=True,
        gridcolor="#1e293b"
    )

    fig_products.update_yaxes(
        showgrid=False
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

# ============================================================
# SALES PAGE
# ============================================================

elif page == "Sales":

    st.title("Sales Activity")

    st.caption(
        f"{len(filtered_df):,} transactions"
    )

    st.divider()

    st.dataframe(
        filtered_df.sort_values(
            "Order Date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PRODUCTS PAGE
# ============================================================

elif page == "Products":

    st.title("Product Performance")

    st.caption(
        "Product-level revenue and volume analysis"
    )

    product_data = (
        filtered_df
        .groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    st.divider()

    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# REGIONS PAGE
# ============================================================

elif page == "Regions":

    st.title("Regional Performance")

    st.caption(
        "Revenue distribution across business regions"
    )

    region_data = (
        filtered_df
        .groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Order ID", "nunique"),
            Units=("Quantity", "sum")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    st.divider()

    st.dataframe(
        region_data,
        use_container_width=True,
        hide_index=True
    )

    fig_regions = px.bar(
        region_data,
        x="Region",
        y="Revenue",
        text_auto=".2s"
    )

    fig_regions.update_traces(
        marker_color="#3b82f6"
    )

    fig_regions.update_layout(
        template="plotly_dark",
        height=400,
        paper_bgcolor="#0d1522",
        plot_bgcolor="#0d1522",
        xaxis_title="Region",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_regions,
        use_container_width=True
    )

# ============================================================
# INSIGHTS PAGE
# ============================================================

elif page == "Insights":

    st.title("Business Insights")

    st.caption(
        "Key findings from the current dataset selection"
    )

    product_revenue = (
        filtered_df
        .groupby("Product")["Revenue"]
        .sum()
    )

    region_revenue = (
        filtered_df
        .groupby("Region")["Revenue"]
        .sum()
    )

    category_revenue = (
        filtered_df
        .groupby("Category")["Revenue"]
        .sum()
    )

    best_product = product_revenue.idxmax()

    best_region = region_revenue.idxmax()

    best_category = category_revenue.idxmax()

    st.divider()

    i1, i2, i3 = st.columns(3)

    with i1:

        st.metric(
            "TOP PRODUCT",
            best_product
        )

    with i2:

        st.metric(
            "TOP REGION",
            best_region
        )

    with i3:

        st.metric(
            "TOP CATEGORY",
            best_category
        )

    st.divider()

    st.subheader(
        "Performance Summary"
    )

    st.write(
        f"Revenue generated: **₹{total_revenue:,.0f}**"
    )

    st.write(
        f"Orders processed: **{total_orders:,}**"
    )

    st.write(
        f"Units sold: **{total_units:,.0f}**"
    )

    st.write(
        f"Highest revenue product: **{best_product}**"
    )

    st.write(
        f"Highest revenue region: **{best_region}**"
    )

    st.write(
        f"Highest revenue category: **{best_category}**"
    )