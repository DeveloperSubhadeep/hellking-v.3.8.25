from pymongo import MongoClient, errors
from tqdm import tqdm

# Old MongoDB
old_client = MongoClient("mongodb+srv://devildevil:devildevil@cluster0.0hajx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
old_db = old_client["cluster0"]
old_collection = old_db["Deendayal_files"]

# New MongoDB
new_client = MongoClient("mongodb+srv://hellking1:hellking1@cluster0.zqg7rco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
new_db = new_client["cluster0"]
new_collection = new_db["hellking_files"]

batch_size = 1000  # <- ekhane 100 set kora holo
batch = []
inserted, skipped, failed = 0, 0, 0
failed_docs = []

total_docs = old_collection.count_documents({})

for doc in tqdm(old_collection.find({}), total=total_docs, desc="Transferring"):
    batch.append(doc)
    if len(batch) == batch_size:
        try:
            new_collection.insert_many(batch, ordered=False)
            inserted += len(batch)
        except errors.BulkWriteError as bwe:
            for err in bwe.details['writeErrors']:
                if err['code'] == 11000:
                    skipped += 1
                else:
                    failed += 1
                    failed_docs.append(err)
        batch = []

# Insert remaining
if batch:
    try:
        new_collection.insert_many(batch, ordered=False)
        inserted += len(batch)
    except errors.BulkWriteError as bwe:
        for err in bwe.details['writeErrors']:
            if err['code'] == 11000:
                skipped += 1
            else:
                failed += 1
                failed_docs.append(err)

print(f"✅ Done! Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")