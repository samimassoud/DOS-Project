# CLI.py
import argparse

CATALOG_SERVER_URL = 'http://localhost:5001'
ORDER_SERVER_URL = 'http://localhost:5002'  # Assuming the order server is running on port 5002

def search_catalog(topic):
    response = requests.get(f'{CATALOG_SERVER_URL}/catalog', params={'query': topic})
    if response.status_code == 200:
        print(response.json())
    else:
        print("Failed to retrieve catalog.")

def get_item_info(item_id):
    response = requests.get(f'{CATALOG_SERVER_URL}/info', params={'id': item_id})
    if response.status_code == 200:
        print(response.json())
    else:
        print("Failed to retrieve item information.")

def purchase_item(item_id):
    response = requests.post(f'{ORDER_SERVER_URL}/purchase', json={'id': item_id})
    if response.status_code == 200:
        print(response.json())
    else:
        print("Purchase failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI for Catalog and Order Servers')
    parser.add_argument('action', choices=['search', 'info', 'purchase'], help='Action to perform')
    parser.add_argument('--topic', help='Topic to search (for search action)')
    parser.add_argument('--id', help='ID of the item (for info and purchase actions)')
    args = parser.parse_args()

    if args.action == 'search':
        search_catalog(args.topic)
    elif args.action == 'info':
        get_item_info(args.id)
    elif args.action == 'purchase':
        purchase_item(args.id)
