from pymongo import MongoClient
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_databases(client):
    return client.list_database_names()

def list_collections(db):
    return db.list_collection_names()

def show_documents(collection, limit=5):
    for doc in collection.find().limit(limit):
        print(doc)
        print("-"*40)

def main():
    # URI diye directly connect
    uri = "mongodb+srv://hellking1:hellking1@cluster0.zqg7rco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    while True:
        clear_screen()
        print("Databases:")
        dbs = list_databases(client)
        for i, db_name in enumerate(dbs):
            print(f"{i+1}. {db_name}")
        choice = input("Select database number (or 'q' to quit): ")

        if choice.lower() == 'q':
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(dbs):
            continue

        db = client[dbs[int(choice)-1]]

        while True:
            clear_screen()
            print(f"Database: {db.name}")
            collections = list_collections(db)
            for i, col_name in enumerate(collections):
                print(f"{i+1}. {col_name}")
            col_choice = input("Select collection number (or 'b' to go back): ")

            if col_choice.lower() == 'b':
                break
            if not col_choice.isdigit() or int(col_choice) < 1 or int(col_choice) > len(collections):
                continue

            collection = db[collections[int(col_choice)-1]]
            clear_screen()
            print(f"Collection: {collection.name}")
            show_documents(collection)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
