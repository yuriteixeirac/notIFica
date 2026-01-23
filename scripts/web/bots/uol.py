import feedparser, requests
from bs4 import BeautifulSoup
import logging, dotenv, os

dotenv.load_dotenv()

COMUNICA_URL = "http://127.0.0.1:8000/api"
RSS_URL = "https://rss.home.uol.com.br/index.xml"

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)

def get_title(url: str) -> str:
    html = requests.get(url).html
    soup = BeautifulSoup(html, 'html.parser')

    return soup.select_one('h1.title').text


def get_image(section: str) -> str:
    soup = BeautifulSoup(section, 'html.parser')
    return soup.find('img').get('src')


feed = feedparser.parse(RSS_URL)
if feed.status_code != 200:
    exit()

token = requests.post(f"{COMUNICA_URL}/login/", json = {
    "username": os.getenv("MATRICULA"),
    "password": os.getenv("SENHA"),
}).json().get("Token")

for entry in feed.entries:
    if entry is None:
        continue

    link = entry.link
    noticia = {
        "titulo": get_title(),
        "sumario": entry.summary,
        "link": link,
        "imagem": get_image(link),
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
        logger.error(f"STATUS CODE {result.status_code} PARA {entry.link}.")
