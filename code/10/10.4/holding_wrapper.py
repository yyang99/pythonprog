# holding.py

class Holding(object):
    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, newprice):
        if not isinstance(newprice, float):
            raise TypeError('Expected float')
        if newprice < 0:
            raise ValueError('Must >= 0')
        self._price = newprice

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, newshares):
        if not isinstance(newshares, int):
            raise TypeError('Expected int')
        self._shares = newshares

    def __setattr__(self, name, value):
        if name not in ('name', 'date', "shares", "price", '_shares', '_price'):
            raise AttributeError(f"No attribute {name}")
        super().__setattr__(name, value)

    def __repr__(self):
        return 'Holding({!r},{!r},{!r},{!r})'.format(self.name, self.date, self.shares, self.price)

    def __str__(self):
        return '{} shares of {} at ${:0.2f}'.format(self.shares, self.name, self.price)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares

import csv

class Portfolio(object):
    def __init__(self):
        self.holdings = []

    @classmethod
    def from_csv(cls, filename):
        self = cls()
        with open(filename, 'r') as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                h = Holding(row[0], row[1], int(row[2]), float(row[3]))
                self.holdings.append(h)
        return self

    def total_cost(self):
        return sum([h.shares * h.price for h in self.holdings])

    def __len__(self):
        return len(self.holdings)

    def __getitem__(self, n):
        if isinstance(n, str):
            return [ h for h in self.holdings if h.name == n ]
        else:
            return self.holdings[n]

    def __iter__(self):
        return self.holdings.__iter__()


def read_portfolio(filename):
    portfolio = []
    with open(filename, 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            h = Holding(row[0], row[1], int(row[2]), float(row[3]))
            portfolio.append(h)
    return portfolio

class ReadOnly:
    def __init__(self, obj):
        self._obj = obj
    def __getattr__(self, attr):
        return getattr(self._obj, attr)
    def __setattr__(self, attr, value):
        if attr == '_obj':
            super().__setattr__(attr, value)
        else:
            raise AttributeError(f"ReadOnly object, attribute {attr} can not be set")

class Portfolio1(Portfolio):
    def __getattr__(self, attr):
        return getattr(self.holdings, attr)

if __name__ == '__main__':
    h = Holding('AA', '2001-01-01', 100, 35.0)
    r = ReadOnly(h)

    portfolio = Portfolio1.from_csv('../../Data/portfolio.csv')
    portfolio.append(h)
