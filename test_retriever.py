from retriever import retrieve

query = "leave policy"

docs = retrieve(query)

print(f"\nResults for: {query}\n")

for i, d in enumerate(docs, 1):
    print(f"Result {i}:")
    print(d.page_content)
    print(d.metadata)
    print("-----")