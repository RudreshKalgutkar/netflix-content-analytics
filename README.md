```markdown
# 🍿 Netflix Content Strategy & Analytics

**Live Dashboard:** [View the Interactive Web App Here](https://netflix-content-analytics-rudreshkalgutkar.streamlit.app/)

## 📌 Project Overview
An end-to-end Python data analytics deployment exploring Netflix's global acquisition strategy, historical production velocity, and demographic content footprint. This project transitions from raw dataset ingestion and complex feature engineering in Jupyter to a fully deployed, interactive web application hosted on Streamlit Community Cloud. 

Developed through a rigorous, multi-phase lifecycle spanning initial data cleaning, broad structural architecture design, and meticulous visual refinement the final application consolidates 20 custom Plotly charts into a professional, high-performance executive dashboard.

## 🎯 Strategic Objectives

The primary objective is to decode Netflix's complete catalog strategy through a comprehensive 20-chart analysis, answering critical business questions:

* How does the foundational catalog composition balance across content formats, duration buckets, and unified maturity ratings?
* What are the historical acquisition trends, and how does the operational lag between original release and platform availability impact catalog growth?
* Which geographic hubs dominate the global production footprint, and what distinct content strategies define primary versus secondary regional markets?
* Which macro-genres and thematic roots drive platform volume, and how do they correlate with runtime and target demographics?
* Who are the key creative talents (directors and actors) shaping the catalog, and how do their contributions cluster globally?
* How do multi-dimensional variables—specifically Origin Country, Macro-Genre, and Target Maturity—interact to form the overarching content pipeline?

## 📊 Data Architecture & Feature Engineering

The foundation of the dashboard is built on a rigorously pre-processed dataset (`Netflix_Project_Final_V3.csv`), condensed from 11 original to 19 final columns, ensuring every field serves a traceable analytical purpose:

* **Explicit Null Imputation:** Resolved thousands of missing values across director, cast, and country fields by applying explicit categorical tags ("Uncredited Director," "Uncredited Cast," "Unknown Country"). This preserves these titles for volume-based analytics while enabling clean exclusion for talent-specific rankings.
* **Targeted Data Cleansing:** Dropped exactly 10 legacy catalog rows (0.1% of data, e.g., *Friends*, *Frasier*) lacking `date_added` where no defensible fill date existed.
* **Duration Standardization:** Collapsed a fragmented, NaN-heavy duration design into a streamlined `duration_value` and `duration_bucket` framework, utilizing content type to disambiguate units (minutes vs. seasons) for consistent numerical analysis.
* **Unified Maturity Scaling:** Harmonized disparate Movie and TV rating systems onto a single 0-5 numerical axis. A value of 0 was explicitly reserved for unrated/unknown content to prevent skewed aggregate calculations.
* **List-Based Tag Preservation:** Retained original comma-separated metadata within consolidated list columns (`director_list`, `cast_list`, `country_list`, `genre_list`). This optimized the dataset for on-demand `.explode()` operations in specific visualizations without exploding base row counts.
* **Advanced Feature Engineering:** Engineered deferred metrics such as `acquisition_lag` and `content_age` for time-series charts, and built a custom `genre_root` mapping within the application logic to accurately group highly fragmented sub-genres.

## 📈 Dashboard Architecture

The application features a persistent executive header containing high-level KPIs and total catalog metrics, anchored above a structured 6-tab interface that houses 20 custom interactive charts:

1. **Catalog Composition:** Foundational breakdown of the content mix, analyzing Movie vs. TV Show ratios alongside duration standardization and unified maturity levels.
2. **Acquisition Trends:** Time-series analysis focusing on platform growth, historical production volume, and the operational lag between initial release and Netflix availability.
3. **Global Footprint:** Geographic deep-dives utilizing regional breakdowns and spatial mapping to expose the production strategies of primary hubs and secondary international markets.
4. **Genre Intelligence:** Multi-variable exploration of macro-genres and root categorizations to identify thematic dominance and duration-to-genre correlations.
5. **Creative Talent:** Targeted analysis of actor and director frequencies—filtered of uncredited anomalies—mapping top talent contributions across content types.
6. **Advanced Synthesis:** Complex multi-dimensional visualizations, culminating in a Parallel Categories flow diagram (Chart 20) that maps the complete end-to-end pipeline from Origin Country to Macro-Genre to Target Maturity.

## 💡 Key Analytical Insights

* **Geographic Dominance:** The United States and India serve as the undisputed primary funnels for global content production, dwarfing secondary hubs like the UK, South Korea, and Japan.
* **Content Format Shifts:** The historical data reveals strategic shifts in the ratio of Movie acquisitions versus long-term TV Show investments.
* **Operational Latency:** Time-series analysis of the engineered `acquisition_lag` metric exposes the exact temporal gap between original release years and platform integration, mapping Netflix's dual strategy of aggressive contemporary licensing versus deferred archival cataloging.
* **Pipeline Synthesis (Country-to-Maturity):** The Chart 20 flow diagram reveals a rigid demographic pipeline where production origin heavily dictates macro-genre output and final target maturity tier (e.g., specific regional funnels disproportionately prioritizing tier-4 and tier-5 adult content over lower maturity brackets).
* **Creative Talent Clustering:** After explicitly filtering null imputations ("Uncredited Director/Cast") using `.explode()` on list-based tags, frequency mapping demonstrates that high-volume directors and actors are deeply localized within specific regional boundaries and thematic roots, rather than distributed across the platform's global footprint.
* **Format-Duration Disambiguation:** By standardizing duration into calculated `duration_value` and `duration_bucket` features, the data exposes clear catalog boundaries between feature-length movie investments and the volume of multi-season, binge-optimized television series.

## 🛠️ Technical Stack & Methodologies
**Languages & Libraries:**
* `Python 3.x`: Core programming language.
* `Pandas` / `NumPy`: Data manipulation, aggregation, and structural engineering.
* `Plotly` (Graph Objects & Express): Advanced interactive data visualization (Choropleths, Bubble Scatters, Parallel Categories).
* `Streamlit`: Web application framework and frontend UI.

**Methodologies & Deployment:**
* Exploratory Data Analysis (EDA) and Feature Engineering via Jupyter Notebooks.
* Cloud deployment and hosting via Streamlit Community Cloud.
* Environment dependency management (`requirements.txt`) utilizing strict version control to ensure stable cloud builds.
* Git-based version control for repository management.

## 📁 Repository Structure

```text
netflix-content-analytics/
│
├── data/
│   ├── netflixdata.csv                   # Raw original dataset
│   └── Netflix Dataset.docx              # Supporting data dictionary/documentation
│
├── images/
│   ├── overview.PNG                      # Dashboard Tab 1: Hero KPIs
│   ├── part1.PNG                         # Dashboard Tab 2: Content Split
│   ├── part2.PNG                         # Dashboard Tab 3: Historical Velocity
│   ├── part3.PNG                         # Dashboard Tab 4: Global Footprint
│   └── part4.PNG                         # Dashboard Tab 5: Macro Genre
│
├── app.py                                # Core Streamlit deployment script
├── Netflix Project Final V3.ipynb        # Data cleaning & engineering notebook
├── Netflix_Project_Final_V3.csv          # Cleaned dataset fueling the live app
└── requirements.txt                      # Cloud deployment dependencies

```

## 📊 Visual Portfolio

### 1. Executive Overview & KPIs

### 2. Content Type Split

### 3. Historical Production Velocity

### 4. Global Content Production Footprint

### 5. Macro Genre Landscape

## 🚀 How to Run Locally

To explore the dashboard on your local machine, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Open your terminal/command prompt in the project directory and install the required packages:
```bash
pip install -r requirements.txt

```


4. Launch the application:
```bash
streamlit run app.py

```


5. The dashboard will automatically open in your default web browser at `http://localhost:8501`.

---

© 2026 Rudresh Kalgutkar. All Rights Reserved.

```

```
