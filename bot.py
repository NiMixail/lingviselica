import telebot
from telebot import types
from random import choice
from hangman import hangman

cyr = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-.')

bot = telebot.TeleBot('6797245876:AAHNUyaqLZye2Dx9j2WcwXXK34yna_BcGUA')

keyboard = types.ReplyKeyboardMarkup(row_width=5)
buttons = [types.KeyboardButton(text=letter) for letter in cyr]
keyboard.add(*buttons)

words = {}
with open('dictionary.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words[line.split(' * ')[0]] = line.split(' * ')[1]

w = None

neg = """Чё то у вас минус мозг.
Даже мясо образованей, чем ты.
Вообще не people of culture
Вы последние, худшие, топ -10000.
Вы уже слились с бетоном, вы вообще не люди.
Водка без колы - деньги на ветер.
Коллеги, если вы не запомните это определение, мы всем выпишем за счет библиотеки учебники русского языка 5 класса.""".split(
    '\n')

pos = """Я ем дедов.
Мне пора повеситься. Вам время заварить чай.
Хайпим, хайпим, ыэээ…
Абабубабубабаба.
Ощущения - АТАС!!! полный ФЕФЕФЕ!
МЯЯЯЯУ!
Какого чёрта у вас это слово существует?
""".split('\n')


def upd(msg, mstks, vw):
    text = f"<code>{hangman[mstks]}</code>\n{vw}"
    if text != msg.text:
        try:
            bot.edit_message_text(chat_id=msg.chat.id,
                                  message_id=msg.message_id,
                                  text=text,
                                  parse_mode='HTML')
        except Exception as e:
            print(e)


@bot.message_handler(commands=['jajemdedov'])
def jajemdedov(message):
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "кинув взгляд в загадочной мексиканской шляпи, убираю кнопки с буквами...",
                     reply_markup=remove_markup)


@bot.message_handler(commands=['guess'])
def guess(message):
    global w, view, mistakes, letters, msg
    w = choice(list(words.keys()))
    view = ''.join(i + ' ' if i == ' ' else '_ ' for i in w)
    mistakes = 0
    letters = {c: 7 for c in cyr}  # 7 - not used, 2 - guessed, 1 - wrong

    bot.reply_to(message, text='ㅤ', reply_markup=keyboard)
    msg = bot.reply_to(message, text=f"<code>{hangman[mistakes]}</code>\n{view}", parse_mode='HTML')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global w, view, mistakes, letters
    if w and (len(message.text) == 1 or message.text == w) and (message.text.isupper() or not message.text.isalpha()):
        c = message.text
        if c in w:
            if c == w:
                view = ''.join(i + ' ' for i in w)
            if c in letters:
                if letters[c] != 2:
                    letters[c] = 2
                    for i in range(len(w)):
                        if w[i] == c:
                            view = view[:i * 2] + c + ' ' + view[(i + 1) * 2:]
                    upd(msg, mistakes, view)
            if view == ''.join(i + ' ' for i in w):
                bot.reply_to(message,
                             f"{choice(pos)} \nБыло действительно загадано слово {w} — {words[w]}")
                w = None
        else:
            if c in letters:
                letters[c] = 1
            mistakes += 1
            bot.set_message_reaction(message.chat.id, message.message_id,
                                     [types.ReactionTypeEmoji("👎")])
            upd(msg, mistakes, view)
            if mistakes == len(hangman) - 1:
                bot.reply_to(message,
                             text=f'{choice(neg)} \nБыло загадано слово {w} — {words[w]}')
                w = None


bot.polling()
