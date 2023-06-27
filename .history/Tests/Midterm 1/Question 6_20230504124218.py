import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def myhex(number):
    hex_dict = {10: 'A',11: 'B',12: 'C',13: 'D',14: 'E',15: 'F'}

    if number == 0:
        return '0'

    else:
        value = ''
        while number > 0:
            remainder = number % 16
            if remainder <= 9:
                value = str(remainder)+value
            else:
                # value = hex_dict[remainder]+value
                value = hex_dict.get(remainder)+value

            number //= 16

    print(f"Hexidecimal of {number}: {value}")


while True:
    clear()
    value = int(input("Enter a number within the range (0,1024): "))
    if value >= 0 and value <= 1024:
        myhex(value)
        exit()