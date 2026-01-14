import os
from dotenv import load_dotenv

load_dotenv(".env")
PROXY = os.environ.get("PROXY")
PROXIES = {
    'http': PROXY,
    'https': PROXY,
}
TIMEOUT=60
URL_BROWSER= 'https://www.dnrec.jus.gov.ar/MasBuscados/'

HEADER_BROWSER= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://github.com/Fer-Mig-Agus/mas_buscados_crawler',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'IDNODO=.cluster3',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

HEADER_PAGE={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'IDNODO=.cluster3',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0, i',
}

