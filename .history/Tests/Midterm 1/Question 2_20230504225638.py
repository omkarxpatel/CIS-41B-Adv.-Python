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
        # Implement sorting by a specific column using the `sorted` function
        return GasConcentrationData(sorted(self.data, key=lambda d: getattr(d, column)))

    def search_by_gas(self, gas):
        # Implement searching for a specific gas by filtering the data
        return GasConcentrationData([d for d in self.data if d.gas.lower() == gas.lower()])
