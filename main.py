# Hangman game
from random import choice
from hangman import hangman

words = {}
with open('dictionary.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words[line.split(' * ')[0]] = line.split(' * ')[1]

while True:
    print('\n' * 32)
    w = choice(list(words.keys()))
    view = '_' * len(w)
    mistakes = 0
    while True:
        print(hangman[mistakes] + ' ' * 6 + view)
        if mistakes == len(hangman) - 1:
            print('Вы проиграли!')
            print(w, '-', words[w])
            input('Нажмите Enter, чтобы продолжить..\n\n')
            break
        letter = input('\nВводите букву, славяне: ').upper()
        if letter in w:
            for i in range(len(w)):
                if w[i] == letter:
                    view = view[:i] + letter + view[i+1:]
            print('\n' * 32)
        else:
            mistakes += 1
            print('\n' * 32)
        if view == w:
            print('Верно!')
            print(w, '-', words[w])
            input('Нажмите Enter, чтобы продолжить..\n\n')
            break
