import streamlit as st
import pandas as pd
import ast

# ============================================================
# PAGE CONFIGURATION & THEME
# ============================================================
st.set_page_config(
    page_title="Netflix Content Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom Netflix CSS (Brute-forcing Streamlit's native styles)
st.markdown(
    """
    <style>
    /* Soft off-white background to create a 'Card' effect for charts */
    .stApp {
        background-color: #F8F8F8;
    }
    
    /* Sleek, compact Banner Container */
    .netflix-title-container {
        background-color: #221F1F !important; /* Netflix Black */
        padding: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 25px !important;
        text-align: center !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Single-line Title Text */
    .netflix-title-container h1 {
        color: #E50914 !important; /* Netflix Red */
        font-family: 'Arial Black', 'Impact', sans-serif !important; 
        font-size: 2.8rem !important; 
        font-weight: 900 !important;
        margin: 0 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        line-height: 1.2 !important;
    }

    /* KPI Card Container Styling */
    [data-testid="stMetric"] {
        background-color: #F5F5F1 !important; /* Crisp Light Grey */
        border: 1px solid #D9D9D9 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        text-align: center !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* KPI Label (e.g., "Total Titles") */
    [data-testid="stMetricLabel"] {
        color: #221F1F !important; /* Netflix Black */
        font-weight: 900 !important;
        justify-content: center !important;
        font-size: 1.1rem !important;
    }
    
    /* KPI Value (e.g., "8,797") */
    [data-testid="stMetricValue"] {
        color: #E50914 !important; /* Netflix Red */
        font-weight: 900 !important;
    }

    /* Navigation Tabs Container (Snug padding, no hollow height) */
    [data-baseweb="tab"] {
        padding-top: 12px !important;
        padding-bottom: 12px !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
    }
    
    /* Force the actual text and emoji tags inside the tab to scale up */
    [data-baseweb="tab"] p, 
    [data-baseweb="tab"] span, 
    [data-baseweb="tab"] div {
        font-size: 1.08rem !important; /* Actually enlarges the text/emojis */
        font-weight: 600 !important;
        margin: 0 !important; /* Strips out invisible margins that push text down */
    }
    
    /* Space out the tabs slightly */
    [data-baseweb="tab-list"] {
        gap: 6px; 
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# BRAND PALETTE
# ============================================================
NETFLIX_COLORS = {
    'red': '#E50914',
    'dark_red': '#B20710',
    'black': '#221F1F',
    'dark_gray': '#404040',
    'mid_gray': '#808080',
    'light_gray': '#B3B3B3',
    'white': '#F5F5F1'
}

# ============================================================
# DATA INGESTION & STATE
# ============================================================
@st.cache_data
def load_data():
    # 1. Load the locked dataset
    df = pd.read_csv('Netflix_Project_Final_V3.csv')
    
    # 2. Deserialize list columns safely
    list_cols = ['director_list', 'cast_list', 'country_list', 'genre_list']
    for col in list_cols:
        df[col] = df[col].apply(ast.literal_eval)
        
    return df

df = load_data()

# ============================================================
# TOP ANCHOR: EXECUTIVE KPIs
# ============================================================
# Render the new custom Netflix title block
st.markdown(
    """
    <div class="netflix-title-container">
        <h1>NETFLIX CATALOG DASHBOARD</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Dynamic KPI Calculations
total_titles = len(df)
total_movies = len(df[df['type'] == 'Movie'])
total_tv_shows = len(df[df['type'] == 'TV Show'])

# Calculate unique countries (excluding 'Unknown Country' and 'nan')
unique_countries = set(
    country for sublist in df['country_list'] 
    for country in sublist 
    if country not in ['Unknown Country', 'nan', 'NaN', '']
)
countries_represented = len(unique_countries)

# Calculate unique genres
unique_genres = set(genre for sublist in df['genre_list'] for genre in sublist)
total_unique_genres = len(unique_genres)

# Aggregations
avg_movie_duration = df[df['type'] == 'Movie']['duration_value'].mean()
avg_tv_seasons = df[df['type'] == 'TV Show']['duration_value'].mean()
median_release_year = int(df['release_year'].median())
median_acquisition_year = int(df['year_added'].median())

# Render Metric Rows
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Titles", f"{total_titles:,}")
with col2:
    st.metric("Total Movies", f"{total_movies:,}")
with col3:
    st.metric("Total TV Shows", f"{total_tv_shows:,}")
with col4:
    st.metric("Countries Represented", f"{countries_represented}")
with col5:
    st.metric("Unique Genres", f"{total_unique_genres}")

st.write("") # Lightweight spacer

col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    st.metric("Avg. Movie Duration", f"{avg_movie_duration:.0f} Mins")
with col7:
    st.metric("Avg. TV Seasons", f"{avg_tv_seasons:.1f} Seasons")
with col8:
    st.metric("Median Release Year", f"{median_release_year}")
with col9:
    st.metric("Median Acquisition Year", f"{median_acquisition_year}")
with col10:
    st.empty() # Placeholder to maintain alignment

st.markdown("---")

# Navigation Tabs Placeholder Setup
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 Catalog Composition", 
    "📈 Acquisition Trends", 
    "🌍 Global Footprint", 
    "🎭 Genre Intelligence", 
    "👥 Creative Talent", 
    "🔬 Advanced Synthesis"
])

