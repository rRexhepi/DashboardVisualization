# DashboardVisualization

---

## 📄 Project Description

The **DashboardVisualization** is an interactive data visualization tool developed using Python's Bokeh library. It provides insights into the British Film Institute's expenditures over £25,000, allowing users to explore, filter, and analyze spending data through intuitive tables and dynamic graphs.

---

## 🛠️ Features

- **Summary Tab:** Aggregated view of total records per month.
- **Data Tab:** Detailed view with interactive filters for Expense Area, Supplier, Month, and Transaction Reference. Includes a download button to export filtered data as a CSV file.
- **Graphs Tab:** Interactive bar and line charts displaying total records and total amount over time with hover tooltips for enhanced data insights.

---

## 🚀 Getting Started

### 🎯 Prerequisites

- **Python 3.7+**
- **pip** (Python package installer)

### 🔧 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/bfi-spend-dashboard.git
   cd bfi-spend-dashboard

2. **Set Up a Virtual Environment (Recommended)**
- Creating a virtual environment ensures that your project dependencies are isolated from other Python projects on your system.
   ```bash
   # Create a virtual environment named 'venv'
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate

3. **Install Dependencies**
- Install the required Python packages using the requirements.txt file.

   ```bash
   pip install -r requirements.txt

## 🖥️ Usage
1. Prepare the Data
- Ensure that your input CSV file is located at data/input/tabula-bfi-payments-over-25000-report-2014-15.csv. If your data file is named differently or located elsewhere, update the vouchers_data_path variable in dashboard.py accordingly.

2. Run the Dashboard
- Execute the dashboard.py script to generate and view the dashboard.
   ```bash
   python dashboard.py

3. View the Dashboard
- After running the script, the dashboard will be generated at data/output/Dashboard.html. Open this file in your web browser to interact with the dashboard.
   ```bash
   open data/output/Dashboard.html  # macOS
   # or
   start data/output/Dashboard.html  # Windows
   # or manually navigate to the file in your browser

## 📁 Project Structure
- 
   ```bash
   bfi-spend-dashboard/
   │
   ├── data/
   │   ├── input/
   │   │   └── tabula-bfi-payments-over-25000-report-2014-15.csv
   │   └── output/
   │       └── Dashboard.html
   │
   ├── dashboard.py
   ├── requirements.txt
   ├── README.md
   └── .gitignore
