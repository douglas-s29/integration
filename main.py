import requests
import pandas as pd


# Authentication and URL to request API
api_key = 'Mq1EWAXiHwraLIQgfq4stmUxKiM6VpC5Xd9o3wuX1Go'
url = 'https://api.instabuy.com.br/store/products'

# Define the headers for the API request
headers = {
    'api-key': api_key,
    'Content-Type': 'application/json'
}

# Dictionary of months
months = {
    'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
    'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
    'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
}

# Function to convert the date into the desired format
def convert_date(date_str):
    if pd.notnull(date_str) and isinstance(date_str, str) and date_str:
        parts = date_str.split('-')
        if len(parts) == 3:
            day, month_abbrev, year = parts
            month = months.get(month_abbrev.upper())
            if month and year.startswith('20'):
                year = year[2:]
                return f"20{year}-{month}-{day.zfill(2)}T00:00:00"
    return None

# Function to format numerical values with correct decimal places
def format_decimal(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
    try:
        value = float(value)
        return '{:.2f}'.format(value)
    except ValueError:
        return value

# Function to replace blank values with an empty string
def replace_empty(value):
    if pd.isnull(value):
        return ''
    return value

# Reading from CSV file using Pandas
df = pd.read_csv('items.csv', delimiter=';')

# Apply transformations to all cells in the DataFrame
df['Preço regular'] = df['Preço regular'].apply(format_decimal)
df['Promocao'] = df['Promocao'].apply(format_decimal)
df['Data termino promocao'] = df['Data termino promocao'].apply(convert_date)

# Converting stock to int
df['estoque'] = df['estoque'].apply(int)  

# Replace blank values in the 'Promocao' field with an empty string
df['Promocao'] = df['Promocao'].apply(replace_empty)

# Scroll through the products and make PUT requests to the Instabuy API
for list_items, row in df.iterrows():
    data = {
        "products": [
            {
                "internal_code": int(row['Código interno']),
                "barcodes": [str(row['Código de barras'])],
                "name": row['Nome'],
                "price": row['Preço regular'],
                "promo_price": row['Promocao'],
                "promo_end_at": row['Data termino promocao'],
                "stock": row['estoque'],
                "visible": bool(row['ativo'])
            }
        ]
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        updated_product_data = response.json() 

        data_data = updated_product_data.get('data', '')      
        data_status = updated_product_data.get('status', '')
        data_count = row['estoque']
        http_status = response.status_code

        resposta_api = {
            'Data': data_data,
            'Status': data_status,
            'Count': data_count,
            'Status HTTP': http_status
        }
        

        if data_status == 'success':
            print(f"Product updated {row['Código interno']}: {resposta_api}")
        else:
            print(f"Error update product {row['Código interno']}: {data_data}")

    else:
        print(f"Error update product {row['Código interno']}: {response.text}")