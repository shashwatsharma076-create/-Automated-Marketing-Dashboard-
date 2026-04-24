# 📊 Marketing Dashboard Pro

> A powerful, automated marketing analytics dashboard built with **Streamlit + Plotly**. Visualize key marketing metrics, track campaigns, analyze spend, and monitor conversions in real-time.

---

## 🚀 Why This Project is Perfect for Jobs

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