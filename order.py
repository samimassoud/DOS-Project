import requests
from flask import Flask
app = Flask(__name__)
CATALOG_SERVER_URL = 'http://localhost:5001'
ORDER_SERVER_URL = 'http://localhost:5002'  # Assuming the order server is running on port 5002

@app.route('/purchase', methods=['POST'])
def purchase_item(item_id):
    # Check if the item is in stock
    response = requests.get(f'{CATALOG_SERVER_URL}/info', params={'id': item_id})
    if response.status_code == 200:
        item_info = response.json()
        if item_info['stock'] > 0:
            # If item is in stock, decrement the stock by 1
            updated_stock = item_info['stock'] - 1
            update_response = requests.post(f'{CATALOG_SERVER_URL}/update', json={'id': item_id, 'stock': updated_stock})
            if update_response.status_code == 200:
                print("Purchase successful!")
            else:
                print("Failed to update stock.")
        else:
            print("Item is out of stock.")
    else:
        print("Failed to retrieve item information.")

if __name__ == "__main__":
  #  item_id = input("Enter the ID of the item you want to purchase: ")
  #  purchase_item(item_id)
    app.run(debug=True, host='0.0.0.0', port=5002)
