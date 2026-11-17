import json
import subprocess
import sys
from urllib.parse import quote


def web_search(query: str) -> list[dict]:
    encoded_query = quote(query)
    url = (
        "https://fi.wikipedia.org/w/api.php"
        f"?action=opensearch&search={encoded_query}&format=json"
    )
    result = subprocess.run(
        ["curl", "--max-time", "10", url],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list) or len(data) < 4:
        return []
    titles = data[1]
    urls = data[3]
    results: list[dict] = []
    for title, link in zip(titles, urls):
        results.append({"title": title, "url": link})
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Käyttö: python web_search.py <hakusana>")
        sys.exit(1)
    results = web_search(sys.argv[1])
    for item in results:
        print(f"{item['title']}: {item['url']}")
