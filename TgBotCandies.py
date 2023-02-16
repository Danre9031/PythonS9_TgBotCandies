import telebot
from random import randint

bot = telebot.TeleBot("") 

names = []
candies = 50
max_value = 28
current_value = 0
value = 0

def restart():
    global candies
    global current_value
    candies = 50
    current_value = 0

def get_player_names(message):   
    global names
    names = [message.from_user.first_name, 'Бот']

def coin_toss():
    global switch
    global names
    switch = randint(0, 1)

def switch_turn():
    global switch
    if switch == 1:
        switch = 0
    else:
        switch = 1

def player_move(message):
    global value
    global current_value
    global candies
    if message.text.isdigit() and 0 < int(message.text) <= max_value:
        value = int(message.text)
        bot.send_message(message.chat.id, f'Игрок берет {value} конфет')
        candies -= value
        current_value = value
        switch_turn()
    else:
        bot.send_message(message.chat.id, f'Можно брать от 1 до {max_value} конфет!')    
    game(message)

def bot_move(message):
    global current_value
    global value
    global candies
    
    if candies % (max_value + 1) > 0:
        value = candies % (max_value + 1)
   
    else:
        if current_value > 0:
            value = max_value + 1 - current_value
        
        else:
            value = randint(1, max_value)
    
    if current_value > 0 and candies % (max_value + 1) == 0:
        value = max_value + 1 - current_value
    bot.send_message(message.chat.id, f'Бот берет {value} конфет')
    candies -= value
    current_value = value
    switch_turn()
    game(message)


def game(message):
    if candies > 0:
        bot.send_message(message.chat.id, f'На кону {candies} конфет')
        if switch == 0:
            bot.send_message(message.chat.id, f'Ваш ход. Сколько конфет возьмете (1 - {max_value}?')
            bot.register_next_step_handler(message, player_move)
        else:
            bot_move(message)
    else:
        bot.send_message(message.chat.id, f'Осталось {candies} конфет')
        switch_turn()
        bot.send_message(message.chat.id, f'Выиграл {names[switch]}!')

def option(message):
    if message.text.lower() == 'yes':  
        get_player_names(message)
        coin_toss()
        restart()
        bot.send_message(message.chat.id, f'Первым ходит {names[switch]}')
        game(message)
    elif message.text.lower() == 'no':
        bot.send_message(message.chat.id, f'Ok')
    else:
        bot.send_message(message.chat.id, f'Команда не распознано. Попробуйте снова.')

def play_game():
    @bot.message_handler(content_types = ["text"]) 
    def controller(message):
        if message.text.lower() == 'play':
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, сыграем в игру с конфетами (yes/no)?')
            bot.register_next_step_handler(message, option)
        else:
            bot.send_message(message.chat.id, f'Напиши play') 
    bot.infinity_polling()

play_game()