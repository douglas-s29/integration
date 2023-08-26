# Instabuy Product Update Script

This script reads data from a CSV file containing product information, transforms the data, and updates the products using the Instabuy API.

## Requirements

- Python 3.10.4 (recommended)
- Required Python packages:
- requests
- pandas
```

 pip install requests

```
```

 pip install pandas

```

## Getting Started

1. Clone or download this repository to your local machine.

2. Install the required Python packages by running the following command:

3. Download the CSV file named items.csv. Make sure the CSV columns have the names.
- `Código interno`  
- `Código de barras`
- `Nome`
- `Preço regular`
- `Promocao`
- `Data termino promocao`
- `estoque`
- `ativo`

4. Adjust the `api_key` variable in the script to match your Instabuy API credentials and endpoint.

5. Run the script using the following command:

   `python3 main.py`


## Features

- Dates are returned in ISO8601 format: YYYY-MM-DDTHH:MM:SS.
- Formats numerical values with only 2 decimal places.
- Handles empty values in certain fields.
- Sends PUT requests to the Instabuy API to update products.

## Notes

- For the script to work normally, it is extremely important that the name of the CSV file is 'items.csv' and is in the same folder as the 'main.py' file




