# Aaron Adekoya — Data Engineer Portfolio

A Streamlit application showcasing a CV, sales analytics dashboard, and sales forecast.

## Prerequisites

- Python 3.9 or higher

## Setup

1. **Clone the repository** and navigate into the project directory:

   ```bash
   cd App
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
streamlit run Home.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

## Project Structure

```
Home.py                             # Main entry point
sidebar.py                          # Sidebar component
requirements.txt                    # Python dependencies
data/
  generate_data.py                  # Script to generate sample sales data
  sales_data.csv                    # Sample sales dataset
pages/
  1_CV.py                           # CV page
  2_Sales_Analytics_Dashboard.py    # Sales analytics dashboard
  3_Sales_Forecast.py               # Sales forecasting page
```
