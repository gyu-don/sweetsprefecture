from util_scraper import *
from pprint import pprint
import re


with UpdateLogger("shoplist.json") as logger:
    def scraping(name, url, *args, **kwargs):
        #pprint([name, url, args, kwargs])
        ret = do_scraping(name, url, *args, **kwargs)
        ret = list(ret)
        ret[1] = True
        logger.append(*ret)
        pprint(ret)

    # --- 以下、add_newsite.sh で書き写される ---
