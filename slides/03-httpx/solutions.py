import pathlib

import httpx

# On va travailler dans un dossier que mon dépôt git ignore, pour ne pas polluer le repo évidemment
# vous pouvez faire comme vous voulez et télécharger les fichiers ailleurs (ça ne concerne que les
# questions où on écrit dans des fichiers avec `open(…)`).
pathlib.Path("local").mkdir(exist_ok=True)

# 1
print("=== 1. ===")
print(httpx.get("http://httpbin.org").text)

# 2
print("=== 2. ===")
print(httpx.get("http://httpbin.org/anything").text)

# 3
print("=== 3. ===")
print(httpx.post("http://httpbin.org/anything").text)

# 4
print("=== 4. ===")
print(httpx.get("http://httpbin.org/anything", params={"value": "pandas"}).text)

# 5
print("=== 5. ===")
with open("local/robots.txt", "w") as out_stream:
    response = httpx.get("https://www.google.com/robots.txtt")
    out_stream.write(response.text)

# 6
print("=== 6. ===")
print(httpx.get("http://httpbin.org/anything", headers={"user-agent": "Elephant"}).text)

# 7
print("=== 7. ===")
print(httpx.get("http://httpbin.org/anything").headers)

# 8
print("=== 8. ===")
print(httpx.post("http://httpbin.org/anything", data='{"value": "pandas"}').text)

# 9
print("=== 9. ===")
print(
    httpx.post(
        "http://httpbin.org/anything",
        data='{"value": "pandas"}',
        headers={"content-type": "application/json"},
    ).text
)

# 10
print("=== 10. ===")
print(httpx.get("https://www.google.com", headers={"Accept-Encoding": "gzip"}).text)

# 11
print("=== 11. ===")
with open("local/image.png", "wb") as out_stream:
    response = httpx.get("http://httpbin.org/image", headers={"Accept": "image:png"})
    out_stream.write(response.content)

# 12
print("=== 12. ===")
print(httpx.put("http://httpbin.org/anything").text)

# 13
print("=== 13. ===")
with open("local/image.jpeg", "wb") as out_stream:
    response = httpx.get("http://httpbin.org/image/jpeg")
    out_stream.write(response.content)

# 14
print("=== 14. ===")
auth = httpx.BasicAuth(username="morgan", password="secret")
client = httpx.Client()
response = client.get("http://httpbin.org/anything", auth=auth)
print(response.text)

# 10
print("=== 10. ===")
print(httpx.get("https://duckduckgo.com", headers={"accept-language": "es"}).text)
