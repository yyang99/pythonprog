# holding.py
class Typed:
    type_name: object

    def __init__(self, name, validator=None):
        self.name = name
        self.validator = validator

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type_name):
            raise TypeError(f"value {value} is not a {self.type_name.__name__}")
        if self.validator:
            self.validator(value)
        instance.__dict__[self.name] = value

def no_nagative(value):
    if value <= 0:
        raise ValueError(f"vlaue {value} is native")

class Float(Typed):
    type_name = float

class Integer(Typed):
    type_name = int

class Holding(object):
    shares = Integer('shares')
    price = Float('price', no_nagative)

    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price

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

    def __getattr__(self, name):
        return getattr(self.holdings, name)

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

if __name__ == '__main__':
    portfolio = read_portfolio('../../Data/portfolio.csv')
    h = Holding('AA', '2001-01-01', 100, 35.0)
