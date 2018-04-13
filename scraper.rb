require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new

page = agent.get('https://www.fastenergy.at/heizoelpreis-tendenz.htm')

rows = page.search('#tabelle tbody tr')

rows = rows.map { |row| row.search('> td')  }

rows.each do |columns|
  name, prices, price_difference = columns

  name = name.text.strip
  price_today, price_yesterday = prices.search('div > div').map(&:text).map(&:strip)
  price_difference = price_difference.search('div > div').first.text.strip

  price_per_liter = ->(string) { Float(string.tr("\u0096", "-").tr(' ', '').tr('€', '').strip.tr(',', '.')) / 100.0 }

  id = name.downcase.sub('ä', 'ae').sub('ö', 'oe').sub('ü', 'ue')
  price_today = price_per_liter.(price_today)
  price_yesterday = price_per_liter.(price_yesterday)
  price_difference = price_per_liter.(price_difference)

  ScraperWiki.save_sqlite([:id], {
    id: id,
    name: name,
    price_today: price_today,
    price_yesterday: price_yesterday,
    price_difference: price_difference,
  })
end
