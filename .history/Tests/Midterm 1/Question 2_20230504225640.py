from collections import namedtuple

GasConcentration = namedtuple('GasConcentration', [
    'gas',
    'pre_1750',
    'recent',
    'absolute_increase',
    'percentage_increase',
])

class GasConcentrationData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '\n'.join(
            f'{d.gas}: {d.pre_1750} -> {d.recent} ({d.absolute_increase}, {d.percentage_increase}%)'
            for d in self.data
        )

    def sort_by_column(self, column):
        return GasConcentrationData(sorted(self.data, key=lambda d: getattr(d, column)))

    def search_by_gas(self, gas):
        return GasConcentrationData([d for d in self.data if d.gas.lower() == gas.lower()])
