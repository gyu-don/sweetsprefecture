from util_scraper import *
from pprint import pprint
import re

def p(x):
    pprint(x)
    return x

with UpdateLogger("shoplist.json") as logger:
    def scraping(name, url, *args, **kwargs):
        #pprint([name, url, args, kwargs])
        ret = do_scraping(name, url, *args, **kwargs)
        ret = list(ret)
        pprint(ret)
        ret[1] = True
        logger.append(*ret)

    # --- 以下、add_newsite.sh で書き写される ---