# [PHASE A COMPLETE]

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ============================================================
# TAB 1: CATALOG COMPOSITION
# ============================================================
with tab1:
    
    # ------------------------------------------------------------
    # CHART 1 — CONTENT TYPE SPLIT (MOVIES VS. TV SHOWS)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Content Type Split</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    type_counts = df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    color_map = {'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']}
    mapped_colors = type_counts['type'].map(color_map)

    # Build Figure
    fig1 = go.Figure(data=[go.Pie(
        labels=type_counts['type'],
        values=type_counts['count'],
        hole=0.5,
        domain=dict(x=[0.1, 0.9], y=[0.05, 0.95]),
        marker=dict(colors=mapped_colors, line=dict(color='#FFFFFF', width=2)),
        textinfo='percent+label',
        textposition='inside',
        insidetextfont=dict(size=14, color='white', family='Helvetica Neue, Arial, sans-serif'),
        hoverinfo='label+value+percent',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    )])

    fig1.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Catalog Composition: Movies vs. TV Shows</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5, xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        showlegend=True,
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.08, xanchor='center', x=0.5,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    # Render strict Plotly canvas
    st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** Movies represent approximately 69.7% (6,126 titles) of the catalog, while TV Shows account for 30.3% (2,671 titles) of total available inventory.
        * **Commercial Implication:** Although film licenses provide immediate catalog volume and promotional splash, TV Shows drive recurring platform engagement, lower subscriber churn, and higher lifetime customer value (LTV). An executive recommendation is to selectively expand high-retention episodic series while moderating passive film backfill.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 2 — AUDIENCE MATURITY & RATING BREAKDOWN
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Audience Maturity & Rating Breakdown</h3>", unsafe_allow_html=True)
    
    # Local Data Prep (Preserving global 1-row-per-title state)
    df_tree = df[df['maturity_level'] > 0].copy()
    tree_counts = df_tree.groupby(['maturity_level', 'rating']).size().reset_index(name='count')
    
    netflix_maturity_scale = [
        [0.0, '#FFC5C6'],
        [0.25, '#FF8A8C'],
        [0.5, '#F94A4D'],
        [0.75, NETFLIX_COLORS['red']],
        [1.0, NETFLIX_COLORS['dark_red']]
    ]

    # Build Figure
    fig2 = px.treemap(
        tree_counts,
        path=[px.Constant("Netflix Catalog"), 'maturity_level', 'rating'],
        values='count',
        color='maturity_level',
        color_continuous_scale=netflix_maturity_scale,
        range_color=[1, 5]
    )

    fig2.update_layout(
        height=500, # Large Chart (Treemap)
        title=dict(
            text='<b>Audience Maturity & Rating Breakdown</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5, xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=60, b=40, l=40, r=40),
        coloraxis_colorbar=dict(
            title=dict(text="<b>Maturity Level</b>", font=dict(color=NETFLIX_COLORS['black'])),
            orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5, thickness=15, len=0.5,
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['1 (Kids)', '2 (Older Kids)', '3 (Teens)', '4 (Young Adults)', '5 (Adults)']
        )
    )
    
    fig2.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=2)),
        hovertemplate="<b>%{label}</b><br>Maturity Level: %{color}<br>Total Titles: %{value}<extra></extra>"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** Netflix has a massive footprint of mature content. Maturity Level 5 (driven by `TV-MA`,`NC-17` for Movies also has 3 Titles but it is miniscule compared to `TV-MA`hence not visible in Tree Map ) and Level 4 (driven by `TV-14` and `R`) consume the vast majority of the catalog space.
	* **Commercial Implication:** The visual confirms Netflix is heavily indexed toward adult and young adult subscribers, prioritizing complex, mature storytelling over family-syndication content (Levels 1 and 2).
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 3 — CONTENT DURATION PROFILES (MOVIES VS. TV SHOWS)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Content Duration Profiles</h3>", unsafe_allow_html=True)
    
    # Local Data Prep
    movie_order = ['<60 min', '60-90 min', '90-120 min', '120-150 min', '150+ min']
    tv_order = ['1 season', '2-3 seasons', '4-6 seasons', '7+ seasons']

    movies_df = df[df['type'] == 'Movie']['duration_bucket'].value_counts().reindex(movie_order).fillna(0).reset_index()
    movies_df.columns = ['duration_bucket', 'count']

    tv_shows_df = df[df['type'] == 'TV Show']['duration_bucket'].value_counts().reindex(tv_order).fillna(0).reset_index()
    tv_shows_df.columns = ['duration_bucket', 'count']

    # Build Figure
    fig3 = make_subplots(
        rows=1, cols=2, 
        subplot_titles=('<b>Movies (Runtimes)</b>', '<b>TV Shows (Seasons)</b>'),
        horizontal_spacing=0.1
    )

    fig3.add_trace(go.Bar(
        x=movies_df['duration_bucket'], y=movies_df['count'], name='Movie',
        marker_color=NETFLIX_COLORS['red'], hovertemplate="<b>%{x}</b><br>Volume: %{y:,}<extra></extra>"
    ), row=1, col=1)

    fig3.add_trace(go.Bar(
        x=tv_shows_df['duration_bucket'], y=tv_shows_df['count'], name='TV Show',
        marker_color=NETFLIX_COLORS['black'], hovertemplate="<b>%{x}</b><br>Volume: %{y:,}<extra></extra>"
    ), row=1, col=2)

    fig3.update_layout(
        height=500, # Large Chart (Subplots)
        title=dict(
            text='<b>Content Duration Profiles</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5, xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        showlegend=True,
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=80, b=60, l=40, r=40)
    )

    fig3.update_yaxes(title_text="Total Titles", showgrid=True, gridcolor=NETFLIX_COLORS['light_gray'], zeroline=True, zerolinecolor=NETFLIX_COLORS['black'], row=1, col=1)
    fig3.update_yaxes(showgrid=True, gridcolor=NETFLIX_COLORS['light_gray'], zeroline=True, zerolinecolor=NETFLIX_COLORS['black'], row=1, col=2)

    for annotation in fig3['layout']['annotations']:
        annotation['font'] = dict(size=14, color=NETFLIX_COLORS['dark_gray'])

    fig3.update_traces(width=0.4, row=1, col=1)
    fig3.update_traces(width=0.32, row=1, col=2)

    st.plotly_chart(fig3, use_container_width=True)
    
    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The 90–120 minute runtime heavily dominates the film catalog. Meanwhile, the TV show catalog is massively skewed toward 1-Season series.
        * **Commercial Implication:** The extreme drop-off after 1-Season TV shows highlights the industry’s high cancellation velocity—Netflix invests heavily in rapid ideation but cuts underperforming series early. For films, standard theatrical runtimes (1.5 to 2 hours) remain the core anchor over shorter features.
        """)

import plotly.express as px
import numpy as np

# ============================================================
# TAB 2: ACQUISITION TRENDS (PHASE C)
# ============================================================
with tab2:
    
    # ------------------------------------------------------------
    # CHART 4 — HISTORICAL PRODUCTION VELOCITY (CONTENT BY RELEASE YEAR)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Historical Production Velocity</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    release_counts = df.groupby(['release_year', 'type']).size().reset_index(name='count')
    
    # Build Figure
    fig4 = px.line(
        release_counts,
        x='release_year',
        y='count',
        color='type',
        markers=True,
        color_discrete_map={'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']},
        labels={'release_year': 'Original Release Year', 'count': 'Total Titles', 'type': 'Content Type'}
    )
    
    fig4.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Historical Production Velocity (Content by Release Year)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            gridwidth=1, 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            gridwidth=1, 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=80, l=40, r=40)
    )
    
    fig4.update_traces(hovertemplate="<b>%{x}</b><br>Volume: %{y:,}<extra></extra>")
    fig4.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig4, use_container_width=True)
    
    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The distribution is severely right-skewed. An overwhelming majority of the content available on Netflix was produced post-2010, forming an exponential spike, while classic titles (pre-1990) represent a minuscule fraction of the catalog.
        * **Commercial Implication:** Netflix is not a historical archive. Its consumer value proposition is firmly anchored in contemporary, modern productions. Competitors (like HBO Max/Max or Criterion) may own the "classic" lane, but Netflix competes on modern volume and recency.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 5 — PLATFORM INGESTION TRAJECTORY (TITLES ADDED BY YEAR)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Platform Ingestion Trajectory</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    ingestion_counts = df.groupby(['year_added', 'type']).size().reset_index(name='count')
    
    # Build Figure
    fig5 = px.bar(
        ingestion_counts,
        x='year_added',
        y='count',
        color='type',
        barmode='group',
        color_discrete_map={'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']},
        labels={'year_added': 'Year Added to Netflix', 'count': 'Total Titles Ingested', 'type': 'Content Type'}
    )
    
    fig5.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Platform Ingestion Trajectory (Titles Added by Year)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            showgrid=False,
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black'],
            tickmode='linear'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            gridwidth=1, 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    fig5.update_traces(hovertemplate="<b>%{x}</b><br>Ingested Volume: %{y:,}<extra></extra>")
    
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** Annual additions were modest through 2015, followed by an aggressive volume expansion from 2016 to 2019 (peaking at over 2,000 titles added in 2019 alone). Movie acquisitions drove the bulk of this volume surge, while TV Show additions expanded at a steadier, controlled rate.
        * **Commercial Implication:** The 2016–2019 surge reflects Netflix's global footprint expansion, where bulk licensing of films was used to quickly establish regional catalog depth. The post-2019 plateau and slight dip signal a shift from unconstrained volume backfill toward curated, higher-margin original productions.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 6 — LIBRARY FRESHNESS MATRIX (RELEASE VS. INGESTION)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Library Freshness Matrix</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    heat_counts = df.groupby(['release_year', 'year_added']).size().reset_index(name='count')
    
    netflix_heatmap_scale = [
        [0.0, '#221F1F'],                     
        [0.5, '#B20710'],                     
        [1.0, '#E50914']                      
    ]
    
    # Build Figure
    fig6 = px.scatter(
        heat_counts,
        x='release_year',
        y='year_added',
        size='count',
        color='count',
        color_continuous_scale=netflix_heatmap_scale,
        labels={'release_year': 'Original Release Year', 'year_added': 'Year Added to Netflix', 'count': 'Total Titles'}
    )
    
    fig6.update_layout(
        height=500, # Large Chart / Matrix
        title=dict(
            text='<b>Library Freshness Matrix: Movies & TV Shows (Release vs. Ingestion)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            showgrid=False,                              
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False, 
            zeroline=False,
            title_standoff=20
        ),
        margin=dict(t=60, b=100, l=80, r=40),
        coloraxis_colorbar=dict(
            title=dict(text="<b>Total Titles</b>", font=dict(color=NETFLIX_COLORS['black'])),
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='center',
            x=0.5,
            thickness=15,
            len=0.5
        )
    )
    
    fig6.update_traces(
        marker=dict(line=dict(width=0)),
        hovertemplate="<b>Release Year:</b> %{x}<br><b>Year Added:</b> %{y}<br><b>Volume:</b> %{marker.size}<extra></extra>"
    )
    
    st.plotly_chart(fig6, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The matrix reveals a massive, glowing cluster of large bubbles along the "diagonal" (where `year_added` equals `release_year`), meaning the vast majority of titles arrive on Netflix the exact same year they are produced. 
        * **Commercial Implication:** The dense diagonal validates that Netflix has successfully transitioned from a secondary syndication window (hosting old movies) to a primary premiere destination. The modern value proposition relies heavily on recency and exclusivity rather than a deep archival back catalog.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 7 — CUMULATIVE ACQUISITION LAG (FRESHNESS BY PERCENTAGE)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Cumulative Acquisition Lag</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    if 'acquisition_lag' not in df.columns:
        df['acquisition_lag'] = df['year_added'] - df['release_year']
        
    lag_df = df[df['acquisition_lag'] >= 0].dropna(subset=['acquisition_lag'])
    
    # Build Figure
    fig7 = px.ecdf(
        lag_df,
        x='acquisition_lag',
        color='type',
        color_discrete_map={'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']},
        labels={'acquisition_lag': 'Years Between Release and Netflix Debut', 'type': 'Content Type'}
    )
    
    fig7.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Cumulative Acquisition Lag (Freshness by Percentage)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            title_text='Years of Lag (Time-to-Platform)',
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        yaxis=dict(
            title_text='Cumulative Percentage of Catalog',
            title_standoff=20,
            tickformat='.0%',
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    fig7.update_traces(
        line=dict(width=3),
        hovertemplate="<b>Lag Time:</b> %{x} years<br><b>Cumulative Catalog:</b> %{y:.1%}<extra></extra>"
    )
    
    st.plotly_chart(fig7, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The TV Show trajectory is remarkably steep, breaching the 80% cumulative mark at just 3 years of lag. Movies follow a much slower curve, taking 8 years to reach that exact same 80% threshold. 
        * **Commercial Implication:** This mathematically proves a bifurcated licensing strategy. TV Shows are treated almost strictly as immediate, contemporary assets (driven by Originals and day-and-date broadcast licensing). Movies serve a dual purpose: acting as fresh premiere attractions while simultaneously relying on a massive "long tail" of older syndicated films to artificially pad the catalog's depth.
        """)

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================
# TAB 3: GLOBAL FOOTPRINT
# ============================================================
with tab3:
    
    # ------------------------------------------------------------
    # CHART 8 — TOP 15 PRODUCTION COUNTRIES
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Top 15 Production Countries (Volume & Format Bias)</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    country_df = df.explode('country_list').dropna(subset=['country_list'])
    country_df = country_df[~country_df['country_list'].astype(str).str.lower().str.contains('unknown')]
    country_df = country_df[country_df['country_list'].astype(str).str.strip() != '']

    country_counts = country_df.groupby(['country_list', 'type']).size().reset_index(name='count')
    top_15_countries = country_df['country_list'].value_counts().head(15).index
    top_15_df = country_counts[country_counts['country_list'].isin(top_15_countries)]

    # Build Figure
    fig8 = px.bar(
        top_15_df,
        x='count',
        y='country_list',                                
        color='type',
        orientation='h',
        color_discrete_map={'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']},
        labels={'count': 'Total Titles Produced', 'country_list': 'Production Country', 'type': 'Content Type'},
        category_orders={'country_list': top_15_countries[::1]}  
    )
    
    fig8.update_layout(
        height=500, # Medium Chart                                     
        title=dict(
            text='<b>Top 15 Production Countries (Volume & Format Bias)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        yaxis=dict(
            showgrid=False,
            title_text=''
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=40, l=120, r=40)
    )

    fig8.update_traces(hovertemplate="<b>%{y}</b><br>Volume: %{x}<extra></extra>")
    
    st.plotly_chart(fig8, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The United States completely dominates total volume, holding a massive lead over all other nations combined. However, looking at the format ratios reveals deep regional biases: India indexes almost exclusively in feature films (driven by Bollywood acquisition), while countries like South Korea and Japan exhibit a much higher concentration of TV Shows (driven by K-Dramas and Anime).
        * **Commercial Implication:** Netflix does not apply a "one-size-fits-all" global acquisition strategy. It highly localizes its catalog to match regional industry strengths—buying bulk cinema in India, while investing heavily in episodic series in East Asia.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 9 — GLOBAL CONTENT PRODUCTION FOOTPRINT (CHOROPLETH)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Global Content Production Footprint</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    country_df_geo = df.explode('country_list').dropna(subset=['country_list'])
    country_df_geo = country_df_geo[country_df_geo['country_list'].str.strip() != ''] 
    
    country_counts_geo = country_df_geo.groupby('country_list').size().reset_index(name='count')
    country_counts_geo['log_count'] = np.log10(country_counts_geo['count'])

    netflix_map_scale = [
        [0.0, '#F5F5F1'],                     
        [0.25, '#FFC5C6'],                    
        [0.5, '#F94A4D'],                     
        [0.75, NETFLIX_COLORS['red']],        
        [1.0, NETFLIX_COLORS['black']]        
    ]
    
    # Build Figure
    fig9 = px.choropleth(
        country_counts_geo,
        locations='country_list',
        locationmode='country names',
        color='log_count',
        color_continuous_scale=netflix_map_scale,
        hover_name='country_list',
        custom_data=['count']                            
    )

    fig9.update_layout(
        height=750, # Large Chart / Map
        title=dict(
            text='<b>Global Content Production Footprint</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        geo=dict(
            showframe=False,                             
            showcoastlines=True,
            coastlinecolor=NETFLIX_COLORS['light_gray'],
            projection_type='natural earth',             
            bgcolor='#FFFFFF',
            showocean=False,
            showlakes=False
        ),
        margin=dict(t=60, b=80, l=40, r=40),
        coloraxis_colorbar=dict(
            title=dict(text="<b>Total Titles (Log Scale)</b>", font=dict(color=NETFLIX_COLORS['black'])),
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            thickness=15,
            len=0.5,
            tickvals=[0, 1, 2, 3, 3.5],                  
            ticktext=['1', '10', '100', '1,000', '3,100+'] 
        )
    )

    fig9.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Total Titles: %{customdata[0]:,}<extra></extra>",
        marker_line_width=0.5,                           
        marker_line_color=NETFLIX_COLORS['light_gray']
    )

    st.plotly_chart(fig9, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** While the United States remains the undisputed center of production, the map reveals distinct, highly active regional clusters: Europe (led by the UK, France, and Spain) and Asia (led by India, Japan, and South Korea). Significant portions of Africa, the Middle East, and Eastern Europe remain "cold spots" with negligible production volume.
        * **Commercial Implication:** Netflix has successfully established major international footholds, but its production strategy is highly concentrated in a few key "super-regions" rather than being evenly distributed globally. This targeted localization strategy focuses on high-subscriber-growth markets with established local film industries.
        """)

# ============================================================
# TAB 4: GENRE INTELLIGENCE
# ============================================================
with tab4:
    
    # ------------------------------------------------------------
    # CHART 10 — THE GENRE LANDSCAPE (PORTFOLIO TREEMAP)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>The Genre Landscape</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    genre_df = df.explode('genre_list').dropna(subset=['genre_list'])
    genre_df = genre_df[genre_df['genre_list'].str.strip() != '']
    genre_counts = genre_df.groupby('genre_list').size().reset_index(name='count')

    netflix_treemap_scale = [
        [0.0, '#221F1F'],                     
        [0.5, '#B20710'],                     
        [1.0, '#E50914']                      
    ]

    # Build Figure
    fig10 = px.treemap(
        genre_counts,
        path=[px.Constant("Netflix Catalog"), 'genre_list'],  
        values='count',
        color='count',
        color_continuous_scale=netflix_treemap_scale,
        custom_data=['count']
    )

    fig10.update_layout(
        height=750, # Large Chart / Treemap
        title=dict(
            text='<b>The Genre Landscape (Portfolio Allocation)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=60, b=100, l=40, r=40), 
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        coloraxis_colorbar=dict(
            title=dict(text="<b>Total Titles</b>", font=dict(color=NETFLIX_COLORS['black'])),
            orientation="h",       
            thickness=15,
            len=0.6,
            yanchor="top",
            y=-0.1,                
            xanchor="center",
            x=0.5
        )
    )
    
    fig10.update_traces(
        hovertemplate="<b>%{label}</b><br>Total Titles: %{value:,}<extra></extra>",
        texttemplate="<b>%{label}</b><br>%{value:,}",
        textfont=dict(size=14),                          
        marker_line_width=2,                             
        marker_line_color='#FFFFFF'                      
    )
    
    st.plotly_chart(fig10, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The visual real estate is overwhelmingly dominated by three massive blocks: *International Movies*, *Dramas*, and *Comedies*. These foundational pillars form the bedrock of the catalog, physically pushing niche categories (like Sci-Fi, Horror, or Anime) to the outer margins.
        * **Commercial Implication:** Netflix's core acquisition strategy is highly risk-averse regarding volume. While they aggressively market expensive niche hits (like *Stranger Things* for Sci-Fi), the actual vault is overwhelmingly stocked with universal, highly translatable themes and localized global cinema to ensure there is a baseline offering for every global demographic.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 11 — GENRE DOMINANCE BY FORMAT (BUTTERFLY CHART)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Genre Dominance by Format</h3>", unsafe_allow_html=True)
    
    # Define Root Genre mapping locally
    def get_root_genre(g):
        g = g.strip()
        if 'Stand-Up' in g: return 'Stand-Up Comedy'
        if 'Comed' in g: return 'Comedy'
        if 'Action' in g: return 'Action & Adventure'
        if 'Docum' in g or 'Docuseries' in g: return 'Documentary'
        if 'Sci-Fi' in g or 'Fantasy' in g: return 'Sci-Fi & Fantasy'
        if 'Crime' in g: return 'Crime'
        if 'Kid' in g or 'Children' in g: return 'Kids & Family'
        if 'Horror' in g: return 'Horror'
        if 'Thriller' in g: return 'Thriller'
        if 'Roman' in g: return 'Romance'
        if 'Drama' in g: return 'Drama'
        if 'Anime' in g: return 'Anime'
        if 'Music' in g: return 'Music'
        if 'Reality' in g: return 'Reality TV'
        return g.replace(' Movies', '').replace(' TV Shows', '').replace(' Series', '').replace('TV ', '').strip()

    # Prepare Data
    genre_df_b = df.explode('genre_list').dropna(subset=['genre_list'])
    genre_df_b = genre_df_b[genre_df_b['genre_list'].str.strip() != '']
    genre_df_b['root_genre'] = genre_df_b['genre_list'].apply(get_root_genre)

    counts_df = genre_df_b.groupby(['root_genre', 'type']).size().reset_index(name='count')
    top_15_genres = genre_df_b['root_genre'].value_counts().head(15).index
    counts_df = counts_df[counts_df['root_genre'].isin(top_15_genres)]

    total_per_genre = counts_df.groupby('root_genre')['count'].transform('sum')
    counts_df['percentage'] = (counts_df['count'] / total_per_genre)
    counts_df['diverging_pct'] = counts_df.apply(
        lambda x: -x['percentage'] if x['type'] == 'Movie' else x['percentage'], axis=1
    )

    sort_df = counts_df.pivot(index='root_genre', columns='type', values='percentage').fillna(0)
    if 'TV Show' in sort_df.columns:
        sort_order = sort_df.sort_values('TV Show', ascending=True).index
    else:
        sort_order = sort_df.index

    # Build Figure
    fig11 = px.bar(
        counts_df,
        x='diverging_pct',
        y='root_genre',
        color='type',
        orientation='h',
        color_discrete_map={'Movie': NETFLIX_COLORS['red'], 'TV Show': NETFLIX_COLORS['black']},
        category_orders={'root_genre': sort_order},
        custom_data=['percentage']  
    )

    fig11.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Genre Dominance by Format (Movie vs. TV Focus)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        barmode='relative',
        xaxis=dict(
            title_text='← Movies (%)            Format Distribution            TV Shows (%) →',
            showgrid=True, 
            gridcolor=NETFLIX_COLORS['light_gray'], 
            zeroline=True, 
            zerolinecolor=NETFLIX_COLORS['black'],
            zerolinewidth=2,
            tickvals=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1],
            ticktext=['100%', '75%', '50%', '25%', '0%', '25%', '50%', '75%', '100%']
        ),
        yaxis=dict(
            title_text='',
            showgrid=False
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        margin=dict(t=60, b=40, l=140, r=40)
    )

    fig11.update_traces(
        hovertemplate="<b>%{y}</b><br>Format: %{data.name}<br>Share: %{customdata[0]:.1%}<extra></extra>"
    )

    st.plotly_chart(fig11, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The normalized data reveals stark format biases that were previously hidden. For instance, **Stand-Up Comedy** and **Documentaries** are overwhelmingly biased toward feature-length formats (pulling heavily to the left). Conversely, **Crime**, **Kids' Programming**, and **Reality/Docuseries** dominate the episodic TV side (pulling heavily to the right).
        * **Commercial Implication:** Netflix understands that certain themes are better suited for specific retention strategies. Stand-up specials act as quick, impactful subscriber acquisition events (Movies), while Crime and Kids' content are designed as "bingeable," multi-hour retention engines (TV Shows).
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 12 — REGIONAL GENRE SPECIALIZATION (HEATMAP)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Regional Genre Specialization</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    df_geo = df.explode('country_list').dropna(subset=['country_list'])
    df_geo = df_geo[df_geo['country_list'].str.strip() != '']
    df_matrix = df_geo.explode('genre_list').dropna(subset=['genre_list'])
    df_matrix = df_matrix[df_matrix['genre_list'].str.strip() != '']

    df_matrix['root_genre'] = df_matrix['genre_list'].apply(get_root_genre)
    df_matrix = df_matrix[df_matrix['root_genre'] != 'International']

    top_15_countries_hm = df_matrix['country_list'].value_counts().head(15).index
    top_22_genres_hm = df_matrix['root_genre'].value_counts().head(22).index

    df_matrix = df_matrix[
        (df_matrix['country_list'].isin(top_15_countries_hm)) & 
        (df_matrix['root_genre'].isin(top_22_genres_hm))
    ]

    crosstab_vol = pd.crosstab(df_matrix['country_list'], df_matrix['root_genre'])
    crosstab_vol = crosstab_vol.loc[top_15_countries_hm, top_22_genres_hm]
    crosstab_pct = crosstab_vol.div(crosstab_vol.sum(axis=1), axis=0)

    heatmap_scale = [
        [0.0, '#F5F5F1'],                     
        [0.15, '#FFC5C6'],                    
        [0.5, NETFLIX_COLORS['red']],         
        [1.0, NETFLIX_COLORS['dark_red']]     
    ]
    
    # Build Figure
    fig12 = px.imshow(
        crosstab_pct,
        labels=dict(x="Root Genre", y="Production Country", color="Concentration"),
        x=crosstab_pct.columns,
        y=crosstab_pct.index,
        color_continuous_scale=heatmap_scale,
        aspect="auto"  
    )

    fig12.update_layout(
        height=750, # Large Chart / Heatmap
        title=dict(
            text='<b>Regional Genre Specialization (Percentage of Output)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            tickangle=-45,                       
            side='bottom',
            showgrid=False
        ),
        yaxis=dict(
            showgrid=False
        ),
        margin=dict(t=80, b=120, l=120, r=40),
        coloraxis_colorbar=dict(
            title="<b>Share of<br>Country's Output</b>",
            tickformat='.0%',
            thickness=15
        )
    )

    fig12.update_traces(
        customdata=crosstab_vol,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Genre: %{x}<br>"
            "Concentration: <b>%{z:.1%}</b><br>"
            "Titles: %{customdata:,}<extra></extra>"
        )
    )

    st.plotly_chart(fig12, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The map will reveal intense, isolated clusters of deep red rather than an even spread. For example, Japan's row will show a massive concentration strictly in Anime. India will show an overwhelming cluster in Drama and Comedy (Bollywood). The UK will glow strongly in Documentaries and Crime. 
        * **Commercial Implication:** Netflix operates a decentralized, hyper-local supply chain. Instead of forcing American genres onto international hubs, it utilizes those hubs to mass-produce what they are already culturally optimized for, and then exports that specialized content to the rest of the global subscriber base.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 13 — CATALOG STRUCTURAL HIERARCHY (SUNBURST)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Catalog Structural Hierarchy</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    sunburst_df = df[df['maturity_level'] > 0].copy()
    sunburst_df = sunburst_df.dropna(subset=['maturity_level', 'genre_list'])

    maturity_mapping = {
        1: 'Level 1 (Kids)',
        2: 'Level 2 (Older Kids)',
        3: 'Level 3 (Teens)',
        4: 'Level 4 (Young Adults)',
        5: 'Level 5 (Adults)'
    }
    sunburst_df['maturity_label'] = sunburst_df['maturity_level'].map(maturity_mapping)

    sunburst_df = sunburst_df.explode('genre_list')
    sunburst_df = sunburst_df[sunburst_df['genre_list'].str.strip() != '']
    sunburst_df['root_genre'] = sunburst_df['genre_list'].apply(get_root_genre)

    branch_counts = sunburst_df.groupby(['type', 'maturity_label', 'maturity_level', 'root_genre']).size().reset_index(name='count')
    branch_counts = branch_counts.sort_values(['type', 'maturity_label', 'count'], ascending=[True, True, False])
    top_branches = branch_counts.groupby(['type', 'maturity_label']).head(5)

    maturity_scale = [
        [0.0, '#F5F5F1'],                     
        [0.25, '#FFC5C6'],                    
        [0.5, '#E50914'],                     
        [0.75, '#B20710'],                    
        [1.0, '#221F1F']                      
    ]

    # Build Figure
    fig13 = px.sunburst(
        top_branches,
        path=['type', 'maturity_label', 'root_genre'],
        values='count',
        color='maturity_level',               
        color_continuous_scale=maturity_scale,
        range_color=[1, 5],                   
        custom_data=['count', 'maturity_level']
    )

    fig13.update_layout(
        height=750, # Large Chart / Sunburst
        title=dict(
            text='<b>Catalog Structural Hierarchy (Format → Maturity → Genre)</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=60, b=40, l=40, r=40),
        coloraxis_colorbar=dict(
            title="<b>Maturity Level</b>",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['1 (Kids)', '2', '3', '4', '5 (Adults)'],
            thickness=15,
            len=0.5
        )
    )

    fig13.update_traces(
        textinfo='label+percent parent',
        insidetextorientation='radial',
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Titles: %{customdata[0]:,}<br>"
            "Maturity Level: %{customdata[1]}<br>"
            "Share of Parent: %{percentParent:.1%}<extra></extra>"
        ),
        marker_line_width=1.5,
        marker_line_color='#FFFFFF'
    )

    st.plotly_chart(fig13, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The chart visually proves that Netflix is fundamentally an **Adult/Mature** platform (evidenced by the deep red weighted average of the center rings). Tracing the hierarchy reveals strict genre-demographic boundaries: Adult TV is overwhelmingly driven by Drama and Crime, while Kids TV relies almost entirely on Animation and Family content.
        * **Commercial Implication:** While Netflix markets itself as a family household necessity, its actual content acquisition pipeline is hyper-focused on mature audiences. It utilizes a massive, mature portfolio to drive engagement and retention, while maintaining a smaller, highly concentrated family portfolio for baseline household utility.
        """)

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================
# TAB 5: CREATIVE TALENT
# ============================================================
with tab5:
    
    # ------------------------------------------------------------
    # CHART 14 — TOP 15 MOST FREQUENT DIRECTORS (LOLLIPOP)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Top 15 Most Frequent Directors</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    dir_df = df.explode('director_list').dropna(subset=['director_list'])
    dir_df['director_list'] = dir_df['director_list'].str.strip()
    
    dir_df = dir_df[
        (dir_df['director_list'] != '') & 
        (dir_df['director_list'] != 'Uncredited Director')
    ]
    
    top_dirs = dir_df.groupby('director_list').size().reset_index(name='count')
    top_dirs = top_dirs.sort_values('count', ascending=False).head(15)
    top_dirs = top_dirs.sort_values('count', ascending=True)

    # Build Figure
    fig14 = go.Figure()

    for i, row in top_dirs.iterrows():
        fig14.add_shape(
            type="line",
            x0=0,
            x1=row['count'],
            y0=row['director_list'],
            y1=row['director_list'],
            line=dict(color='#E5E5E5', width=3), 
            layer='below'
        )

    fig14.add_trace(
        go.Scatter(
            x=top_dirs['count'],
            y=top_dirs['director_list'],
            mode='markers+text',
            marker=dict(color=NETFLIX_COLORS['red'], size=14),
            text=top_dirs['count'],                       
            textposition='middle right',
            textfont=dict(size=12, color=NETFLIX_COLORS['black']),
            name='Titles',
            hovertemplate="<b>%{y}</b><br>Titles Directed: %{x}<extra></extra>"
        )
    )

    fig14.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Top 15 Most Frequent Directors</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=60, b=40, l=150, r=40), 
        xaxis=dict(
            title='<b>Total Titles</b>',
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray'],
            zeroline=True,
            zerolinecolor=NETFLIX_COLORS['black'],
            zerolinewidth=2
        ),
        yaxis=dict(
            title='',
            showgrid=False
        ),
        showlegend=False
    )

    st.plotly_chart(fig14, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** A common stakeholder assumption is that a global platform's top directors would be marquee Hollywood auteurs—names like Christopher Nolan, Steven Spielberg, or Quentin Tarantino. However, the data completely shatters this expectation. The highest-volume slots are overwhelmingly dominated by hyper-specialized regional powerhouses. 
        * **Commercial Implication:** Netflix achieves raw volume not by paying astronomical fees for massive Hollywood directors, but by partnering with high-output regional specialists. For example, Rajiv Chilaka dominates the list through the mass production of Indian children's animation (*Chhota Bheem*), while Raúl Campos and Jan Suter generate massive volume through Latin American stand-up comedy specials.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 15 — TOP 15 MOST PROLIFIC CAST MEMBERS (LOLLIPOP)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Top 15 Most Prolific Cast Members</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    cast_df = df.explode('cast_list').dropna(subset=['cast_list'])
    cast_df['cast_list'] = cast_df['cast_list'].str.strip()
    
    cast_df = cast_df[
        (cast_df['cast_list'] != '') & 
        (cast_df['cast_list'] != 'Uncredited Cast')
    ]
    
    top_cast = cast_df.groupby('cast_list').size().reset_index(name='count')
    top_cast = top_cast.sort_values('count', ascending=False).head(15)
    top_cast = top_cast.sort_values('count', ascending=True)

    # Build Figure
    fig15 = go.Figure()

    for i, row in top_cast.iterrows():
        fig15.add_shape(
            type="line",
            x0=0,
            x1=row['count'],
            y0=row['cast_list'],
            y1=row['cast_list'],
            line=dict(color='#E5E5E5', width=3), 
            layer='below'
        )

    fig15.add_trace(
        go.Scatter(
            x=top_cast['count'],
            y=top_cast['cast_list'],
            mode='markers+text',
            marker=dict(color=NETFLIX_COLORS['red'], size=14),
            text=top_cast['count'],                       
            textposition='middle right',
            textfont=dict(size=12, color=NETFLIX_COLORS['black']),
            name='Titles',
            hovertemplate="<b>%{y}</b><br>Titles Appeared In: %{x}<extra></extra>"
        )
    )

    fig15.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Top 15 Most Prolific Cast Members</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=60, b=40, l=150, r=40), 
        xaxis=dict(
            title='<b>Total Titles</b>',
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray'],
            zeroline=True,
            zerolinecolor=NETFLIX_COLORS['black'],
            zerolinewidth=2
        ),
        yaxis=dict(
            title='',
            showgrid=False
        ),
        showlegend=False
    )

    st.plotly_chart(fig15, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The data decisively proves that the highest-volume actors are not American A-listers. The top spots are overwhelmingly dominated by Indian cinema icons (like Anupam Kher, Shah Rukh Khan, and Om Puri) alongside highly prolific Japanese anime voice actors (like Takahiro Sakurai).
        * **Commercial Implication:** This exposes Netflix's massive strategic reliance on the Indian film industry (Bollywood/Tollywood) to drive catalog depth. Indian cinema produces feature films at a vastly higher volume than Hollywood, and Netflix licenses these massive back catalogs to maintain high retention in one of their most critical growth markets.
        """)

# ============================================================
# TAB 6: ADVANCED SYNTHESIS
# ============================================================
with tab6:
    
    # ------------------------------------------------------------
    # CHART 16 — CATALOG VINTAGE & SHELF-LIFE (HISTOGRAM)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Catalog Vintage & Shelf-Life</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    df['content_age'] = 2021 - df['release_year']
    vintage_df = df[df['content_age'] >= 0].copy()
    
    median_age_movie = vintage_df[vintage_df['type'] == 'Movie']['content_age'].median()
    median_age_tv = vintage_df[vintage_df['type'] == 'TV Show']['content_age'].median()

    # Build Figure
    fig16 = px.histogram(
        vintage_df,
        x='content_age',
        color='type',
        color_discrete_map={
            'Movie': NETFLIX_COLORS['red'], 
            'TV Show': NETFLIX_COLORS['black']
        },
        barmode='group',
        nbins=45
    )

    fig16.add_vline(
        x=median_age_movie, 
        line_width=2.5, 
        line_dash="dash", 
        line_color=NETFLIX_COLORS['red'],
        annotation_text=f"Movie Median: {int(median_age_movie)} yrs", 
        annotation_position="top right",
        annotation_font=dict(color=NETFLIX_COLORS['red'], size=12, weight='bold'),
        annotation_yshift=0
    )

    fig16.add_vline(
        x=median_age_tv, 
        line_width=2.5, 
        line_dash="dash", 
        line_color=NETFLIX_COLORS['black'],
        annotation_text=f"TV Median: {int(median_age_tv)} yrs", 
        annotation_position="top right",
        annotation_font=dict(color=NETFLIX_COLORS['black'], size=12, weight='bold'),
        annotation_yshift=-35,
        annotation_xshift=20
    )

    max_age = vintage_df['content_age'].max()

    fig16.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Catalog Vintage & Shelf-Life Distribution</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=70, b=50, l=60, r=40),
        bargap=0.15,
        bargroupgap=0.05,
        xaxis=dict(
            title='<b>Content Age / Shelf-Life (Years Since Release)</b>',
            range=[-1.5, max_age + 2],         
            dtick=5,                            
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray'],
            zeroline=True,
            zerolinecolor=NETFLIX_COLORS['black'],
            zerolinewidth=1.5
        ),
        yaxis=dict(
            title='<b>Total Titles</b>',
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray']
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        )
    )

    fig16.update_traces(
        hovertemplate="<b>%{data.name}</b><br>Content Age: %{x} Years<br>Titles: %{y}<extra></extra>"
    )

    st.plotly_chart(fig16, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The histogram will reveal a massive, heavily skewed right-tail distribution (meaning the bulk of the data sits close to 0-5 years of age). The median age of the catalog is shockingly young proving that almost the entire library was produced within a very recent window. Furthermore, TV Shows have an even younger median age than Movies.
        * **Commercial Implication:** Netflix operates almost entirely on "freshness" rather than nostalgia. Unlike Disney+ (which relies on a century-old vault) or HBO, Netflix trains its algorithm and user base to constantly consume the "new." Content older than 10 years forms an almost negligible part of their retention strategy.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 17 — DURATION BUCKET VS. MATURITY LEVEL HEATMAP
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Duration Bucket vs. Maturity Level</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    heatmap_scale = [
        [0.0, '#F5F5F1'],                     
        [0.15, '#FFC5C6'],                    
        [0.5, NETFLIX_COLORS['red']],         
        [1.0, NETFLIX_COLORS['dark_red']]     
    ]

    pivot_dm = pd.crosstab(
        df.loc[
            (df['maturity_level'] != 0) & (df['duration_bucket'] != 0),
            'duration_bucket'
        ],
        df.loc[
            (df['maturity_level'] != 0) & (df['duration_bucket'] != 0),
            'maturity_level'
        ]
    )

    def sort_buckets(bucket_name):
        name = str(bucket_name).lower()
        if 'min' in name:
            if '<' in name: return 1
            if '60' in name: return 2
            if '90' in name: return 3
            if '>' in name: return 4
            return 5
        if 'season' in name:
            if '1' in name: return 11
            if '2' in name: return 12
            if '3' in name: return 13
            if '4' in name or '+' in name: return 14
            return 15
        return 99

    sorted_index = sorted(pivot_dm.index, key=sort_buckets)
    pivot_dm = pivot_dm.reindex(sorted_index)

    # Build Figure
    fig17 = px.imshow(
        pivot_dm,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=heatmap_scale
    )

    fig17.update_layout(
        height=500, # Medium Chart
        title=dict(
            text='<b>Duration Bucket vs. Maturity Level Distribution</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=80, b=40, l=150, r=40),
        coloraxis_colorbar=dict(
            title="<b>Total Titles</b>",
            thicknessmode="pixels", thickness=15,
            lenmode="pixels", len=300,
            yanchor="middle", y=0.5,
            ticks="outside"
        )
    )

    fig17.update_xaxes(
        title_text="<b>Maturity Level (1-5)</b>",
        type='category',
        side='bottom',
        showgrid=False
    )

    fig17.update_yaxes(
        title_text="<b>Content Duration Bucket</b>", 
        title_standoff=25,
        type='category',
        showgrid=False
    )

    st.plotly_chart(fig17, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The absolute center of gravity for the entire Netflix catalog is the **90–120 minute duration window at Maturity Level 4 (Adult)**, representing the highest concentration of titles on the platform.
        * **Commercial Implication:** Confirms that despite experimental formats, the platform's core acquisition and production strategy still revolves around the standard 1.5 to 2-hour mature feature film, paired with high volumes of single-season TV shows across all demographics.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 18 — TEMPORAL SHIFT IN GENRE STRATEGY
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Temporal Shift in Genre Strategy</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    time_df = df[(df['year_added'] >= 2015) & (df['year_added'] <= 2021)].copy()
    genre_exploded = time_df.explode('genre_list').dropna(subset=['genre_list'])
    genre_exploded['genre_list'] = genre_exploded['genre_list'].str.strip()

    def map_genre_root(g):
        g = str(g).lower()
        if 'international' in g: return 'International'
        if 'comed' in g: return 'Comedy'
        if 'drama' in g: return 'Drama'
        if 'documentar' in g: return 'Documentary'
        if 'action' in g or 'adventure' in g: return 'Action & Adventure'
        if 'kid' in g or 'children' in g or 'family' in g: return 'Kids & Family'
        if 'thrill' in g or 'horror' in g: return 'Thriller & Horror'
        if 'romanc' in g or 'romantic' in g: return 'Romance'
        return 'Other'

    genre_exploded['genre_root'] = genre_exploded['genre_list'].apply(map_genre_root)
    genre_exploded = genre_exploded[genre_exploded['genre_root'] != 'Other']
    
    top_7_genres = genre_exploded['genre_root'].value_counts().head(7).index.tolist()
    genre_top7 = genre_exploded[genre_exploded['genre_root'].isin(top_7_genres)]
    
    yearly_counts = genre_top7.groupby(['year_added', 'genre_root']).size().reset_index(name='count')
    yearly_totals = yearly_counts.groupby('year_added')['count'].transform('sum')
    yearly_counts['share_pct'] = (yearly_counts['count'] / yearly_totals) * 100

    # Build Figure
    fig18 = go.Figure()

    genre_colors = {
        'International': NETFLIX_COLORS['red'],       
        'Romance': NETFLIX_COLORS['dark_red'],        
        'Action & Adventure': '#FF6B6B',              
        'Comedy': '#221F1F',                          
        'Drama': '#404040',                           
        'Kids & Family': '#606060',                   
        'Thriller & Horror': '#808080'                
    }

    for genre in top_7_genres:
        genre_data = yearly_counts[yearly_counts['genre_root'] == genre].sort_values('year_added')
        line_color = genre_colors.get(genre, '#606060')
        line_width = 4 if genre == 'International' else 2
     
        fig18.add_trace(
            go.Scatter(
                x=genre_data['year_added'],
                y=genre_data['share_pct'],
                mode='lines+markers',
                name=genre,
                line=dict(color=line_color, width=line_width),
                marker=dict(size=8, color=line_color),
                hovertemplate=f"<b>{genre}</b><br>Year: %{{x}}<br>Share: %{{y:.1f}}%<extra></extra>"
            )
        )

    fig18.update_layout(
        height=750, # Large Chart / Time Series
        title=dict(
            text='<b>Temporal Shift in Genre Strategy (2015–2021)</b><br><sup>Normalized Share of Top 7 Macro-Genres</sup>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=90, b=50, l=60, r=40),
        xaxis=dict(
            title='<b>Year Added</b>',
            tickmode='linear',
            dtick=1,                            
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray'],
            zeroline=False
        ),
        yaxis=dict(
            title='<b>Percentage Share (%)</b>',
            showgrid=True,
            gridcolor=NETFLIX_COLORS['light_gray'],
            zeroline=True,
            zerolinecolor=NETFLIX_COLORS['black']
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=12, color=NETFLIX_COLORS['black'])
        ),
        hovermode='x unified' 
    )

    fig18.add_vline(
        x=2016, 
        line_width=2, 
        line_dash="dash", 
        line_color=NETFLIX_COLORS['black']
    )
    fig18.add_annotation(
        x=2016.1, 
        y=yearly_counts['share_pct'].max(),
        text="<b>2016 Global Expansion</b>",
        showarrow=False,
        xanchor="left",
        yshift=15,
        font=dict(color=NETFLIX_COLORS['black'], size=12)
    )

    st.plotly_chart(fig18, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Catalog Finding:** The data reveals a distinct "scissors effect" post-2016. The relative share of traditional American staples (Standard Comedies and Dramas) steadily declines as a percentage of the total pipeline. Simultaneously, International features/series and Documentaries experience a massive, sustained upward trajectory.
        * **Commercial Implication:** This mathematically visualizes Netflix's January 2016 global expansion. To retain audiences in 130+ new countries, Netflix heavily shifted budget away from expensive Hollywood licensing and poured it into regional/international production and highly bingeable, universally translatable formats like Docuseries.
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 19 — MACRO-GENRE LANDSCAPE: ERA, DURATION & MATURITY
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>Macro-Genre Landscape</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    df_b = df[df['maturity_level'] > 0].copy()
    df_b = df_b.explode('genre_list').dropna(subset=['genre_list'])
    df_b['genre_list'] = df_b['genre_list'].astype(str).str.strip()

    def map_genre_root_b(g):
        g = g.lower()
        if 'international' in g: return 'International'
        if 'stand-up' in g: return 'Stand-Up'              
        if 'sci-fi' in g or 'fantasy' in g: return 'Sci-Fi & Fantasy'
        if 'docu' in g: return 'Documentary'               
        if 'comed' in g: return 'Comedy'
        if 'action' in g or 'adventure' in g: return 'Action & Adventure'
        if 'kid' in g or 'children' in g or 'family' in g: return 'Kids & Family'
        if 'thrill' in g or 'horror' in g: return 'Thriller & Horror'
        if 'romanc' in g or 'romantic' in g: return 'Romance'
        if 'drama' in g: return 'Drama'
        return 'Other'

    df_b['genre_root'] = df_b['genre_list'].apply(map_genre_root_b)
    df_b = df_b[df_b['genre_root'] != 'Other']

    bubble_summary = df_b.groupby(['type', 'genre_root']).agg(
        Avg_Release_Year=('release_year', 'mean'),
        Avg_Duration=('duration_value', 'mean'),
        Avg_Maturity=('maturity_level', 'mean'),
        Total_Volume=('genre_root', 'count')
    ).reset_index()

    # Build Figure
    fig19 = px.scatter(
        bubble_summary,
        x='Avg_Release_Year',
        y='Avg_Duration',
        size='Total_Volume',
        color='Avg_Maturity',
        facet_col='type',
        facet_col_spacing=0.08,  
        text='genre_root',
        size_max=60,
        hover_name='genre_root',
        color_continuous_scale=[
            [0.0, NETFLIX_COLORS['black']],
            [1.0, NETFLIX_COLORS['red']]
        ]
    )

    fig19.update_layout(
        height=750, # Large Chart / Subplot
        title=dict(
            text='<b>Macro-Genre Landscape: Era, Duration & Maturity</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(t=100, b=120, l=60, r=40),  
        coloraxis_colorbar=dict(
            title="<b>Avg. Maturity (1-5)</b>",
            orientation="h",
            thicknessmode="pixels", thickness=15,
            lenmode="fraction", len=0.4,
            yanchor="top", y=-0.15,
            xanchor="center", x=0.5,
            ticks="outside"
        )
    )

    fig19.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[1]}</b>", font=dict(size=16)))
    fig19.update_traces(textposition='top center', textfont=dict(color=NETFLIX_COLORS['black'], size=10), marker=dict(opacity=0.75))  

    fig19.update_yaxes(matches=None, showticklabels=True, showgrid=True, gridcolor=NETFLIX_COLORS['light_gray'], nticks=7)
    fig19.update_yaxes(title_text='<b>Avg. Duration (Minutes)</b>', row=1, col=1)
    fig19.update_yaxes(title_text='<b>Avg. Duration (Seasons)</b>',range=[0.8, 3.2], row=1, col=2)

    fig19.update_xaxes(
        range=[2005, 2022], 
        showgrid=True, 
        gridcolor=NETFLIX_COLORS['light_gray'], 
        title_text='<b>Avg. Release Year</b>',
        nticks=7
    )

    st.plotly_chart(fig19, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Strategic Positioning (Movies):** Instantly reveals the coordinates of Netflix's film strategy. For example, it visually proves if Documentaries skew highly modern (far right X) and mature (Dark Red) but require shorter attention spans (lower Y), while Drama/International/Comedy dominates the volume (massive bubbles).
        * **Strategic Positioning (TV Shows):** Differentiates viewer commitment requirements. It exposes whether Kids' Animation (black color) sustains longer/shorter/similar multi-season runs (on Y axis) compared to modern adult thrillers (Dark Red).
        """)

    st.markdown("---")

    # ------------------------------------------------------------
    # CHART 20 — END-TO-END CATALOG FLOW (ORDERED 3-PILLAR)
    # ------------------------------------------------------------
    st.markdown(f"<h3 style='color: {NETFLIX_COLORS['black']};'>End-to-End Catalog Flow</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    df_cap = df[df['maturity_level'] > 0].copy()

    df_cap = df_cap.dropna(subset=['country'])
    df_cap = df_cap[~df_cap['country'].astype(str).str.lower().str.contains('unknown')]
    df_cap = df_cap[df_cap['country'].astype(str).str.strip() != '']

    top_5_countries = df_cap['country'].value_counts().head(5).index.tolist()
    df_cap = df_cap[df_cap['country'].isin(top_5_countries)]

    country_mapping = {country: i for i, country in enumerate(top_5_countries)}
    df_cap['country_color_index'] = df_cap['country'].map(country_mapping)

    df_cap = df_cap.explode('genre_list').dropna(subset=['genre_list'])
    df_cap['genre_list'] = df_cap['genre_list'].astype(str).str.strip()

    def map_genre_root_capstone(g):
        g = g.lower()
        if 'stand-up' in g: return 'Stand-Up'
        if 'sci-fi' in g or 'fantasy' in g: return 'Sci-Fi & Fantasy'
        if 'docu' in g: return 'Documentary'
        if 'comed' in g: return 'Comedy'
        if 'action' in g or 'adventure' in g: return 'Action & Adventure'
        if 'kid' in g or 'children' in g or 'family' in g: return 'Kids & Family'
        if 'thrill' in g or 'horror' in g: return 'Thriller & Horror'
        if 'romanc' in g or 'romantic' in g: return 'Romance'
        if 'drama' in g: return 'Drama'
        return 'Other'

    df_cap['genre_root'] = df_cap['genre_list'].apply(map_genre_root_capstone)
    df_cap = df_cap[df_cap['genre_root'] != 'Other']

    top_5_genres_cap = df_cap['genre_root'].value_counts().head(5).index.tolist()
    df_cap = df_cap[df_cap['genre_root'].isin(top_5_genres_cap)]

    df_cap['format_genre'] = df_cap['type'] + " - " + df_cap['genre_root'].astype(str)
    df_cap['maturity_level'] = df_cap['maturity_level'].astype(int)

    format_genre_order = []
    for genre in top_5_genres_cap:
        for fmt in ['Movie', 'TV Show']:  
            label = f"{fmt} - {genre}"
            if label in df_cap['format_genre'].unique():
                format_genre_order.append(label)

    country_colors = [
        NETFLIX_COLORS['red'],        
        NETFLIX_COLORS['black'],      
        '#FF9999',                    
        '#808080',                    
        '#D9D9D9'                     
    ]

    # Build Figure
    fig20 = px.parallel_categories(
        df_cap,
        dimensions=['country', 'format_genre', 'maturity_level'],
        color='country_color_index',
        color_continuous_scale=country_colors,
        labels={
            'country': 'Origin Country',
            'format_genre': 'Format & Macro-Genre',
            'maturity_level': 'Target Maturity'
        }
    )

    fig20.data[0].dimensions[0].update(categoryorder='array', categoryarray=df_cap['country'].value_counts().index.tolist())
    fig20.data[0].dimensions[1].update(categoryorder='array', categoryarray=format_genre_order)
    fig20.data[0].dimensions[2].update(categoryorder='array', categoryarray=[5, 4, 3, 2, 1])

    fig20.update_layout(
        height=750, 
        title=dict(
            text='<b>End-to-End Catalog Flow: Origin to Audience</b>',
            font=dict(size=20, color=NETFLIX_COLORS['black']),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=90, b=50, l=150, r=60), # Increased left margin
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        coloraxis_showscale=False,
        font=dict(size=10) # Shrink node text to prevent smudging
    )

    fig20.update_traces(
        line_shape='hspline',
        labelfont=dict(size=14, color=NETFLIX_COLORS['black']), # Keeps top column names crisp and readable
        tickfont=dict(size=9, color=NETFLIX_COLORS['black'])    # Shrinks the node names (USA, India, etc.) to stop the smudging
    )
    
    st.plotly_chart(fig20, use_container_width=True)

    with st.expander("💡 View Key Insights"):
        st.markdown("""
        * **Regional Specialization:** Interacting with the chart visually proves distinct production strategies. Highlighting India reveals a massive, concentrated funnel directly into Movie Dramas/Action, whereas highlighting the United Kingdom reveals a much wider, fragmented split into TV Shows and Comedies.
        * **Demographic Pooling:** By tracing the country-colored ribbons to the final pillar, it becomes instantly clear which global hubs are responsible for supplying Netflix's heaviest TV-MA (Level 5) adult content versus family-friendly tiers.
        """)