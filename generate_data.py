import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define realistic data
regions = ['North', 'South', 'East', 'West', 'Central']
segments = ['Consumer', 'Corporate', 'Home Office']
categories = ['Technology', 'Furniture', 'Office Supplies']
sub_categories = {
    'Technology': ['Phones', 'Laptops', 'Accessories', 'Monitors', 'Printers'],
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Desks', 'Furnishings'],
    'Office Supplies': ['Paper', 'Binders', 'Art', 'Storage', 'Appliances']
}

# Generate customers
num_customers = 200
customers = []
for i in range(num_customers):
    customer_id = f"CUST-{i+1:04d}"
    customer_name = f"Customer {i+1}"
    segment = random.choice(segments)
    region = random.choice(regions)
    
    # Assign cities based on region
    cities = {
        'North': ['New York', 'Boston', 'Chicago'],
        'South': ['Atlanta', 'Dallas', 'Houston'],
        'East': ['Philadelphia', 'Washington DC', 'Baltimore'],
        'West': ['Los Angeles', 'San Francisco', 'Seattle'],
        'Central': ['Denver', 'Kansas City', 'Minneapolis']
    }
    city = random.choice(cities[region])
    
    states = {
        'New York': 'NY', 'Boston': 'MA', 'Chicago': 'IL',
        'Atlanta': 'GA', 'Dallas': 'TX', 'Houston': 'TX',
        'Philadelphia': 'PA', 'Washington DC': 'DC', 'Baltimore': 'MD',
        'Los Angeles': 'CA', 'San Francisco': 'CA', 'Seattle': 'WA',
        'Denver': 'CO', 'Kansas City': 'MO', 'Minneapolis': 'MN'
    }
    state = states[city]
    
    customers.append({
        'customer_id': customer_id,
        'customer_name': customer_name,
        'segment': segment,
        'city': city,
        'state': state,
        'region': region
    })

customers_df = pd.DataFrame(customers)

# Generate products
num_products = 100
products = []
for i in range(num_products):
    product_id = f"PROD-{i+1:04d}"
    category = random.choice(categories)
    sub_category = random.choice(sub_categories[category])
    product_name = f"{sub_category} Model {random.randint(1, 50)}"
    unit_price = round(random.uniform(10, 500), 2)
    
    products.append({
        'product_id': product_id,
        'product_name': product_name,
        'category': category,
        'sub_category': sub_category,
        'unit_price': unit_price
    })

products_df = pd.DataFrame(products)

# Generate orders
num_orders = 2000
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)

orders = []
for i in range(num_orders):
    order_id = f"ORD-{i+1:05d}"
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    customer = random.choice(customers)
    product = random.choice(products)
    
    quantity = random.randint(1, 10)
    discount = random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.25])
    
    # Calculate sales and profit
    unit_price = product['unit_price']
    sales = round(unit_price * quantity * (1 - discount), 2)
    profit = round(sales * random.uniform(0.1, 0.3), 2)
    
    orders.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'customer_id': customer['customer_id'],
        'product_id': product['product_id'],
        'region': customer['region'],
        'category': product['category'],
        'sub_category': product['sub_category'],
        'quantity': quantity,
        'sales': sales,
        'profit': profit,
        'discount': discount
    })

orders_df = pd.DataFrame(orders)

# Save to CSV
orders_df.to_csv('data/sales_data.csv', index=False)
customers_df.to_csv('data/customers.csv', index=False)
products_df.to_csv('data/products.csv', index=False)

print(f"Generated {len(orders_df)} orders")
print(f"Generated {len(customers_df)} customers")
print(f"Generated {len(products_df)} products")
print("Data saved to data/ directory")
