# !/usr/bin/env python
from data import token
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import traceback

# Авторизация ВК
vk = vk_api.VkApi(token=token)
session = vk.get_api()

# Переменные
longpoll = VkBotLongPoll(vk, 196777400)
users = {}
print("Бот запущен")


# Классы
class SetUnicVariables:
    def __init__(self, response):
        self.event = event
        self.direction = 0
        self.vote = False
        self.response = response

    def voter(self, v=None):
        global full_name
        self.direction = v
        if self.direction == 'я пока не определился(-ась)':
            send("Подтвердим запрос: Вы хотитите вступить в Молодежное самоуправление, но с направлением не "
                 "определились\nПравильно?", keyboard)
        else:
            send("Подтвердим запрос: Вы хотитите вступить в Молодежное самоуправление на "
                 "направление {0}\nПравильно?".format(self.direction), keyboard)
        full_name = vk.method("users.get", {"user_ids": event.obj.from_id})[0]['first_name'] + ' ' + \
                    vk.method("users.get", {"user_ids": event.obj.from_id})[0]['last_name']

        return self.direction


# Функции
def send(message, kb, attachment=None, payload=None):
    vk.method('messages.send',
              {'peer_id': event.obj.peer_id, 'user_id': event.obj.user_id, 'message': message,
               'random_id': get_random_id(),
               'attachment': attachment, 'keyboard': kb, 'payload': payload})


def create_inline_kb():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_openlink_button('Вступить в  общую беседу', 'https://vk.me/join/AJQ1dyhiTxhUMvyd8Iq5PyfI')
    if test == 'культурно-массовые мероприятия':
        keyboard.add_line()
        keyboard.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d_UYIBiOxLbcrwCtzp3t')
    if test == 'информационное':
        keyboard.add_line()
        keyboard.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d8sGNxjh0FKltch6tUZ1')
    if test == 'корпоративная культура':
        keyboard.add_line()
        keyboard.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d37oIhhvkWSKlsSAplFD')
    if test == 'спортивное':
        keyboard.add_line()
        keyboard.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1dxUFNhjXn8R4wHWYPub2')
    keyboard = keyboard.get_keyboard()
    return keyboard


