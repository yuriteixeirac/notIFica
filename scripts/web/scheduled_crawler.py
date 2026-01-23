import requests
import subprocess, os

CURRENT_CRAWLERS = [
    'cnn.py', 'g1.py', 'metropoles.py', 'uol.py'
]

healthcheck = requests.get("http://localhost:8000/api/healthcheck/")

if healthcheck.status_code != 200:
    exit()

for file in os.listdir():
    if file in CURRENT_CRAWLERS:
        subprocess.run(['python3', f'bots/{file}'])
