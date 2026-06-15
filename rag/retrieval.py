from rag.models import DocumentChunk
from pgvector.django import CosineDistance


def retrieve_chunks(query_vector, k=5):
    chunks = DocumentChunk.objects.order_by(
        CosineDistance('embedding', query_vector)
    )[:k]
    return chunks
