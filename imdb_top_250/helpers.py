from money import XMoney, xrates, Money
from decimal import Decimal

#Exchange rates current as of June 8th, 2016
xrates.install('money.exchange.SimpleBackend')
xrates.base = 'USD'
rates = {'UKP': 0.69, 'EUR': 0.88, 'DEM': 1.72, 'FRF': 5.77, 'INR': 66.50, 'AUD': 1.34, 'JPY': 107.07, 'RUR': 63.67}
for k, v in rates.iteritems():
    xrates.setrate(k, Decimal(v))


def money_converter(amount):
    """Returns value in USD
    """
    if amount == None:
        return None
    if amount[0] == '$':
        return amount[1:].replace(',', '')
    if amount[0] == '\xc2': #Pound
        return str(Money(amount[2:].replace(',', ''), 'UKP').to('USD')).replace(',', '')[4:]
    if amount[0] == '\xe2': #Euro
        return str(Money(amount[3:].replace(',', ''), 'EUR').to('USD')).replace(',', '')[4:]
    pre = amount[0:3]
    if pre in rates.keys():
        return str(Money(amount[5:].replace(',', ''), pre).to('USD')).replace(',', '')[4:]
    return amount
