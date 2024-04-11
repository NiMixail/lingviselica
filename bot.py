import telebot
from telebot import types
from random import choice
from hangman import hangman
from re import sub

cyr = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-.')

with open('token.txt') as f:
    token = f.read()

bot = telebot.TeleBot(token)

keyboard = types.ReplyKeyboardMarkup(row_width=5)
buttons = [types.KeyboardButton(text=letter) for letter in cyr]
keyboard.add(*buttons)

words = {}
with open('dictionary.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words[line.split(' * ')[0]] = line.split(' * ')[1]
frazeos = {}
with (open('dictionary_f_.txt', 'r', encoding='utf-8') as f):
    for line in f:
        line = sub(r'</?div.*?>|<br.*?>|a href.*?.htm»', '', line
                   ).replace('&amp;LT;', '⟨').replace('&amp;GT;', '⟩')
        frazeo = sub(r'\(.*?\)', '', line.split(' ###### ')[0]).upper()
        frazeos[frazeo] = line.split(' ###### ')[1]
chats = {}

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


def upd(chat_id):
    try:
        chat = chats[chat_id]
        text = f"<code>{hangman[chat['mis']]}</code>\n{chat['view']}"
        if text != chat['msg'].text:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=chat['msg'].id,
                                      text=text,
                                      parse_mode='HTML')
                # bot.edit_message_reply_markup()
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, text='''Доброго времени суток! 
    Чтобы воспользоваться мною, пропишите /guess.
    Если хотите угадывать фразеологизм, а не термин, пропишите /fguess.
    Чтобы скрыть клавиатуру букв, пропишите /jajemdedov.
    В моей библиотеке более 2500 терминов и 14300 фразеологизмов. Удачи!''')


@bot.message_handler(commands=['test'])
def test(message):
    ch = choice(list(frazeos.keys()))
    print(ch)
    bot.reply_to(message,
                 text=frazeos[ch],
                 parse_mode='HTML')


@bot.message_handler(commands=['jajemdedov'])
def jajemdedov(message):
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "кинув взгляд в загадочной мексиканской шляпи, убираю кнопки с буквами...",
                     reply_markup=remove_markup)


@bot.message_handler(commands=['guess'])
def guess(message):
    bot.reply_to(message, text='ㅤ', reply_markup=keyboard)
    print(message.chat.id)
    chats[message.chat.id] = {'w': choice(list(words.keys())),
                              'view': None,
                              'mis': 0,
                              'abc': {c: 7 for c in cyr}}  # 7 - not used, 2 - guessed, 1 - wrong
    chats[message.chat.id]['info'] = words[chats[message.chat.id]['w']]
    chats[message.chat.id]['view'] = ''.join(i + ' ' if i == ' ' else '_ ' for i in chats[message.chat.id]['w'])
    chats[message.chat.id]['msg'] = bot.reply_to(message,
                                                 text=f"<code>{hangman[0]}</code>\n{chats[message.chat.id]['view']}",
                                                 parse_mode='HTML')

@bot.message_handler(commands=['fguess'])
def fguess(message):
    bot.reply_to(message, text='ㅤ', reply_markup=keyboard)
    print('f', message.chat.id)
    chats[message.chat.id] = {'w': choice(list(frazeos.keys())),
                              'view': None,
                              'mis': 0,
                              'abc': {c: 7 for c in cyr}}  # 7 - not used, 2 - guessed, 1 - wrong
    chats[message.chat.id]['info'] = frazeos[chats[message.chat.id]['w']]
    chats[message.chat.id]['view'] = ''.join(i + ' ' if i == ' ' else '_ ' for i in chats[message.chat.id]['w'])
    chats[message.chat.id]['msg'] = bot.reply_to(message,
                                                 text=f"<code>{hangman[0]}</code>\n{chats[message.chat.id]['view']}",
                                                 parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    ch = chats[message.chat.id]
    if (ch['w'] and (len(message.text) == 1 or message.text == ch['w'])
            and (message.text.isupper() or not message.text.isalpha())):
        c = message.text
        if c in ch['w']:
            if c == ch['w']:
                ch['view'] = ''.join(i + ' ' for i in ch['w'])
            if c in ch['abc']:
                if ch['abc'][c] != 2:
                    ch['abc'][c] = 2
                    for i in range(len(ch['w'])):
                        if ch['w'][i] == c:
                            ch['view'] = ch['view'][:i * 2] + c + ' ' + ch['view'][(i + 1) * 2:]
                    upd(message.chat.id)
            if ch['view'] == ''.join(i + ' ' for i in ch['w']):
                bot.reply_to(message,
                             f"{choice(pos)} \nБыло действительно загадано <b>{ch['w']}</b> — {ch['info']}",
                             parse_mode='HTML')
                ch['w'] = None
        else:
            if c in ch['abc']:
                ch['abc'][c] = 1
            ch['mis'] += 1
            bot.set_message_reaction(message.chat.id, message.message_id,
                                     [types.ReactionTypeEmoji("👎")])
            upd(message.chat.id)
            if ch['mis'] == len(hangman) - 1:
                bot.reply_to(message,
                             text=f'{choice(neg)} \nБыло загадано <b>{ch["w"]}</b> — {ch["info"]}',
                             parse_mode='HTML')
                ch['w'] = None


bot.polling()
