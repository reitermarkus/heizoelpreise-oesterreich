# -*- coding: utf-8 -*-


import os
os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'

import lxml.html
import scraperwiki
import time


def inner_html(row, column):
  return row.cssselect("td:nth-child(%s)" % column)[0].text_content().strip()


def price_per_liter(price):
  return round(float(price.replace(u'€', '').replace(',', '.').strip()) / 100, 4)


start = time.time()


html = scraperwiki.scrape("http://www.fastenergy.at/heizoelpreis-tendenz.htm")

tablerows = lxml.html.fromstring(html).cssselect(".trend3 tr:not(:first-child)")

for row in tablerows:

  name             = inner_html(row, 1)
  price_today      = inner_html(row, 2)
  price_yesterday  = inner_html(row, 3)
  price_difference = inner_html(row, 4)

  scraperwiki.sqlite.save(
    unique_keys=['id'],
    data={
      'id':               name.lower().replace(u'ä', 'ae').replace(u'ö', 'oe').replace(u'ü', 'ue'),
      'name':             name,
      'price_today':      price_per_liter(price_today),
      'price_yesterday':  price_per_liter(price_yesterday),
      'price_difference': price_per_liter(price_difference)
    },
    table_name='data'
  )


end = time.time()

print("\nScraping started at\n  %s,\nended at\n  %s,\nand took\n  %f seconds." % (
  time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(start)),
  time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(end)),
  (end - start)
))
