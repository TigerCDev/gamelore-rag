from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from rag.models import DocumentChunk
from youtube_transcript_api import YouTubeTranscriptApi

import requests


def fetch_text(url):
    headers = {
        'User-Agent': 'gamelore-rag/1.0 (https://github.com/TigerCDev/gamelore-rag; educational project)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def embed_chunks(chunks):
    embeddings = OpenAIEmbeddings()
    vectors = embeddings.embed_documents(chunks)
    return vectors


def store_chunks(chunks, vectors, game_id, source_url, source_type):
    for chunk, vector in zip(chunks, vectors):
        DocumentChunk.objects.create(
            content=chunk,
            embedding=vector,
            source_url=source_url,
            source_type=source_type,
            game_id=game_id,
        )


def ingest_url(url, game_id, source_type):
    text = fetch_text(url)
    chunks = chunk_text(text)
    vector = embed_chunks(chunks)
    store_chunks(chunks, vector, game_id, url, source_type)

# --- Youtube section --- #

def fetch_youtube_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    text = ' '.join([item.text for item in transcript])
    return text

def ingest_youtube(video_id, game_id, source_type):
    text = fetch_youtube_transcript(video_id)
    chunks = chunk_text(text)
    vector = embed_chunks(chunks)
    store_chunks(chunks, vector, game_id, f'https://www.youtube.com/watch?v={video_id}', source_type)
