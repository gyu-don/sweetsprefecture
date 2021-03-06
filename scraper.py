#!/usr/bin/python3

import re
from util_scraper import *


with UpdateLogger("shoplist.json") as logger:
    def scraping(name, url, *args, **kwargs):
        print('Scraping {0}\n    {1}'.format(name, url))
        status, is_updated, jsonpath, d = do_scraping(name, url, *args, **kwargs)
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
                if words_filter(it.dt, ("ベルギー", "Belgium", "Bruxelles"))),
            lambda bs: (it.dd for it in bs
                if words_filter(it.dt, ("ベルギー", "Belgium", "Bruxelles"))))

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

    scraping("PABLO", "http://www.pablo3.com/shop/",
            lambda bs: bs,
            lambda bs: (x for x in bs.find_all("div", class_="section01_box_title")
                if words_filter(x, ("韓国", "ソウル", "台北"))),
            lambda bs: (x for x in bs.find_all("div", class_="section01_box_address")
                if words_filter(x, ("韓国", "ソウル", "台北"))),
            address_postfilter=lambda s:re.sub(r"\[email.*\*\/", "", s))

    scraping("クラブハリエ", "http://clubharie.jp/corporate/shoplist/index.html",
            lambda bs: bs,
            lambda bs: (plain_text(x.contents[0])
                    for x in bs.findAll("h2", class_="")),
            lambda bs: (plain_text(x.p.contents[1])
                    for x in bs.findAll("section", class_="adress")))

    scraping("マールブランシュ", "http://www.malebranche.co.jp/shop/shopinfo.php",
            lambda bs: bs,
            lambda bs: bs.findAll("strong"),
            lambda bs: (x.dd for x in bs.findAll("dl")))

    scraping("資生堂パーラー", ["http://parlour.shiseido.co.jp/shoplist/",
        "http://parlour.shiseido.co.jp/shoplist/area/kanto/",
        "http://parlour.shiseido.co.jp/shoplist/area/hokkaido_tohoku/",
        "http://parlour.shiseido.co.jp/shoplist/area/chubu/",
        "http://parlour.shiseido.co.jp/shoplist/area/kinki_chugoku_shikoku/",
        "http://parlour.shiseido.co.jp/shoplist/area/kyushu_okinawa/"],
        lambda bs: bs.findAll("div", class_="section-shop")[1],
        lambda bs: bs.findAll("p", class_="font-bold"),
        lambda bs: bs.findAll("p", class_="address"))

    scraping("ピエールマルコリーニ", "http://www.pierremarcolini.jp/shop/",
            lambda bs: bs.find("div", class_="box510"),
            lambda bs: (x for x in bs.find_all("span", class_="b")
                if words_filter(x, ("ハワイ", "International"))),
            lambda bs: bs.find_all("p"),
            exclude_re(r"\(SHOP(\/CAFE)?\)$"),
            exclude_re(r"^.*ADDRESS\n", re.S))

    scraping("キットカット ショコラトリー", "https://nestle.jp/brand/kit/chocolatory/store.html",
            lambda bs: bs.find("div", class_="base"),
            lambda bs: bs.find_all("h3"),
            lambda bs: (x.find_all("p")[1] for x in bs.find_all("div", class_="summary")))

    scraping("ベルアメール", "https://www.belamer.jp/html/user_data/shop.php",
            lambda bs: bs,
            lambda bs: bs.find_all("div", class_="shop_name"),
            lambda bs: bs.find_all("div", class_="shop_info"))

    scraping("デメル", "http://www.demel.co.jp/company/shops.html",
            lambda bs: bs.find_all("tr"),
            lambda bss: (bs.th for bs in bss),
            lambda bss: (bs.find_all("td")[1] for bs in bss))

    scraping("アンテノール", "https://www.antenor.jp/shops/",
            lambda bs: bs,
            lambda bs: bs.find_all(attrs={"data-label": "店名"}),
            lambda bs: bs.find_all(attrs={"data-label": "住所"}))

    scraping("アンリ・シャルパンティエ", "http://www.henri-charpentier.com/shop/",
            lambda bs: bs.find("dl", class_="storeList").find_all("h3"),
            lambda bss: filter(words_filter_f(["デンプシーヒル"]), bss),
            lambda bss: filter(words_filter_f(["Singapore"]),
                    (h3.parent.findNext("li") for h3 in bss)))

    scraping("ヒルバレー", "http://www.hillvalley.jp/shop/",
            lambda bs: bs.find(id="shopArea"),
            lambda bs: bs.find_all("h2"),
            lambda bs: bs.find_all(class_="address"))
