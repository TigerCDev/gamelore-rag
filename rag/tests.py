from django.test import TestCase
from games.models import Game
from rag.models import DocumentChunk
from rag.retrieval import retrieve_chunks
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

from rag.router import classify_question



class TestRouter(TestCase):
    """Test Factual Section"""
    def test_factual_question(self):
        self.assertEqual(classify_question('who made Expedition 33'), 'factual')

    def test_when_is_factual(self):
        self.assertEqual(classify_question('when was God if War released'), 'factual')

    def test_how_old(self):
        self.assertEqual(classify_question('how old is Kratos in God of War'), 'factual')

    def test_who_voice(self):
        self.assertEqual(classify_question('who voice Joel in The Last of Us'), 'factual')

    def test_copies_sold(self):
        self.assertEqual(classify_question('how many copies Uncharted 4 have sold'), 'factual')

    """"Test Narrative Section"""
    def test_narrative_question(self):
        self.assertEqual(classify_question('what is the narrative theme of Expedition 33'), 'narrative')

    def test_how_does_is_narrative(self):
        self.assertEqual(classify_question('how does the combat reflect the story'), 'narrative')

    def test_what_award(self):
        self.assertEqual(classify_question('what award did God of War won'), 'narrative')

    def test_narrative_character_motivation(self):
        self.assertEqual(classify_question('explain the relationship between Arthur Morgan and Dutch in RDR2'), 'narrative')

    def test_why_character_does_that(self):
        self.assertEqual(classify_question(
            'why Joel chose to bring Ellie out of the Firefly camp at the end instead of letting them finding a cure'), 'narrative'
            )


class TestAskEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ask_required_questions(self):
        response = self.client.post('/api/v1/ask/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    @patch('rag.views.ChatGroq')
    @patch('rag.views.OpenAIEmbeddings')
    def test_ask_narrative_returns_answer(self, mock_embeddings, mock_llm):
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 1536
        mock_llm.return_value.invoke.return_value = MagicMock(content='Test answer')

        response = self.client.post('/api/v1/ask/',
            {'question': 'how does the story make you feel'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.data)
        self.assertIn('question_type', response.data)


class TestRetrieval(TestCase):
    def test_retrieve_chunks_returns_results(self):
        game = Game.objects.create(
            title='Test Game',
            release_year=2024,
            synopsis='A test game',
            engine='Test engine',
        )

        DocumentChunk.objects.create(
            content='This is a test chunk about narrative themes',
            embedding=[0.1] * 1536,
            source_url='https://example.com',
            source_type='essay',
            game=game
        )

        results = retrieve_chunks([0.1] * 1536)
        self.assertGreater(len(results), 0)


class TestEdgeCases(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_empty_question_returns_400(self):
        response = self.client.post('/api/v1/ask/', {'question': ''}, format='json')
        self.assertEqual(response.status_code, 400)