# forecastly
Development of AI based sales forecasting system
# Forecastly 

Forecastly is an AI-powered web application designed to help businesses forecast future revenue and sales trends using machine learning algorithms.

## Overview

Forecastly allows users to upload historical sales data and generate accurate forecasts, identify anomalies, and analyze future business performance through an intuitive dashboard.

The system automatically evaluates multiple forecasting models and selects the best-performing algorithm based on prediction accuracy.

## Features

###  Sales Forecasting

* Revenue forecasting for upcoming periods
* Automatic model evaluation and selection
* Forecast accuracy tracking

###  Machine Learning

* Ridge Regression
* Decision Tree Regression
* Performance comparison using forecasting metrics

###  Business Analytics

* Revenue trends visualization
* Forecast charts and dashboards
* Performance insights

###  Anomaly Detection

* Detection of unusual sales patterns
* Identification of unexpected spikes or drops

###  Scenario Analysis

* Optimistic Scenario (+15%)
* Realistic Scenario
* Pessimistic Scenario (-15%)

###  User Management

* Secure user registration and login
* Personal dashboard
* File management system

###  Admin Panel

* User statistics
* Uploaded datasets monitoring
* System analytics

## Technology Stack

### Backend

* Python
* Flask
* SQLAlchemy
* SQLite

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

## Project Structure

```text
forecastly/
│
├── app.py
├── models.py
├── ml/
│   └── forecasting.py
├── templates/
├── static/
├── uploads/
├── instance/
└── requirements.txt
```

## How It Works

1. User uploads a CSV or Excel file containing historical sales data.
2. The system preprocesses the dataset.
3. Multiple machine learning algorithms are trained and evaluated.
4. The best-performing model is selected automatically.
5. Forecasts, analytics, and visualizations are generated.
6. Users can explore future business scenarios and insights.

## Dataset Requirements

The uploaded dataset should contain:

| Column  | Description      |
| ------- | ---------------- |
| Date    | Transaction date |
| Revenue | Revenue amount   |

Example:

| Date       | Revenue |
| ---------- | ------- |
| 2025-01-01 | 1500    |
| 2025-01-02 | 1650    |
| 2025-01-03 | 1720    |

## Installation

```bash
git clone https://github.com/yourusername/forecastly.git

cd forecastly

pip install -r requirements.txt

python app.py
```

## Future Improvements

* Additional forecasting algorithms
* Power BI integration
* Export forecast reports
* Advanced business intelligence dashboards
* Cloud deployment

## Author

**Aizere Sabyr**

International Information Technology University (IITU)

Bachelor's Degree in Information Systems

Business Analysis Track

## License

This project was developed for educational and academic purposes.
