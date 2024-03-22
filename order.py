import requests
from flask import Flask
app = Flask(__name__)
CATALOG_SERVER_URL = 'http://172.17.0.2:5001'
ORDER_SERVER_URL = 'http://172.17.0.3:5002' 

@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase_item(item_id):
    # Check if the item is in stock
    response = requests.get(f'{CATALOG_SERVER_URL}/info', params={'id': item_id})
    if response.status_code == 200:
        item_info = response.json()
        if item_info['stock'] > 0:
            # If item is in stock, we decrement the stock by 1
            updated_stock = item_info['stock'] - 1
            update_response = requests.post(f'{CATALOG_SERVER_URL}/update', json={'id': item_id, 'stock': updated_stock})
            if update_response.status_code == 200:
                return("Purchase successful!") , 200
            else:
                return("Failed to update stock.") , 500
        else:
            return("Item is out of stock.") , 400
    else:
        return("Failed to retrieve item information.") , 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
