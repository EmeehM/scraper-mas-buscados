import crawler
from logger import get_logger
logger = get_logger(__name__)

def main():
    logger.info('Start crawling...')
    crawler.Crawler().crawl()
    logger.info('End crawling..')

if __name__ == '__main__':
    main()


