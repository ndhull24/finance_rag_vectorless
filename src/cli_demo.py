from src.retrieve import search

def main():
    print("Finance RAG Phase 1 - CLI demo")
    print("Type a question about your finance documents, and I'll try to find relevant sections for you. Empty to exit")

    while True:
        q = input("Question: ").strip()
        if not q:
            print("Goodbye!")
            break

        hits = search(q, k=8)

        # Group results by section_path
        grouped = {}
        for text, meta in hits:
            key = (meta["doc_name"], meta["section_path"])
            grouped.setdefault(key, []).append(text)

        print("\nRelevant sections:")
        for (doc_name, section_path), texts in list(grouped.items())[:3]:
            print(f"\n  [{doc_name}] {section_path}")
            for t in texts[:2]:
                snippet = t[:350].replace("\n", " ")
                print(f"    • {snippet}{'...' if len(t) > 350 else ''}")

if __name__ == "__main__":
    main()