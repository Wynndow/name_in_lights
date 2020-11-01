from main import LETTER_CODES

for k, v in LETTER_CODES.items():
    for i in range(5):
        for j in range(3):
            if v[j][i] == 1:
                print('X', end = '')
            else:
                print(' ', end = '')
        print()

    print('\n\n')
