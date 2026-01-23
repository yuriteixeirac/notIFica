from bs4 import BeautifulSoup
import feedparser, dotenv
import requests, logging, os

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)

COMUNICA_URL = "http://localhost:8000/api"
RSS_URL = "https://g1.globo.com/rss/g1/"


def get_imagem(entry: dict[str]):
    imagem = noticia.get("media_content", "")
    if imagem:
        return imagem[0].get("url")


dotenv.load_dotenv()

feed = feedparser.parse(RSS_URL)
if feed.status != 200:
    exit()

token = requests.post(f"{COMUNICA_URL}/login/", json={
    "username": os.getenv("MATRICULA"),
    "password": os.getenv("SENHA")
}).json().get("Token")

for news in feed.entries:
    noticia = {
        "titulo": news.title,
        "sumario": news.get("subtitle", ''),
        "link": news.link,
        "em_display": True,
        "imagem": get_imagem(news),
        "automatizada": True
    }

    result = requests.post(
        f"{COMUNICA_URL}/noticia/",
        json=noticia, headers={
            "Authorization": f"Token {token}"
        }
    )

    if result.status_code != 201:
        logging.error(f"STATUS CODE {result.status_code} PARA {news.link}.")
