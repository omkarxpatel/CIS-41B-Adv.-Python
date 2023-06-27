from typing import NamedTuple


class GreenhouseGasData(NamedTuple):
    Gas: str
    Pre_1750: float
    Recent: float
    Absolute_increase_since_1750: float
    Percentage_increase_since_1750: float


class GreenhouseGasCollection:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def sort_by(self, column):
        if column not in GreenhouseGasData._fields:
            raise ValueError(f"{column} not found in {GreenhouseGasData._fields}")
        # self.data = sorted(self.data, key=lambda x: x[column])
        self.data = sorted(self.data, key=lambda x: getattr(x, column))

    def search(self, gas):
        for gas_data in self.data:
            if gas_data.Gas == gas:
                return gas_data
        return None


def main():
    data = [
        GreenhouseGasData("Carbon dioxide", 280, 414.8, 134.8, 48.0),
        GreenhouseGasData("Methane", 722, 1874.0, 1152.0, 159.0),
        GreenhouseGasData("Nitrous oxide", 270, 329.0, 59.0, 21.9),
        GreenhouseGasData("Fluorinated gases", 0.5, 13.0, 12.5, 2500.0),
    ]
    collection = GreenhouseGasCollection(data)
    print("Data:", collection)

    collection.sort_by("Recent")
    print("Data sorted by Recent:", collection)

    result = collection.search("Carbon dioxide")
    if result:
        print("Data for Carbon dioxide:", result)
    else:
        print("Data for Carbon dioxide not found")


if __name__ == "__main__":
    main()