# 📊 Marketing Dashboard Pro

> A powerful, automated marketing analytics dashboard built with **vibe coding** - pure Streamlit + Plotly. No React, no complex builds. Just pure Python magic.

---

## 🔥 What is Vibe Coding?

**Vibe coding** is when you build entire applications without rigid planning - you go with the flow, iterate quickly, and let the code guide you. It's different from traditional coding:

| Traditional Coding | Vibe Coding |
|-----------------|------------|
| Plan everything first | Build and adapt |
| Extensive documentation | Code speaks for itself |
| Complex architecture | Simple is better |
| Multiple frameworks | Minimal dependencies |
| Weeks of planning | Hours of building |

**With vibe coding, I:**
- Start with a basic idea
- Build incrementally
- Fix issues as they come
- Refactor when needed
- Ship fast, iterate faster

---

## 🐛 Debugging Stories & Tough Spots

### 1. **Metric Card HTML Not Rendering**

**Problem:** Custom HTML metric cards weren't displaying - just showing raw HTML.

**Code that almost failed:**
```python
# First attempt - didn't work
st.markdown(f"<div class='metric-card'>{title}: {value}</div>")
```

**Debugging process:**
1. Checked if CSS was loaded - it wasn't in Streamlit
2. Realized Streamlit sandboxes HTML
3. Found `unsafe_allow_html=True` was missing

**Fixed:**
```python
# Final working code
st.markdown(f"""
<div class="metric-card" style="background: {gradient}">
    <p>{title}</p>
    <h2>{value}</h2>
</div>
""", unsafe_allow_html=True)  # ← THIS WAS KEY!
```

**Lesson:** Streamlit requires explicit permission for custom HTML.

---

### 2. **Data Generation Causing Division Errors**

**Problem:** Division by zero when calculating CTR for some campaigns.

**Code issue:**
```python
# This crashed when clicks > impressions
df['ctr'] = df['clicks'] / df['impressions'] * 100  # ZeroDivisionError!
```

**Debugging process:**
1. Checked data with `df.isnull().sum()`
2. Found 0 impressions in some rows
3. Added proper error handling

**Fixed:**
```python
# Safe calculation
df['ctr'] = np.where(
    df['impressions'] > 0,
    (df['clicks'] / df['impressions'] * 100).round(2),
    0
)
```

**Lesson:** Always handle edge cases with NumPy/Pandas.

---

### 3. **Plotly Charts Not Responsive**

**Problem:** Charts looked tiny on mobile - didn't scale properly.

**Initial code:**
```python
# Default chart - no sizing
fig = px.bar(df, x='platform', y='spend')
st.plotly_chart(fig)  # Uses full container but didn't work!
```

**Debugging process:**
1. Tested on different screen sizes
2. Found `use_container_width=True` parameter
3. Added responsive CSS

**Fixed:**
```python
# Responsive chart
fig = px.bar(df, x='platform', y='spend', title='Spend by Platform')
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    font=dict(family="Inter")  # Custom font
)
st.plotly_chart(fig, use_container_width=True)  # ← KEY PARAMETER!
```

**Lesson:** Always test on multiple screen sizes.

---

### 4. **Sidebar State Not Persisting**

**Problem:** Date filter reset every time I switched pages.

**Code issue:**
```python
# State reset on page change
date_range = st.date_input("Select Date Range", value=(start, end))
# Every page navigation → reset!
```

**Debugging process:**
1. Realized Streamlit re-runs on every interaction
2. Needed session state to persist
3. Used `st.session_state`

**Fixed:**
```python
# Persist state across interactions
if 'date_range' not in st.session_state:
    st.session_state.date_range = (start, end)

date_range = st.date_input(
    "Select Date Range",
    value=st.session_state.date_range
)
```

**Lesson:** Streamlit is reactive - need explicit state management.

---

### 5. **Data Cache Not Updating**

**Problem:** New data wasn't showing - dashboard showed old data.

