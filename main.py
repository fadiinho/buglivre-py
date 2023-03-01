from provider import MangaProvider

manga_provider = MangaProvider()

search_result = manga_provider.search_manga("martial peak")

id = 7302
page = 1
chapters = manga_provider.get_chapters(id, page)

release_id = 445082
pages = manga_provider.get_pages(release_id)
