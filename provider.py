import requests
import json


class MangaException(Exception):
    def __init__(self, status_code: int, reason: str) -> None:
        super().__init__(reason)
        self.status_code = status_code


class MangaProvider:
    def __init__(self):
        self._base_url = "https://mangalivre.net"
        self._search_path = "/lib/search/series.json"
        self._chapters_path = "/series/chapters_list.json?page={page}&id_serie={id}"
        self._pages_path = "/leitor/pages/{release_id}.json"

        self._headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "pt-BR",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.62 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "content-type": "application/x-www-form-urlencoded",
        }

    def search_manga(self, search: str):
        """Search for a manga"""
        response = requests.post(
            f"{self._base_url}{self._search_path}",
            headers=self._headers,
            data=f"search={search}",
        )

        if not response.ok:
            raise MangaException(response.status_code, response.reason)

        json_response = response.json()

        if not json_response["series"]:
            raise MangaException(404, "Manga not found")

        return json_response

    def get_chapters(self, id: int, page: int):
        """Returns the chapters of a manga"""
        response = requests.get(
            f"{self._base_url}{self._chapters_path.format(id = id, page=page)}",
            headers=self._headers,
        )

        json_response = response.json()

        if not response.ok:
            raise MangaException(response.status_code, response.reason)

        json_response = response.json()

        if not json_response["chapters"]:
            raise MangaException(404, "Manga not found")

        return json_response

    def get_pages(self, release_id: int):
        """Returns the pages of a manga"""
        headers = self._headers.copy()

        headers.update({"content-type": "application/json"})

        response = requests.get(
            f"{self._base_url}{self._pages_path.format(release_id=release_id)}",
            headers=self._headers,
        )

        json_response = response.json()

        if len(json_response["images"]) == 0:
            raise MangaException(404, "Pages not found")

        with open("test.json", "w") as f:
            f.write(json.dumps(json_response, indent=4))

        return json_response
