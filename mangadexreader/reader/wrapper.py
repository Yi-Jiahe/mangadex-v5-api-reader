import requests
import json
import io
from PIL import Image

base_url = "https://api.mangadex.org"


def get_tags():
    url = f"{base_url}/manga/tag"
    r = requests.get(url)
    res = json.loads(r.content.decode('utf-8'))
    print(res)
    inverted_comma = '\''
    with open("tags.py", "w") as f:
        f.write("tags = {\n")
        for result in res:
            data = result["data"]
            f.write(f"\t'{data['attributes']['name']['en'].replace(inverted_comma, '')}': '{data['id']}',\n")
        f.write("}")


def get_manga_list(params):
    url = f"{base_url}/manga"
    r = requests.get(url, params=params)
    print(r.url)
    res = json.loads(r.content.decode('utf-8'))
    if r.status_code == 400:
        for error in res["errors"]:
            print(f"{error['title']}: {error['detail']}")
        return
    if r.status_code == 200:
        results = res["results"]
        ret = list()
        for result in results:
            data = result["data"]
            ret.append({
                'id': data["id"],
                'title': data["attributes"]["title"]["en"],
                'tags': [tag["attributes"]["name"]["en"] for tag in data["attributes"]["tags"]]
            })
        return ret
#             print(f"""
# {data["id"]}
# {data["attributes"]["title"]["en"]}
# {', '.join([tag["attributes"]["name"]["en"] for tag in data["attributes"]["tags"]])}
# """)


def get_manga(manga_id):
    url = f"{base_url}/manga/{manga_id}"
    r = requests.get(url)
    res = json.loads(r.content.decode('utf-8'))
    if r.status_code == 403:
        for error in res["errors"]:
            print(f"{error['title']}: {error['detail']}")
        return
    if r.status_code == 404:
        print("404 Manga no content")
        return
    if r.status_code == 200:
        data = res["data"]
        return {
            'title': data["attributes"]["title"]["en"],
            'description': data["attributes"]["description"]["en"]
        }


def get_manga_chapters(manga_id, limit=10, offset=0):
    url = f"{base_url}/chapter"
    params = {
        "limit": limit,
        "offset": offset,
        "manga": manga_id,
    }
    r = requests.get(url, params=params)
    res = json.loads(r.content.decode('utf-8'))
    results = res["results"]

    ret = {
        "total": res["total"],
        "chapters": list()
    }
    for result in results:
        data = result["data"]
        ret["chapters"].append({
            'id': data["id"],
            'volume': data["attributes"]["volume"],
            'chapter': data["attributes"]["chapter"],
            'title': data["attributes"]["title"]
        })
        # hash = data["attributes"]["hash"]
        # pages = data["attributes"]["data"]
        # pages_data_saver = data["attributes"]["dataSaver"]
#         print(f"""
# {data["id"]}
# Volume {data["attributes"]["volume"]}, chapter {data["attributes"]["chapter"]}
# {data["attributes"]["title"]}
# {hash},
# {pages}
#         """)
    return ret


def get_chapter(chapter_id):
    url = f"{base_url}/chapter/{chapter_id}"
    r = requests.get(url)
    result = json.loads(r.content.decode('utf-8'))
    data = result["data"]
    related_manga = next(e for e in result["relationships"] if e["type"] == "manga")
    print(related_manga)
    return {
        'hash': data["attributes"]["hash"],
        'data': data["attributes"]["data"],
        'dataSaver': data["attributes"]["dataSaver"],
        'mangaID': related_manga["id"],
    }
#     hash = data["attributes"]["hash"]
#     pages = data["attributes"]["data"]
#     pages_data_saver = data["attributes"]["dataSaver"]
#     print(f"""
# {data["id"]}
# Volume {data["attributes"]["volume"]}, chapter {data["attributes"]["chapter"]}
# {data["attributes"]["title"]}
# {hash},
# {pages}
#     """)


def get_mangadexahome_server_url(chapter_id):
    url = f"{base_url}/at-home/server/{chapter_id}"
    r = requests.get(url)
    res = json.loads(r.content.decode('utf-8'))
    return res["baseUrl"]


def get_page(server_base_url, chapter_hash, filename, quality_mode="data"):
    url = f"{server_base_url}/{quality_mode}/{chapter_hash}/{filename}"
    print(url)
    r = requests.get(url)
    res = r.content
    im = Image.open(io.BytesIO(res))
    im.show()


if __name__ == "__main__":
    get_tags()
    # get_manga({
    #     "title": "kobayashi's dragon maid"
    # })
    # get_manga_chapters("bd6d0982-0091-4945-ad70-c028ed3c0917")
    # print(get_chapter("3fb32d7f-8cbd-4b9e-95ad-c075e7ded472"))
    # print(get_mangadexahome_server_url("3fb32d7f-8cbd-4b9e-95ad-c075e7ded472"))
    # get_page(
    #     "https://tv6pyvncy3qb6.apttrvtvrt9zm.mangadex.network:443/zXImry2DA3BNgrS-BJ9rke4Mxb2MIj9CrnZFH_A4f9SzgN8KZ8ZGV69Mn4Wl2WRr4vLGuD6pUNudTtGhsRiZ5rnQ8B1bS9T4XRewb-vfTQr6JRwvclC0Js0vgL5ZZgd7OP8mj7Sn4YN3-_FdJTQMrsKs8Rysh70NDoc34WGi97nIe05GbYyMNHmFDQYxAeZD",
    #     "ae0ca57297808007fcd64a57f2d00057",
    #     "p1-1d1400c0c1dda5967cd1da2f05f029bbb1a54dda9c4df67b05439ed25b472eab.jpg"
    #     )
    pass
