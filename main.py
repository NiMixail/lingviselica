# Hangman game
import os
from random import choice
from hangman import hangman


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')


words = {}
with open('dictionary.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words[line.split(' * ')[0]] = line.split(' * ')[1]

while True:
    clr()
    w = choice(list(words.keys()))
    view = ''.join(i if i == ' ' else '_' for i in w)
    mistakes = 0
    letters = {c: 7 for c in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-.'}  # 7 - not used, 2 - guessed, 1 - wrong
    while True:
        print(hangman[mistakes] + '    ' + view +
              '    Исп.: ' + ''.join(f'\033[3{str(letters[le])}m{le}\033[0m' for le in sorted(letters)))
        if mistakes == len(hangman) - 1:
            print('Вы проиграли!')
            print(w, '-', words[w])
            input('Нажмите Enter, чтобы продолжить..\n\n')
            break
        letter = input('\nВводите букву, славяне: ').upper()
        if letter in w:
            if letter in letters:
                letters[letter] = 2
            for i in range(len(w)):
                if w[i] == letter:
                    view = view[:i] + letter + view[i + 1:]
            clr()
        else:
            mistakes += 1
            if letter in letters:
                letters[letter] = 1
            clr()
        if view == w:
            print('Верно!')
            print(w, '-', words[w])
            input('Нажмите Enter, чтобы продолжить..\n\n')
            break
