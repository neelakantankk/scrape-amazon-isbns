#! python3

from exceptions import InvalidISBNException

def isbn_converter(isbn):
    if len(isbn) == 13:
        return isbn13_to_isbn10(isbn)
    elif len(isbn) == 10:
        return isbn10_to_isbn13(isbn)
    else:
        raise InvalidISBNException

def isbn13_to_isbn10(isbn):
    isbn10 = isbn[3:-1]
    check_digit = 0
    mods = [num for num in range(10,1,-1)]

    for digit,place_value in zip(isbn10,mods):
        check_digit+= int(digit) * place_value

    check_digit = (11 - (check_digit % 11)) % 11 

    if check_digit == 10:
        check_digit = 'X'

    isbn10 = f'{isbn10}{check_digit}' 

    return isbn10

def main():
    isbn = '9781292265193'

    print(isbn_converter(isbn))

if __name__ == '__main__':
    main()
