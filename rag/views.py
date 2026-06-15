from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rag.retrieval import retrieve_chunks
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq



class AskView(APIView):
    def post(self, request):
        question = request.data.get('question')

        if not question:
            return Response(
                {'error': 'question is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        embeddings = OpenAIEmbeddings()
        query_vector = embeddings.embed_query(question)

        chunks = retrieve_chunks(query_vector)

        context = '\n\n'.join([chunk.content for chunk in chunks])

        prompt = f"""You are a game knowledge assistant. Answer the question based on the context provided.
                    If the answer is not in the context, say so.

                    Context:
                        {context}

                    Question: {question}

                    Answer:"""

        llm = ChatGroq(model="llama-3.1-8b-instant")
        answer = llm.invoke(prompt)

        sources = [{'url': chunk.source_url, 'type': chunk.source_type} for chunk in chunks]

        return Response({
            'answer': answer.content,
            'source': sources,
        })
