import argparse, requests, json

CATALOG_SERVER_URL = 'http://localhost:5001'
ORDER_SERVER_URL = 'http://localhost:5002'  # Assuming the order server is running on port 5002

def search_catalog(topic):
    try:
        response = requests.get(f'{CATALOG_SERVER_URL}/catalog', params={'query': topic})
        response.raise_for_status()  # Raise an exception for non-200 status codes
        books = response.json()
        if books:
        #     print("Books found in the catalog:")
        #     for book in books:
        #         print(f"Title: {book['title']}, Author: {book['author']}, Topic: {book['topic']}, Stock: {book['stock']}, Cost: {book['cost']}")
            print(books)
        else:
            print("No books found in the catalog for the given topic.")
    except requests.RequestException as e:
        print(f"Failed to retrieve catalog: {e}")

def get_item_info(item_id):
    try:
        response = requests.get(f'{CATALOG_SERVER_URL}/info', params={'id': item_id})
        response.raise_for_status()  # Raise an exception for non-200 status codes
        book_info = response.json()
        print(f"Title: {book_info['title']}, Author: {book_info['author']}, Topic: {book_info['topic']}, Stock: {book_info['stock']}, Cost: {book_info['cost']}")
    except requests.RequestException as e:
        print(f"Failed to retrieve item information: {e}")

def purchase_item(item_id):
        response = requests.post(f'{ORDER_SERVER_URL}/purchase/{item_id}')
        if response.status_code == 200:
            print("Purchase successful!")
        else:
            print("Failed to purchase book. Status code:", response.status_code)

def main():
    print("Welcome to the Bazar!")
    while True:
        print("\nOptions:")
        print("1. Search books by topic")
        print("2. Get book information by ID")
        print("3. Purchase a book")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            topic = input("Enter the topic: ")
            search_catalog(topic)
        elif choice == '2':
            book_id = input("Enter the book ID: ")
            get_item_info(book_id)
        elif choice == '3':
            book_id = input("Enter the book ID to purchase: ")
            purchase_item(book_id)
        elif choice == '4':
            print("Thank you for coming to Bazar !!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
