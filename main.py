import json
from provider import MangaProvider

manga_provider = MangaProvider()

search_result = manga_provider.search_manga("hypnosis")

with open("result.json", "w") as f:
    f.write(json.dumps(search_result, indent=4))
