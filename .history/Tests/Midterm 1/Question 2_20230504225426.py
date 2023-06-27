from typing import NamedTuple

class GasConcentration(NamedTuple):
    gas: str
    pre_1750: str
    recent: str
    absolute_increase: str
    percentage_increase: str

class GasData:
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return "\n".join([f"{i+1}. {g.gas}: Pre-1750: {g.pre_1750}, Recent: {g.recent}, Absolute increase since 1750: {g.absolute_increase}, Percentage increase since 1750: {g.percentage_increase}" for i, g in enumerate(self.data)])
    
    def __getitem__(self, key):
        return self.data[key]
    
    def sort_by_column(self, column):
        return GasData(sorted(self.data, key=lambda g: getattr(g, column)))
    
    def search_by_gas(self, gas):
        return GasData([g for g in self.data if g.gas.lower() == gas.lower()])
