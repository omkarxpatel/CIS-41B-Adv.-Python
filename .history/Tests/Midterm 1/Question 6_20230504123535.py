def myhex(number):
    hex_dict = {
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F'
    }

    if number == 0:
        return '0'

    result = ''
    while number > 0:
        remainder = number % 16
        if remainder < 10:
            result = str(remainder) + result
        else:
            result = hex_dict[remainder] + result
        number //= 16

    print("Hexidecimal of result)

myhex(int(input("Enter a number within the range (0,1024): ")))