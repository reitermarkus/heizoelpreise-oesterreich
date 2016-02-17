# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.fastenergy.at/heizoelpreis-tendenz.htm")


tablerows = lxml.html.fromstring(html).cssselect(".trend3 tr:not(:first-child)")



def inner_html(self):
  return self.text_content().lstrip().rstrip()


def nicename(self):
  return self.lower().replace(u'ä', 'ae').replace(u'ö', 'oe').replace(u'ü', 'ue')


for row in tablerows:

  name             = inner_html(row.cssselect("td:nth-child(1)")[0])
  price_today      = inner_html(row.cssselect("td:nth-child(2)")[0])
  price_yesterday  = inner_html(row.cssselect("td:nth-child(3)")[0])
  price_difference = inner_html(row.cssselect("td:nth-child(4)")[0])


  scraperwiki.sqlite.save(
    unique_keys=['id'],
    data={
      "id":               nicename(name),
      "name":             name,
      "price_today":      price_today,
      "price_yesterday":  price_yesterday,
      "price_difference": price_difference
    },
    table_name='data'
  )