def create_keyboard(response, payload):
    keyboard = VkKeyboard(one_time=False)
    if response == 'культурно-массовые мероприятия' or response == 'информационное' \
            or response == 'корпоративная культура' or response == 'спортивное' \
            or response == 'я пока не определился(-ась)':
        keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Нет, изменить', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Меню', color=VkKeyboardColor.DEFAULT)
    elif response == 'хочу вступить в мс' or response == 'нет, изменить':
        keyboard.add_button('Культурно-массовые мероприятия', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Информационное', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Корпоративная культура', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Спортивное', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Я пока не определился(-ась)', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Меню', color=VkKeyboardColor.DEFAULT)
    elif response == 'структура' or response == '1. кульурно-массовые мероприятия' \
            or response == '2. информационное направление' \
            or response == '3. корпоративная культура' or response == '4. спортивное направление':
        keyboard.add_button('1. Кульурно-массовые мероприятия', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('2. Информационное направление', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('3. Корпоративная культура', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('4. Спортивное направление', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Меню', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Хочу вступить в МС', color=VkKeyboardColor.POSITIVE)
    else:
        keyboard.add_button('Структура', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Контакты', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Нормативная база', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Хочу вступить в МС', color=VkKeyboardColor.POSITIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard


def bot():  # Основная функция
    global event, keyboard, test
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:

                    if event.obj.payload is not None:
                        payload = event.obj.payload
                    else:
                        payload = None

                    response = event.obj.text.lower()
                    keyboard = create_keyboard(response, payload)

                    if response == 'начать' or response == 'меню':
                        send("Меню:", keyboard)

                    # Кнопки основного меню

                    elif response == 'структура':
                        send("Структура МС\nМолодёжное самоуправление состоит из 4 направлений, за каждое из "
                             "которых отвечают заместители.\n1. Направление по культурно-массовым "
                             "мероприятиям.\n2. Информационное направление.\n3. Направление по "
                             "корпоративной культуре.\n4. Спортивное направление\n\nЧтобы узнать "
                             "подробнее о каком-либо направлении, нажми соответствующую кнопку😌", keyboard)
                    elif response == 'нормативная база':
                        send("Появится позже", keyboard)
                    elif response == 'контакты':
                        send("@id103015969(Вера Козьмина)\nПредседатель молодежного самоуправления\n\n"
                             "@id157367997(Егор Балашов)\nЗаместитель председателя молодежного самоуправления"
                             "\n\n@id182909211(Таня Бова)\nЗаместитель председателя по культурно-массовым "
                             "мероприятиям\n\n@id273207132(Максим Сергеев)\nЗаместитель председателя по "
                             "информационному направлению\n\n@id139115497(Арина Мальцева)\nЗаместитель "
                             "председателя по корпоративной культуре\n\n@id466687166(Карина Грахова)\n"
                             "Заместитель председателя по спортивному направлению ", keyboard)
                    elif response == 'хочу вступить в мс':
                        # Добавление пользователя в массив данных пользователей
                        user_id = event.obj.user_id
                        if users.get(user_id) is None:
                            users[user_id] = SetUnicVariables(response)

                        send("Выберите направление:", keyboard)

                    # Кнопки меню структуры
                    elif response == '1. кульурно-массовые мероприятия':
                        send("В данном направлении ты сможешь:\n"
                             "⭐ пообщаться с креативными, талантливыми и интересными людьми;\n"
                             "⭐ раскрыть в себе творческие и организаторские способности;\n"
                             "⭐ попробовать себя в роли руководителя;\n"
                             "⭐ придумывать массовые мероприятия и реализовывать их;\n"
                             "⭐ завести новые интересные и полезные знакомства.\n"
                             "Интересно?😏\n"
                             "Пиши @tak_to_mir(Тане) и она все тебе подробно расскажет 🤗", keyboard)
                    elif response == '2. информационное направление':
                        send("В данном направлении ты сможешь:\n"
                             "💾 пообщаться с креативными, талантливыми и интересными людьми;\n"
                             "💾 реализовать все свои задумки;\n"
                             "💾 попробовать себя в роли руководителя, дизайнера, оформителя;\n"
                             "💾 научиться вести социальные сети;\n"
                             "💾 придумывать классные мероприятия и реализовывать их;\n"
                             "💾 завести новые интересные и полезные знакомства.\n"
                             "Интересно?😏\n"
                             "Пиши @vjgrvbnapnne(Максиму) и он все тебе подробно расскажет 🤗", keyboard)
                    elif response == '3. корпоративная культура':
                        send("В данном направлении ты сможешь:\n"
                             "🧩 пообщаться с креативными, талантливыми и интересными людьми;\n"
                             "🧩 реализовать все свои задумки;\n"
                             "🧩 попробовать себя в роли руководителя, дизайнера и оформителя;\n"
                             "🧩 придумывать классные мероприятия на развитие личностных и командных качеств "
                             "и реализовывать их;\n"
                             "🧩 завести новые интересные и полезные знакомства.\n"
                             "Интересно?😏\n"
                             "Пиши @arishkamal(Арине) и она все тебе подробно расскажет 🤗", keyboard)
                    elif response == '4. спортивное направление':
                        send("В данном направлении ты сможешь:\n"
                             "⚽ пообщаться с креативными, талантливыми и интересными людьми;\n"
                             "⚽ реализовать все свои задумки;\n"
                             "⚽ попробовать себя в роли руководителя;\n"
                             "⚽ придумывать спортивные мероприятия и реализовывать их;\n"
                             "⚽ завести новые интересные и полезные знакомства.\n"
                             "Интересно?😏\n"
                             "Пиши @id466687166(Карине) и она все тебе подробно расскажет 🤗", keyboard)

                    # Кнопки меню вступления в МС
                    elif response == 'культурно-массовые мероприятия':
                        test = users[user_id].voter('культурно-массовые мероприятия')
                    elif response == 'информационное':
                        test = users[user_id].voter('информационное')
                    elif response == 'корпоративная культура':
                        test = users[user_id].voter('корпоративная культура')
                    elif response == 'спортивное':
                        test = users[user_id].voter('спортивное')
                    elif response == 'я пока не определился(-ась)':
                        test = users[user_id].voter('я пока не определился(-ась)')

                    # Подтвержение вступления в МС
                    elif response == 'да':
                        vk.method('messages.send',
                                  {'chat_id': 1,
                                   'message': "@id{0}({1}) хочет вступить в МС.\nНаправление: {2}".format(
                                       event.obj.from_id, full_name,
                                       test), 'random_id': get_random_id(), 'attachment': None,
                                   'keyboard': None})

                        keyboard = create_inline_kb()
                        send('Уведомление о вступлении отправлено руководителям\nНажмите на кнопку, '
                             'чтобы вступить в беседу', keyboard)
                        keyboard = create_keyboard(response, payload)
                        send('Меню', keyboard)

                    elif response == 'нет, изменить':
                        send("Выберите направление:", keyboard)
                    else:
                        send("Пожалуйста, используйте кнопки", keyboard)
        except:
            print(traceback.format_exc())
