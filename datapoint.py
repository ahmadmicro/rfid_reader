import time

class DataPoint():
    def __init__(self, card, data):
        self.date = None
        self.volume = 0
        self.card = card
        if ':' in data:
            d = data.split(':')
            self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(d[0])))
            self.volume = int(d[1])

    def __str__(self):
        return f'Date:{self.date}, volume:{self.volume}'

    def __repr__(self):
        return f'{{Date:{self.date}, volume:{self.volume}}}'