**Code issue:**
```python
# Only runs once - but I changed data source!
@st.cache_data
def get_data():
    return pd.read_csv("new_data.csv")  # Won't refresh!
```

**Debugging process:**
1. Checked if file was being read
2. Realized cache was the issue
3. Added cache busting

**Fixed:**
```python
# Cache with TTL - refreshes every hour
@st.cache_data(ttl=3600)  # Time to live = 1 hour
def get_data():
    return pd.read_csv("data.csv")

# Or force refresh during development
@st.cache_data(show_spinner=False)  # No cache in dev mode
def get_data():
    return pd.read_csv("data.csv")
```

**Lesson:** Understand when to cache and when not to.

---

### 6. **Plotly Export Causing Errors**

**Problem:** `px.funnel()` wasn't working - function not found.

**Code issue:**
```python
import plotly.express as px
# Tried: px.funnel() - DOESN'T EXIST!
```

**Debugging process:**
1. Checked Plotly documentation
2. Found funnel is `go.Figure()` with funnel trace
3. Used correct API

**Fixed:**
```python
# Correct funnel - using graph_objects
import plotly.graph_objects as go

fig = go.Figure(go.Funnel(
    y=['Impressions', 'Clicks', 'Conversions'],
    x=[10000, 2500, 500]
))
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)
```

**Lesson:** Not all Plotly Express functions exist - sometimes need Graph Objects.

---

## 🛠️ Vibe Coding Philosophy

### What Worked:

✅ **Start Simple** - Basic dashboard first, then add features
✅ **Embrace Errors** - Each error taught me something
✅ **Iterate Fast** - Fix, test, repeat
✅ **Use Documentation** - Streamlit/Plotly docs are excellent
✅ **Test Often** - Run app frequently while building
✅ **Keep It Simple** - No over-engineering

### What's NOT Vibe Coding:

❌ Don't plan for every possible scenario
❌ Don't build "future-proof" architecture
❌ Don't over-engineer solutions
❌ Don't avoid errors - embrace them!
❌ Don't wait for "perfect" code

---

## 📈 Real Challenges I Faced

| Challenge | How I Solved It | Skill Gained |
|-----------|---------------|-------------|
| HTML not rendering | `unsafe_allow_html=True` | Streamlit security |
| Division by zero | `np.where()` | NumPy data handling |
| Charts not responsive | `use_container_width=True` | UI/UX |
| State lost | `st.session_state` | State management |
| Cache stale | TTL caching | Performance |
| Wrong API | Use `go.Figure()` | Plotly APIs |

---

## 🎯 What This Project Proves

- ✅ I can build full dashboards from scratch
- ✅ I debug issues independently  
- ✅ I understand my dependencies (Streamlit, Plotly, Pandas)
- ✅ I can read documentation
- ✅ I iterate quickly
- ✅ I ship working code

---

## 🔧 Hard Parts I Solved

1. **Custom UI in Streamlit** - HTML injection with safety
2. **Data validation** - Edge case handling
3. **State management** - Session state
4. **Performance** - Caching strategies
5. **Responsive design** - Chart sizing
6. **Multiple chart types** - Plotly Express vs Objects

This dashboard directly demonstrates:

| Skill | How It's Shown |
|-------|---------------|
| **API Integration** | Data generation module (easily connect to real APIs) |
| **Data Processing** | Pandas for cleaning, aggregating, transforming |
| **Visualization** | Multiple Plotly charts (line, bar, pie, scatter, funnel) |
| **Dashboarding** | Full Streamlit app with sidebar navigation |
| **Real-time** | Interactive filters, live updates |

---

## 🎯 Features

### 📈 Overview Dashboard
- Key Performance Indicators (KPIs)
- Daily trends visualization
- Platform distribution
- Campaign performance

### 📱 Campaign Analytics
- Filter by campaign type & platform
- Sort and compare campaigns
- Top performers table
- Revenue analysis

