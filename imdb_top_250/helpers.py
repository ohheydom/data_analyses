from money import XMoney, xrates, Money
from decimal import Decimal

#Exchange rates current as of June 8th, 2016
xrates.install('money.exchange.SimpleBackend')
xrates.base = 'USD'
rates = {'EUR': 0.88}
for k, v in rates.iteritems():
    xrates.setrate(k, Decimal(v))

def money_converter(amount):
    """Returns value in USD
    """
    if amount == None:
        return None
    if amount[0] == '$':
        return int(round(float(amount[1:].replace(',', ''))))
    if amount[0] == '\xe2': #Euro
        return int(round(float(str(Money(amount[3:].replace(',', ''), 'EUR').to('USD')).replace(',', '')[4:])))
    return None
