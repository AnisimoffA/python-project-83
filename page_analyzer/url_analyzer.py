from bs4 import BeautifulSoup
import requests

def url_analyze(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    status_code = r.status_code
    h1 = soup.find("h1").text.strip() if soup.find("h1") else None
    title = soup.title.text.strip() if soup.title else None
    description = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else None
    return status_code, h1, title, description


# r = requests.get("https://www.banki.ru/")
# rd = requests.get("https://www.psycopg.org/")

# soup = BeautifulSoup(r.text, "html.parser")
# soup2 = BeautifulSoup(rd.text, "html.parser")

# desc = soup.find("meta", {"name": "description"})["content"]
# desc2 = soup2.find("meta", {"name": "description"})["content"]


# print(desc)
# print("-----")
# print(desc2)

# print(url_analyze("https://www.psycopg.org/"))
