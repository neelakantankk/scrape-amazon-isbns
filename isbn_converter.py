#! /usr/local/bin/python3.7

import argparse

from exceptions import InvalidISBNError

def isbn_converter(isbn):
    if len(isbn) == 13:
        return isbn13_to_isbn10(isbn)
    elif len(isbn) == 10:
        return isbn10_to_isbn13(isbn)
    else:
        raise InvalidISBNError

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

def isbn10_to_isbn13(isbn):
    isbn13 = f"978{isbn[:-1]}"
    check_digit = 0

    for index,digit in enumerate(isbn13,start=1):
        if index%2 == 0:
            check_digit += 3 * int(digit)
        else:
            check_digit += int(digit)

    check_digit = 10 - (check_digit % 10)
    isbn13 = f"{isbn13}{check_digit}"

    return isbn13

def main():

    parser = argparse.ArgumentParser(description="Convert ISBNS between ISBN 13 and ISBN 10")
    parser.add_argument("isbns",nargs="+", type=str)

    isbns = parser.parse_args().isbns

    for isbn in isbns:
        try:
            print(isbn_converter(isbn))
        except InvalidISBNError:
            print(f"{isbn} is invalid")


if __name__ == '__main__':
    main()
