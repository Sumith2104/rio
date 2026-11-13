import chromadb
try:
    client = chromadb.HttpClient(host="localhost", port=8001)
    colls = client.list_collections()
    print("ChromaDB Collections on Port 8001:")
    for c in colls:
        print(" -", c.name, "(count:", c.count(), ")")
except Exception as e:
    print("Error checking ChromaDB:", e)

