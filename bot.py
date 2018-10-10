import telebot
from telebot import types
import secret
from base import *
from my_types import  *

bot = telebot.TeleBot(secret.token)

def sendMainKeyboard(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('Добавить', 'Показать', 'Удалить')
    keyboard.add('Решить!')
    bot.send_message(message.chat.id, 'Меню', reply_markup = keyboard)
    bot.register_next_step_handler(message, mainKeyboardHandler)

@bot.message_handler(commands=['start', 'back', 'menu'])
def handle_text(message):
    sendMainKeyboard(message)

def mainKeyboardHandler(message):
    if message.text == 'Решить!':
        #
        return

    keyboard = types.ReplyKeyboardMarkup()
    if message.text == 'Добавить':
        keyboard.add('Ресурс', 'Товар', 'Расход')
        bot.register_next_step_handler(message, addMenuHandler)
    elif message.text == 'Показать':
        keyboard.add('Ресурсы', 'Товары', 'Расходы')
        bot.register_next_step_handler(message, showMenuHandler)
    elif message.text == 'Удалить':
        keyboard.add('Ресурс', 'Товар', 'Расход')
        bot.register_next_step_handler(message, removeMenuHandler)
    else:
        return
    keyboard.add('Назад')

    bot.send_message(message.chat.id, 'Выберете что ' + message.text.lower(), reply_markup=keyboard)

def addMenuHandler(message):
    if message.text == 'Назад':
        sendMainKeyboard(message)
        return

    if message.text == 'Ресурс':
        bot.register_next_step_handler(message, addResourceHandler)
        bot.send_message(message.chat.id, 'Введите название ресурса и его запасы')
    elif message.text == 'Товар':
        bot.register_next_step_handler(message, addProductHandler)
        bot.send_message(message.chat.id, 'Введите название товара и его стоимость')
    elif message.text == 'Расход':
        if len(Base.fetchResources(message.chat.id)) == 0:
            bot.send_message(message.chat.id, 'Сначала добавьте ресурсы')
        elif len(Base.fetchProducts(message.chat.id)) == 0:
            bot.send_message(message.chat.id, 'Сначала добавьте товары')
        else:
            bot.register_next_step_handler(message, addConsumptionHandler)
            bot.send_message(message.chat.id, 'Введите название товара, ресурса и его расход')
    else:
        bot.register_next_step_handler(message, addMenuHandler)
        return

def addResourceHandler(message):
    bot.register_next_step_handler(message, addMenuHandler)
    input = [x for x in  message.text.replace('\n', ' ').split(' ') if x != '']
    try:
        Base.insertResource(message.chat.id, Resource(input[0].lower(), int(input[1])))
        bot.send_message(message.chat.id, "Успешно добавлено!")
    except sqlite3.Error as e:
        print(e)
        bot.send_message(message.chat.id, "Уже есть ресурс с таким названием")
    except:
        bot.send_message(message.chat.id, "Неверно введены данные")


def addProductHandler(message):
    bot.register_next_step_handler(message, addMenuHandler)
    input = [x for x in  message.text.replace('\n', ' ').split(' ') if x != '']
    try:
        Base.insertProduct(message.chat.id, Product(input[0].lower(), int(input[1])))
        bot.send_message(message.chat.id, "Успешно добавлено!")
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, "Уже есть товар с таким названием")
    except:
        bot.send_message(message.chat.id, "Неверно введены данные")

def addConsumptionHandler(message):
    bot.register_next_step_handler(message, addMenuHandler)
    input = [x for x in message.text.replace('\n', ' ').split(' ') if x != '']
    try:
        Base.insertConsumption(message.chat.id, ConsumptionRow(input[0].lower(), input[1].lower(), int(input[2])))
        bot.send_message(message.chat.id, "Успешно добавлено!")
    except sqlite3.Error as e:
        if 'foreign' in str(e).lower():
            bot.send_message(message.chat.id, "Неправильно введено имя продукта/ресурса")
        else:
            bot.send_message(message.chat.id, "Уже есть товар с таким названием")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Неверно введены данные")

def showMenuHandler(message):
    if message.text == 'Назад':
        sendMainKeyboard(message)
        return
    bot.register_next_step_handler(message, showMenuHandler)

    if message.text == 'Ресурсы':
        fetched = Base.fetchResources(message.chat.id)
        header = "Ресурс:   Количество:"
    elif message.text == 'Товары':
        fetched = Base.fetchProducts(message.chat.id)
        header = "Товар:   Стоимость:"
    elif message.text == 'Расходы':
        fetched = Base.fetchConsumptionRows(message.chat.id)
        header = "Товар:   Ресурс:  Расход:"
    else:
        return

    bot.send_message(message.chat.id, 'Ваши ' + message.text.lower() + '\n\n' + header + '\n' +
                                      ('Пусто' if len(fetched) == 0 else '\n'.join([str(x) for x in fetched])))


def genInlineKeyboard(chatId, dataType, data):
    keyboard = types.InlineKeyboardMarkup()
    for d in data:
        keyboard.add(types.InlineKeyboardButton(d, callback_data='$'.join([str(chatId), dataType, d])))
    return keyboard


inlineMessages = {}

def setInlineMessage(chatId, dataType, messageId):
    inlineMessages[str(chatId) + '_' + str(dataType).lower()] = messageId

def getInlineMessage(chatId, dataType):
    return inlineMessages[str(chatId) + '_' + str(dataType).lower()]

def removeMenuHandler(message):
    if message.text == 'Назад':
        sendMainKeyboard(message)
        return

    fetched = None
    if message.text == 'Ресурс':
        fetched = [x.name for x in Base.fetchResources(message.chat.id)]
    elif message.text == 'Товар':
        fetched = [x.name for x in Base.fetchProducts(message.chat.id)]
    elif message.text == 'Расход':
        fetched = [x.prodName + " " + x.resName for x in Base.fetchConsumptionRows(message.chat.id)]
    else:
        return

    if len(fetched) > 0:
         m = bot.send_message(message.chat.id, 'Выберете ' + message.text.lower() + ' для удаления',
                         reply_markup=genInlineKeyboard(message.chat.id, message.text, fetched))
         setInlineMessage(m.chat.id, message.text, m.message_id)

    else:
        bot.send_message(message.chat.id, 'Нет ' + message.text.lower() + 'ов для удаления')
    bot.register_next_step_handler(message, removeMenuHandler)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('$')
    fetched = None
    if data[1] == 'Ресурс':
        Base.deleteResource(data[0], data[2])
        fetched = [x.name for x in Base.fetchResources(data[0])]
    elif data[1] == 'Товар':
        Base.deleteProduct(data[0], data[2])
        fetched = [x.name for x in Base.fetchProducts(data[0])]
    elif data[1] == 'Расход':
        cons = data[2].split(' ')
        Base.deleteConsumptionRow(data[0], cons[0], cons[1])
        fetched = [x.prodName + " " + x.resName for x in Base.fetchConsumptionRows(data[0])]

    bot.answer_callback_query(call.id, "Успешно удалено!")
    if len(fetched) > 0:
        bot.edit_message_reply_markup(data[0], getInlineMessage(data[0], data[1]),
                                      reply_markup=genInlineKeyboard(data[0], data[1], fetched))
    else:
        bot.delete_message(data[0], inlineMessages[data[0] + "_" + data[1].lower()])

bot.polling(none_stop=True,interval=0)
