import feedparser, requests
from bs4 import BeautifulSoup
import logging, dotenv, os


COMUNICA_URL = "http://localhost:8000/api"
METROPOLES_URL = "https://metropoleonline.com.br/rss/latest-posts"

dotenv.load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)


def get_imagem(url: str) -> str:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    imagem = soup.select_one("img.img-fluid.center-image")
    return imagem.get("src")


feed = feedparser.parse(METROPOLES_URL)
if feed.status != 200:
    exit()

token = requests.post(f"{COMUNICA_URL}/login/", json = {
    "username": os.getenv("MATRICULA"),
    "password": os.getenv("SENHA"),
}).json().get("Token")

for news in feed.entries:
    link = news.link
    noticia = {
        "titulo": news.title,
        "sumario": news.summary + '.',
        "link": link,
        "imagem": get_imagem(link),
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
            