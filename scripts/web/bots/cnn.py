import feedparser, requests
from bs4 import BeautifulSoup
import logging, dotenv, os

dotenv.load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)

COMUNICA_URL = "http://127.0.0.1:8000/api"
RSS_URL = "https://admin.cnnbrasil.com.br/feed/"

def get_imagem(url: str) -> str:
    """Recebe uma notícia e retorna a URL para a imagem de capa da notícia."""
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    imagem = soup.select('img.flex.size-full.object-cover')[2]
    return imagem.get("src")


feed = feedparser.parse(RSS_URL)

if feed.status != 200:
    raise requests.exceptions.HTTPError()

token = requests.post(f"{COMUNICA_URL}/login/", json = {
    "username": os.getenv("MATRICULA"),
    "password": os.getenv("SENHA"),
}).json().get("Token")

for news in feed.entries:
    noticia = {
        "titulo": news.title,
        "sumario": news.summary + '.',
        "link": news.link,
        "imagem": get_imagem(news.link),
        "em_display": True,
        "automatizada": True
    }

    result = requests.post(
        f"{COMUNICA_URL}/noticia/",
        json = noticia, headers = {
            "Authorization": f"Token {token}"
        }
    )

    if result.status_code != 201:
        logger.error(f"STATUS CODE {result.status_code} PARA {news.link}.")
