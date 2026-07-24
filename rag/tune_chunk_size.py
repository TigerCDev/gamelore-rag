import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from rag.models import DocumentChunk
from rag.ingestion import ingest_url, ingest_youtube
from rag.eval_runner import run_eval

# (source_url_or_video_id, game_id, source_type, is_youtube)
SOURCES = [
    ('https://en.wikipedia.org/wiki/Clair_Obscur:_Expedition_33', 1, 'essay', False),
    ('OsO3A5tsyW4', 1, 'interview', True),
    ('https://en.wikipedia.org/wiki/God_of_War_(2018_video_game)', 3, 'essay', False),
    ('o-vC1tOzE1Q', 3, 'interview', True),
    ('https://en.wikipedia.org/wiki/The_Last_of_Us_(video_game)', 14, 'essay', False),
    ('y3PODFMAt_w', 14, 'interview', True),
]


def reingest_all(chunk_size):
    DocumentChunk.objects.filter(game_id__in=[1, 3, 14]).delete()
    for source, game_id, source_type, is_youtube in SOURCES:
        print(f"  ingesting {source} @ chunk_size={chunk_size}")
        if is_youtube:
            ingest_youtube(source, game_id, source_type, chunk_size=chunk_size)
        else:
            ingest_url(source, game_id, source_type, chunk_size=chunk_size)


if __name__ == '__main__':
    results = {}
    for size in [256, 512, 1024]:
        print(f"\n{'='*60}\nCHUNK SIZE: {size}\n{'='*60}")
        reingest_all(size)
        score = run_eval(k=8, verbose=False)
        results[size] = score

    print(f"\n{'='*60}")
    print("CHUNK SIZE TUNING SUMMARY")
    for size, score in results.items():
        print(f"  chunk_size={size}: {score:.2f}")
    print(f"{'='*60}")