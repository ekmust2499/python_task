cols = '123456789'


def output(values, sqr1, sqr2, sqr3, sqr4, sqr5):
    for r in 'ABCDEF':
        print(''.join(values[sqr1[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(2) for c in cols) + '      ' +
              ''.join(values[sqr2[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(2) for c in cols))
    print(''.join(values[sqr1[(ord('G') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('A') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr2[(ord('G') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    print(''.join(values[sqr1[(ord('H') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('B') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr2[(ord('H') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    print(''.join(values[sqr1[(ord('I') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('C') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr2[(ord('I') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    for r in 'DEF':
        print('            ' +
              ''.join(values[sqr5[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(2) for c in cols))

    print(''.join(values[sqr3[(ord('A') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('G') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr4[(ord('A') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    print(''.join(values[sqr3[(ord('B') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('H') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr4[(ord('B') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    print(''.join(values[sqr3[(ord('C') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols) +
          ''.join(values[sqr5[(ord('I') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in '456') +
          ''.join(values[sqr4[(ord('C') - 65) * 9 + int(c) - 1]]
                  .center(2) for c in cols))
    for r in 'DEFCHI':
        print(''.join(values[sqr3[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(2) for c in cols) + '      ' +
              ''.join(values[sqr4[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(2) for c in cols))
    print()


def fill_squares(samurai):
    """
    Function of filling Sudoku Samurai by squares
    """
    symbol = 'a'  # top left
    square_a = samurai.cross(samurai.rows, samurai.cols, symbol)
    symbol = 'b'  # top right
    square_b = samurai.cross(samurai.rows, samurai.cols, symbol)
    symbol = 'c'  # bottom left
    square_c = samurai.cross(samurai.rows, samurai.cols, symbol)
    symbol = 'd'  # bottom left
    square_d = samurai.cross(samurai.rows, samurai.cols, symbol)
    symbol = '+'
    square_middle = [samurai.remake_middle(x)
                     for x in samurai.cross(samurai.rows,
                                            samurai.cols, symbol)]
    return square_a, square_b, square_c, square_d, square_middle
