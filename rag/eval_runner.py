import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from rag.eval import EVAL_QUESTIONS
from rag.retrieval import retrieve_chunks
from langchain_openai import OpenAIEmbeddings



def score_retrieval(chunks, expected_answer):
    """Check if retrieved chunks contain keywords from the expected answer."""
    expected_words = set(expected_answer.lower().split())
    chunk_text = ' '.join([c.content.lower() for c in chunks])
    matches = [w for w in expected_words if w in chunk_text]
    return len(matches) / len(expected_words)


def score_answer(actual_answer, expected_answer):
    """Keyword overlap between actual and expected answer."""
    expected_words = set(expected_answer.lower().split())
    actual_words = set(actual_answer.lower().split())
    matches = expected_words & actual_words
    return len(matches) / len(expected_words)


def run_eval():
    embeddings = OpenAIEmbeddings()
    results = []

    for item in EVAL_QUESTIONS:
        question = item['question']
        expected = item['expected_answer']
        game = item['game']

        query_vector = embeddings.embed_query(question)
        chunks = retrieve_chunks(query_vector, k=5)
        retrieval_score = score_retrieval(chunks, expected)

        results.append({
            'question': question,
            'game': game,
            'retrieval_score': retrieval_score,
            'top_chunk': chunks[0].content[:150] if chunks else 'NO CHUNKS FOUND',
        })

        print(f"\nQ: {question}")
        print(f"Game: {game}")
        print(f"Retrieval score: {retrieval_score:.2f}")
        print(f"Top chunk: {chunks[0].content[:150] if chunks else 'NONE'}")
        print("-" * 60)

    avg_score = sum(r['retrieval_score'] for r in results) / len(results)
    print(f"\n{'='*60}")
    print(f"BASELINE RETRIEVAL SCORE: {avg_score:.2f}")
    print(f"Questions evaluated: {len(results)}")
    print(f"{'='*60}")

    return avg_score



if __name__ == '__main__':
    run_eval()
