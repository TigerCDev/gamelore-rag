from celery import shared_task
from rag.ingestion import ingest_url, ingest_youtube



@shared_task
def ingest_url_task(url, game_id, source_type):
    ingest_url(url, game_id, source_type)
    return f'Ingested {url}'


@shared_task
def ingest_youtube_task(video_id, game_id, source_type):
    ingest_youtube(video_id, game_id, source_type)
    return f'Ingested youtube: {video_id}'
