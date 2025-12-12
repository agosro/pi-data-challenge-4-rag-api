from services.embeddings import embed_query
from services.vectorstore import query_similar_chunks

def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    query_vec = embed_query(query)
    results = query_similar_chunks(query_vec, top_k)

    output = []
    for i in range(len(results["ids"][0])):
        distance = float(results["distances"][0][i])
        similarity_score = max(0.0, min(1.0, 1.0 - distance))

        output.append({
            "document_id": results["metadatas"][0][i]["doc_id"],
            "title": results["metadatas"][0][i]["title"],
            "content_snippet": results["documents"][0][i][:150] + "...",
            "similarity_score": similarity_score
        })

    return output
