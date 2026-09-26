# DataPulse - Business Intelligence & Sales Analytics Platform

![DataPulse](https://img.shields.io/badge/DataPulse-BI%20Platform-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive, production-ready Business Intelligence platform that analyzes sales and customer data, converting raw transactional data into actionable business insights through interactive dashboards and SQL-powered analytics.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Dataset Description](#dataset-description)
- [Technologies Used](#technologies-used)
- [SQL Concepts Demonstrated](#sql-concepts-demonstrated)
- [Installation Instructions](#installation-instructions)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Key Business Insights](#key-business-insights)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

DataPulse is an end-to-end Business Intelligence platform designed for e-commerce and retail businesses. It provides real-time analytics dashboards, customer segmentation, product performance analysis, and SQL-powered insights to help businesses make data-driven decisions.

### Key Objectives

- Transform raw transactional data into actionable business insights
- Provide real-time KPI monitoring and trend analysis
- Enable customer segmentation and lifetime value analysis
- Support product portfolio optimization
- Demonstrate advanced SQL concepts for data analysis

## ✨ Features

### Dashboard Pages

1. **Executive Overview**
   - KPI cards: Total Revenue, Orders, Profit, Profit Margin, Average Order Value, Total Customers
   - Monthly revenue trend charts
   - Sales by region visualization
   - Profit by category analysis
   - Top 10 products display

2. **Sales Analytics**
   - Monthly and yearly sales trends
   - Category performance metrics
   - Regional performance analysis
   - Discount vs Profit analysis
   - Top and bottom performing products
   - Sub-category breakdown

3. **Customer Analytics**
   - Customer segmentation by purchase frequency
   - Top customers by revenue
   - Repeat customer analysis
   - Customer Lifetime Value (CLV) estimation
   - Geographic customer distribution
   - Segment performance comparison

4. **Product Analytics**
   - Best-selling products by quantity
   - Most profitable products by margin
   - Low-performing products identification
   - Category and sub-category analysis
   - Product profitability scatter analysis
   - High revenue, low profit product alerts

5. **SQL Insights**
   - Interactive SQL query explorer
   - 8+ advanced SQL query examples
   - Query explanations and business insights
   - Real-time query execution and results
   - SQL concepts reference guide

6. **Business Recommendations**
   - Automated insight generation
   - Priority-based recommendations
   - Action items and next steps
   - Supporting data analysis
   - Regional performance alerts
   - Product portfolio optimization suggestions

### Interactive Filters

- **Date Range**: Filter data by custom date range
- **Region**: Filter by geographic region
- **Category**: Filter by product category
- **Customer Segment**: Filter by customer type (Consumer, Corporate, Home Office)

## 🏗️ Architecture

```
DataPulse/
│
├── app.py                      # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── generate_data.py            # Data generation script
│
├── data/                        # Data directory
│   ├── sales_data.csv          # Orders data
│   ├── customers.csv           # Customer data
│   ├── products.csv            # Product data
│   └── datapulse.db            # SQLite database (auto-generated)
│
├── database/                    # Database module
│   ├── __init__.py
│   ├── database.py             # Database connection and operations
│   ├── schema.sql              # Database schema definition
│   └── queries.sql              # SQL query examples
│
├── analytics/                   # Analytics modules
│   ├── __init__.py
│   ├── sales_analysis.py       # Sales analytics functions
│   ├── customer_analysis.py    # Customer analytics functions
│   └── product_analysis.py     # Product analytics functions
│
├── pages/                       # Streamlit pages
│   ├── __init__.py
│   ├── Executive_Overview.py   # Executive dashboard
│   ├── Sales_Analytics.py      # Sales analysis page
│   ├── Customer_Analytics.py   # Customer analysis page
│   ├── Product_Analytics.py    # Product analysis page
│   ├── SQL_Insights.py         # SQL query explorer
│   └── Business_Recommendations.py  # AI-powered recommendations
│
└── assets/                      # Static assets
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Executive│ │  Sales   │ │ Customer │ │ Product  │       │
│  │ Overview │ │ Analytics│ │ Analytics│ │ Analytics│       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analytics Layer                           │
│  ┌──────────────────┐ ┌──────────────────┐                 │
│  │ Sales Analysis   │ │ Customer Analysis│                 │
│  │ - Trends         │ │ - Segmentation   │                 │
│  │ - Performance    │ │ - CLV            │                 │
│  └──────────────────┘ └──────────────────┘                 │
│  ┌──────────────────┐                                        │
│  │ Product Analysis │                                        │
│  │ - Performance    │                                        │
│  │ - Profitability  │                                        │
│  └──────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLAlchemy ORM                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         SQLite / PostgreSQL Database                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │  │
│  │  │ Orders   │ │Customers │ │ Products │            │  │
│  │  └──────────┘ └──────────┘ └──────────┘            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Dataset Description

### Orders Table

| Column | Type | Description |
|--------|------|-------------|
| order_id | VARCHAR | Unique order identifier |
| order_date | DATE | Order date |
| customer_id | VARCHAR | Foreign key to customers |
| product_id | VARCHAR | Foreign key to products |
| region | VARCHAR | Geographic region |
| category | VARCHAR | Product category |
| sub_category | VARCHAR | Product sub-category |
| quantity | INTEGER | Quantity ordered |
| sales | DECIMAL | Total sales amount |
| profit | DECIMAL | Profit amount |
| discount | DECIMAL | Discount applied |

### Customers Table

| Column | Type | Description |
|--------|------|-------------|
| customer_id | VARCHAR | Unique customer identifier (PK) |
| customer_name | VARCHAR | Customer name |
| segment | VARCHAR | Customer segment (Consumer/Corporate/Home Office) |
| city | VARCHAR | Customer city |
| state | VARCHAR | Customer state |
| region | VARCHAR | Geographic region |

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| product_id | VARCHAR | Unique product identifier (PK) |
| product_name | VARCHAR | Product name |
| category | VARCHAR | Product category |
| sub_category | VARCHAR | Product sub-category |
| unit_price | DECIMAL | Unit price |

### Sample Data Statistics

- **Total Orders**: 2,000
- **Total Customers**: 200
- **Total Products**: 100
- **Date Range**: January 2022 - December 2024
- **Regions**: North, South, East, West, Central
- **Categories**: Technology, Furniture, Office Supplies

## 🛠️ Technologies Used

### Core Technologies

- **Python 3.8+**: Primary programming language
- **Streamlit 1.29**: Web application framework
- **Pandas 2.1**: Data manipulation and analysis
- **SQLAlchemy 2.0**: Database ORM and query building
- **Plotly 5.18**: Interactive data visualization

### Database

- **SQLite**: Default database for easy deployment
- **PostgreSQL**: Optional production database support
- **SQL**: Advanced query capabilities

### Data Processing

- **NumPy 1.26**: Numerical computing
- **Python-dateutil**: Date parsing utilities

## 💻 SQL Concepts Demonstrated

DataPulse showcases advanced SQL concepts through interactive examples:

1. **INNER JOIN**: Combine orders with customers and products
2. **LEFT JOIN**: Find all customers including those with no orders
3. **GROUP BY**: Aggregate data by category, region, segment
4. **HAVING**: Filter groups after aggregation
5. **Subqueries**: Filter orders above average value
6. **CTE (Common Table Expressions)**: Complex multi-step queries
7. **Window Functions**:
   - RANK(): Rank products within categories
   - LAG(): Calculate month-over-month growth
   - SUM() OVER(): Calculate running totals
   - ROW_NUMBER(): Assign sequential numbers
8. **Aggregations**: SUM, COUNT, AVG, MAX, MIN
9. **CASE WHEN**: Conditional logic and categorization
10. **Database Indexing**: Performance optimization on frequently queried columns

### Database Indexes

Indexes are created on:
- `orders.order_date` - For date range queries
- `orders.customer_id` - For customer-based analysis
- `orders.product_id` - For product-based analysis
- `orders.region` - For regional filtering
- `orders.category` - For category filtering
- `customers.region` - For geographic analysis
- `customers.segment` - For segmentation analysis
- `products.category` - For category analysis

## 📦 Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/datapulse.git
cd datapulse
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Generate Sample Data

```bash
python generate_data.py
```

This will create:
- `data/sales_data.csv` - Orders data
- `data/customers.csv` - Customer data
- `data/products.csv` - Product data

### Step 5: Initialize Database

The database is automatically initialized when you first run the application. The SQLite database will be created at `data/datapulse.db`.

## 🚀 Running the Application

### Local Development

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Using PostgreSQL (Optional)

To use PostgreSQL instead of SQLite:

1. Set environment variables:
```bash
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=datapulse
```

2. Create the database:
```sql
CREATE DATABASE datapulse;
```

3. Run the schema:
```bash
psql -U your_username -d datapulse -f database/schema.sql
```

4. Modify `app.py` to use PostgreSQL:
```python
db = get_database_manager(use_postgres=True)
```

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   - Create a GitHub repository
   - Push your code to the repository

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Click "Deploy"

3. **Environment Variables** (if using PostgreSQL)
   - In Streamlit Cloud, go to Settings → Secrets
   - Add your database credentials:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=your_host
   DB_PORT=5432
   DB_NAME=your_database
   ```

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python generate_data.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t datapulse .
docker run -p 8501:8501 datapulse
```

## 📈 Key Business Insights

DataPulse automatically generates actionable insights including:

### Regional Performance
- Identify top-performing regions for resource allocation
- Detect underperforming regions requiring attention
- Compare regional profit margins

### Customer Segmentation
- Identify high-value customer segments
- Calculate Customer Lifetime Value (CLV)
- Detect repeat purchase patterns
- Optimize marketing spend by segment

### Product Portfolio
- Identify best-selling products by quantity and revenue
- Detect high-revenue, low-profit products
- Find declining products requiring intervention
- Optimize inventory based on performance

### Pricing Strategy
- Analyze discount impact on profit margins
- Identify optimal discount levels
- Detect over-discounting patterns

### Seasonal Patterns
- Identify seasonal sales trends
- Plan inventory based on seasonal demand
- Optimize marketing calendar

## 📁 Project Structure

```
DataPulse/
│
├── app.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── generate_data.py                 # Data generation script
│
├── data/                            # Data files
│   ├── sales_data.csv             # Generated orders data
│   ├── customers.csv              # Generated customer data
│   ├── products.csv               # Generated product data
│   └── datapulse.db               # SQLite database (auto-created)
│
├── database/                        # Database module
│   ├── __init__.py                # Module init
│   ├── database.py                # Database manager class
│   ├── schema.sql                 # Database schema
│   └── queries.sql                # SQL query examples
│
├── analytics/                       # Analytics modules
│   ├── __init__.py                # Module init
│   ├── sales_analysis.py          # Sales analytics functions
│   ├── customer_analysis.py       # Customer analytics functions
│   └── product_analysis.py        # Product analytics functions
│
├── pages/                           # Streamlit pages
│   ├── __init__.py                # Module init
│   ├── Executive_Overview.py      # Executive dashboard
│   ├── Sales_Analytics.py         # Sales analysis page
│   ├── Customer_Analytics.py      # Customer analysis page
│   ├── Product_Analytics.py       # Product analysis page
│   ├── SQL_Insights.py            # SQL query explorer
│   └── Business_Recommendations.py # AI recommendations
│
└── assets/                          # Static assets (future use)
```

## 📸 Screenshots

### Executive Overview
*Placeholder: Dashboard showing KPI cards, revenue trend, regional sales*

### Sales Analytics
*Placeholder: Monthly/yearly trends, category performance, discount analysis*

### Customer Analytics
*Placeholder: Customer segmentation, CLV analysis, geographic distribution*

### Product Analytics
*Placeholder: Product performance, profitability scatter, category analysis*

### SQL Insights
*Placeholder: SQL query examples with explanations and results*

### Business Recommendations
*Placeholder: Automated insights with priority levels and action items*

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- Portfolio: [yourportfolio.com]
- LinkedIn: [yourlinkedin]
- GitHub: [yourgithub]

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly team for interactive visualization library
- SQLAlchemy team for the powerful ORM

## 📞 Support

For support, please open an issue in the GitHub repository or contact [your email].

---

**Built with ❤️ using Streamlit, Python,和 SQL**
