from util_scraper import *
from pprint import pprint


with UpdateLogger("shoplist.json") as logger:
    def scraping(name, url, f1, f2, f3):
        ret = do_scraping(name, url, f1, f2, f3)
        ret = list(ret)
        ret[1] = True
        logger(*ret)
        pprint(ret)

    # --- 以下、add_newsite.sh で書き写される ---
