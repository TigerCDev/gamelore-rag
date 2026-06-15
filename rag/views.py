from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rag.retrieval import retrieve_chunks
from rag.router import classify_question

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

        question_type = classify_question(question)

        # -- Factual question -- #
        if question_type == 'factual':
            from games.models import Game

            words = [w for w in question.split() if len(w) > 3]
            from django.db.models import Q
            query = Q()
            for word in words:
                query |= Q(title__icontains=word)

            matched_games = Game.objects.filter(query).values('title', 'release_year', 'synopsis', 'engine')


            return Response({
                'answer': list(matched_games),
                'source': 'structured_database',
                'question_type': 'factual',
            })

        # -- Narrative question -- #

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
            'question_type': 'narrative',
        })