### 💰 Spend Analysis
- Total spend & revenue tracking
- ROI calculation
- Cost per click (CPC) analysis
- Platform comparison

### 🎯 Conversion Tracking
- Conversion funnel visualization
- Conversion rate by campaign type
- Cost per acquisition (CPA)
- Daily conversions

### 📱 Social Media Analytics
- Follower growth tracking
- Engagement metrics
- Likes, comments, shares analysis

### 📋 Reports & Export
- CSV export functionality
- Summary statistics
- Platform comparison

---

## 🛠️ Tech Stack

- **Python** - Core language
- **Streamlit** - Web dashboard framework
- **Pandas** - Data processing
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computing

---

## 🎬 Quick Start

```bash
# Clone the repo
git clone https://github.com/shashwatsharma076-create/-Automated-Marketing-Dashboard-.git
cd Marketing-Dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Then open **http://localhost:8501** in your browser!

---

## 📂 Project Structure

```
Marketing-Dashboard/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.md         # This file
```

---

## 🎨 Dashboard Pages

### 1. Overview
- Total impressions, clicks, conversions, revenue
- CTR, ROAS, Cost per conversion
- Daily trends line charts
- Platform pie charts

### 2. Campaigns
- Filter by campaign type & platform
- Sort by any metric
- Top 20 campaigns table
- Bar charts visualization

### 3. Social Media
- Follower count & growth
- Likes, comments, shares
- Engagement rate
- Area charts & multi-line

### 4. Spend Analysis
- Spend vs revenue scatter plot
- Platform comparison
- ROI tracking
- CPC metrics

### 5. Conversions
- Conversion funnel
- Conversion rate by type
- CPA calculation

### 6. Reports
- CSV download
- Summary statistics
- Platform & campaign comparison

---

## 🔧 How to Connect Real APIs

### Google Analytics Example
```python
from google.analytics import DataApiClient

def get_ga_data():
    client = DataApiClient()
    response = client.run_report(
        property_id="YOUR_PROPERTY_ID",
        date_ranges=[{"start_date": "30daysAgo", "end_date": "today"}],
        dimensions=[{"name": "date"}],
        metrics=[{"name": "sessions"}, {"name": "totalUsers"}]
    )
    return response
```

### Facebook Graph API
```python
import requests

def get_fb_metrics(access_token):
    url = f"https://graph.facebook.com/v18.0/me/insights"
    params = {
        'access_token': access_token,
        'metric': 'page_impressions,page_engagement'
    }
    return requests.get(url, params=params).json()
```

### Google Ads API
```python
from google.ads.googleads import Client

def get_google_ads_data():
    client = Client(login_customer_id="YOUR_ID")
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks
        FROM campaign
    """
    return ga_service.search_stream(query=query)
```

---

## 📊 Sample Metrics Displayed

| Metric | Description |
|--------|-------------|
| Total Impressions | Total ad impressions |
| Total Clicks | Total click-throughs |
| CTR | Click-through rate % |
| Conversions | Total conversions |
| Spend | Total ad spend |
| Revenue | Total revenue |
| ROAS | Return on Ad Spend |
| CPA | Cost per Acquisition |

---

## 🎯 What Makes This Stand Out

✅ **Multiple Pages** - SPA-like navigation  
✅ **Interactive Filters** - Real-time filtering  
✅ **Download Reports** - Export to CSV  
✅ **Responsive Design** - Works on all screens  
✅ **Custom Styling** - Gradient metric cards  
✅ **Error Handling** - Safe data loading  

---

## 💻 Skills Demonstrated

- Streamlit web development
- Pandas data manipulation
- Plotly interactive charts
- API integration patterns
- Dashboard architecture
- Real-time filtering
- Data export functionality
- Responsive design

---

## 🤝 Connect

Give it a ⭐ if you like it!

Built with 💙 by **@shashwatsharma076-create**

---

> *"The best way to predict the future is to create it with data."*