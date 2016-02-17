# -*- coding: utf-8 -*-

import os

os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'

import scraperwiki
import lxml.html


def inner_html(html):
  return html.text_content().strip()


def nicename(name):
  return name.lower().replace(u'ä', 'ae').replace(u'ö', 'oe').replace(u'ü', 'ue')


def price_per_liter(price):
  return round(float(price.replace(u'€', '').replace(',', '.').strip()) / 100, 4)


html = scraperwiki.scrape("http://www.fastenergy.at/heizoelpreis-tendenz.htm")

tablerows = lxml.html.fromstring(html).cssselect(".trend3 tr:not(:first-child)")


for row in tablerows:

  name             = inner_html(row.cssselect("td:nth-child(1)")[0])
  price_today      = inner_html(row.cssselect("td:nth-child(2)")[0])
  price_yesterday  = inner_html(row.cssselect("td:nth-child(3)")[0])
  price_difference = inner_html(row.cssselect("td:nth-child(4)")[0])

  scraperwiki.sqlite.save(
    unique_keys=['id'],
    data={
      'id':               nicename(name),
      'name':             name,
      'price_today':      price_per_liter(price_today),
      'price_yesterday':  price_per_liter(price_yesterday),
      'price_difference': price_per_liter(price_difference)
    },
    table_name='data'
  )
