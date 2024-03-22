import argparse
import requests

CATALOG_SERVER_URL = "http://catalog-server:5001"
ORDER_SERVER_URL = "http://order-server:5002"

def query_by_subject(topic):
    url = f"{CATALOG_SERVER_URL}/query"
    params = {"topic": topic}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)

def query_by_item(item_id):
    url = f"{CATALOG_SERVER_URL}/query"
    params = {"item_id": item_id}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)

def update_item(item_id, cost=None, stock=None):
    url = f"{CATALOG_SERVER_URL}/update/{item_id}"
    data = {}
    if cost:
        data["cost"] = cost
    if stock:
        data["stock"] = stock
    response = requests.put(url, json=data)
    print(response.json())

def purchase_item(item_id):
    url = f"{ORDER_SERVER_URL}/purchase/{item_id}"
    response = requests.post(url)
    print(response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for interacting with catalog and order servers")
    parser.add_argument("command", choices=["query-subject", "query-item", "update", "purchase"])
    parser.add_argument("--topic", help="Topic for query-by-subject")
    parser.add_argument("--item-id", type=int, help="Item ID for query-by-item and update")
    parser.add_argument("--cost", type=float, help="New cost for update")
    parser.add_argument("--stock", type=int, help="New stock for update")
    args = parser.parse_args()

    if args.command == "query-subject":
        query_by_subject(args.topic)
    elif args.command == "query-item":
        query_by_item(args.item_id)
    elif args.command == "update":
        update_item(args.item_id, args.cost, args.stock)
    elif args.command == "purchase":
        purchase_item(args.item_id)
