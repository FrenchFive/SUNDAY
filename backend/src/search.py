import json
import urllib.parse
import urllib.request


def web_search(query: str, max_results: int = 3) -> str:
    """Return a short string with search results from DuckDuckGo."""
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote_plus(query)}&format=json"
    try:
        data = json.load(urllib.request.urlopen(url, timeout=10))
    except Exception as ex:
        return f"Search failed: {ex}"

    results = []
    topics = data.get("RelatedTopics", [])
    for topic in topics:
        if isinstance(topic, dict):
            if 'Text' in topic and 'FirstURL' in topic:
                results.append(f"{topic['Text']} - {topic['FirstURL']}")
            if 'Topics' in topic:
                for sub in topic['Topics']:
                    if isinstance(sub, dict) and 'Text' in sub and 'FirstURL' in sub:
                        results.append(f"{sub['Text']} - {sub['FirstURL']}")
                        if len(results) >= max_results:
                            break
        if len(results) >= max_results:
            break
    return "\n".join(results[:max_results])

