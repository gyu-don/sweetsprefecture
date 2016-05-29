#!/usr/bin/python3

from util_scraper import *


with UpdateLogger("shoplist.json") as logger:
    def scraping(name, url, *args):
        print('Scraping {0}\n    {1}'.format(name, url))
        status, is_updated, jsonpath, d = do_scraping(name, url, *args)
        print(status, "\t", "Updated" if is_updated else "Not modified")
        logger.append(status, is_updated, jsonpath, d)
        return d

    scraping('銀のぶどう', 'http://www.ginnobudo.jp/index.html',
            lambda bs: bs.find('section', id='shoplist'),
            lambda bs: bs.find_all('div', class_='name'),
            lambda bs: bs.find_all('div', class_='address'))
    
    scraping('新宿高野', 'http://takano.jp/takano/shop/',
            lambda bs: bs.find('ul', class_='shoplist'),
            lambda bs: bs.find_all('h2'),
            lambda bs: bs.find_all('div', class_='address'))

    scraping('ねんりん家', 'http://www.nenrinya.jp/shop/index.html',
            lambda bs: bs.find('div', id='main'),
            lambda bs: bs.find_all('p', class_='close'),
            lambda bs: (footer.p for footer in bs.find_all('div', class_='footer')))

    scraping('FOUNDRY', 'http://www.foundry-karuizawa.com/brand/info/',
            lambda bs: bs.find('div', id='inner_wrapper'),
            lambda bs: bs.find_all('h3', id={'map_ttl', 'map_ttl2'}),
            lambda bs: bs.find_all('address'))

    scraping('治一郎', 'http://www.jiichiro.com/shop/',
            lambda bs: bs.find_all('div', class_='shop'),
            lambda bs: (t.strong for t in bs),
            lambda bs: (t.ul.li for t in bs))

    scraping('ARDEUR', 'http://www.ardeur-hakata.jp/user_data/shop_list.php',
            lambda bs: bs.find(id='shop_text'),
            lambda bs: bs.find_all(class_='shop_name'),
            lambda bs: bs.find_all(class_='L_shop'))

    scraping('Quatre', 'http://www.quatre.co.jp/shop/index.html',
            lambda bs: [x for x in bs.find_all('table', class_='shop') if x.table],
            lambda bs: (t.td for t in bs),
            lambda bs: (t.table for t in bs))

    scraping('irina', 'http://www.irina-irina.com/category/shop/',
            lambda bs: bs.find_all(class_='shop-txt'),
            lambda bs: (t.h2 for t in bs),
            lambda bs: bs)

    scraping('strasbourg', 'http://stras.jp/shop/',
            lambda bs: bs.find_all('div', class_='txt'),
            lambda bs: (t.h4 for t in bs),
            lambda bs: (t.find('p', class_='address') for t in bs))

    scraping('Pavlov', 'http://www.pavlov.jp/shop/',
            lambda bs: bs.find_all('div', class_='contents-inner'),
            lambda bs: (t.h2 for t in bs),
            lambda bs: (t.dd for t in bs))

    scraping("ヴィタメール", "https://www.wittamer.jp/shops/",
            lambda bs: bs.find_all("dl"),
            lambda bs: (it.dt for it in bs
                if excluded_words(it.dt, ("ベルギー", "Belgium", "Bruxelles"))),
            lambda bs: (it.dd for it in bs
                if excluded_words(it.dt, ("ベルギー", "Belgium", "Bruxelles"))))

    scraping("ヨックモック", ["http://www.yokumoku.co.jp/store/district01.html",
                    "http://www.yokumoku.co.jp/store/district02.html",
                    "http://www.yokumoku.co.jp/store/district03.html",
                    "http://www.yokumoku.co.jp/store/district04.html",
                    "http://www.yokumoku.co.jp/store/district05.html",
                    "http://www.yokumoku.co.jp/store/district06.html",
                    "http://www.yokumoku.co.jp/store/district07.html"],
            lambda bs: [bs for bs in (tr.find_all("td") for tr in bs.find_all("tr")) if len(bs)>2],
            lambda bs: (a[0] for a in bs),
            lambda bs: (a[1] for a in bs))

    scraping("ケーニヒスクローネ", "http://konigs-krone.co.jp/?page_id=75",
            lambda bs: bs.find("article", class_="product"),
            lambda bs: bs.find_all("h3"),
            lambda bs: (tab.find_all("td")[1] for tab in bs.find_all("table")))

    scraping("ガトーフェスタハラダ", "http://www.gateaufesta-harada.com/store",
            lambda bs: bs,
            lambda bs: bs.find_all("h4"),
            lambda bs: bs.find_all("span", class_="loc"))
