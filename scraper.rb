require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new

page = agent.get('https://www.fastenergy.at/heizoelpreis-tendenz.htm')

rows = page.search('.trend3 tr:not(:first-child)')

rows = rows.map { |row| row.search('> td') }

rows.each do |row|
  columns = row.children.reject { |column| column.content.match?(/\A[[:space:]]+\Z/) }
             .map { |column| column.content.strip }

  name, price_today, price_yesterday, price_difference = columns

  price_per_liter = ->(string) { Float(string.tr('€', '').strip.tr(',', '.')) / 100.0 }

  name = columns[0]
  id = name.downcase.sub('ä', 'ae').sub('ö', 'oe').sub('ü', 'ue')
  price_today = price_per_liter.(columns[1])
  price_yesterday = price_per_liter.(columns[2])
  price_difference = price_per_liter.(columns[3])

  ScraperWiki.save_sqlite([:id], {
    id: id,
    name: name,
    price_today: price_today,
    price_yesterday: price_yesterday,
    price_difference: price_difference,
  })
end
