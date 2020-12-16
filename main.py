# !/usr/bin/env python
import os
from data import *
import messages
import json
import traceback
import random
import urllib.request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from time import sleep
from loguru import logger

# Авторизация ВК
vk = vk_api.VkApi(token=token)
session = vk.get_api()

longpoll = VkBotLongPoll(vk, 196777400)
users = {}
logger.add("error.log", format="{time} {level} {message}", level="ERROR", rotation="100 KB", compression="zip")
logger.info("Bot started")


# Классы
class SetUnicVariables:
    def __init__(self, user_id):
        self.event = event
        self.user_id = user_id
        self.direction = ''
        self.gender = ''

    def voter(self, v=None):
        global full_name
        self.direction = v
        self.gender = 'ась' if determine_gender(self.user_id) == 'w' else 'ся'
        if self.direction in ('не определился', 'не определилась'):
            send_message(f"Подтвердим запрос: \nТы хочешь вступить в Молодежное самоуправление, но с направлением не "
                         f"определил{self.gender}\nПравильно?", keyboard)
        else:
            send_message(f"Подтвердим запрос: \nТы хочешь вступить в Молодежное самоуправление на "
                         f"направление {self.direction}\nПравильно?", keyboard)
        full_name = vk.method("users.get", {"user_ids": event.obj.from_id})[0]['first_name'] + ' ' + \
                    vk.method("users.get", {"user_ids": event.obj.from_id})[0]['last_name']

        return self.direction


# Функции
@logger.catch()
def mailing_subscribers():
    message_id = message_about_processing(None, 0)
    try:
        message_about_processing(message_id, 10)
        name = "mailing_users.txt"
        urllib.request.urlretrieve(url, name)
        mailers = ''
        user_num = 1
        percent = 0

        with open(name, "r") as file:
            message_about_processing(message_id, 35)
            for line in file:
                # logger.debug(len(list(file)))
                user_name = vk.method("users.get", {"user_ids": line})[0]['first_name'] + \
                            ' ' + vk.method("users.get", {"user_ids": line})[0]['last_name']
                user_num += 1
                percent += 1
                if percent == 15:
                    message_about_processing(message_id, 70)
                mailers += f'\n{user_num - 1}. @id{line.strip()} ({user_name})'
            edit_message(f"Запрос выполнен 100%\n\n{mailers}", message_id)

        os.remove("mailing_users.txt")

    except:
        logger.error(traceback.format_exc())
        send_message("Ошибка запроса", keyboard)


def determine_gender(user_id):
    if vk.method('users.get', {'user_ids': user_id, 'fields': 'sex'})[0]['sex'] == 1:
        return 'w'
    else:
        return 'm'


def message_about_processing(message_id, percent):
    """При первом вызове функции для данного сообщения присваивать аргументу percent значение 0"""
    if percent == 0:
        message_id = send_message("Запрос обрабатывается 0%", kb=None)
        return message_id
    elif percent == 100:
        edit_message("Запрос выполнен 100%", message_id)
    else:
        edit_message(f"Запрос обрабатывается {percent}%", message_id)


def edit_message(message, message_id):
    vk.method('messages.edit',
              {'peer_id': event.obj.peer_id,
               'message': message,
               'message_id': message_id})


def send_message(message, kb, attachment=None):
    result = vk.method('messages.send',
                       {'peer_id': event.obj.peer_id, 'user_id': event.obj.user_id,
                        'message': message, 'random_id': get_random_id(),
                        'attachment': attachment, 'keyboard': kb,
                        'dont_parse_links': 0})
    return result


def create_inline_kb():
    kb = VkKeyboard(inline=True)
    kb.add_openlink_button('Вступить в  общую беседу', 'https://vk.me/join/AJQ1dyhiTxhUMvyd8Iq5PyfI')
    if userdata == 'культурно-массовые мероприятия':
        kb.add_line()
        kb.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d_UYIBiOxLbcrwCtzp3t')
    if userdata == 'информационное':
        kb.add_line()
        kb.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d8sGNxjh0FKltch6tUZ1')
    if userdata == 'корпоративная культура':
        kb.add_line()
        kb.add_openlink_button('Вступить в беседу нарпавления', 'https://vk.me/join/AJQ1d37oIhhvkWSKlsSAplFD')

    kb = kb.get_keyboard()
    return kb


def create_keyboard(response, user_id=None, superuser=False):
    kb = VkKeyboard(one_time=False)
    if response == 'культурно-массовые мероприятия' or response == 'информационное' \
            or response == 'корпоративная культура' \
            or response == 'не определился' or response == 'не определилась':
        kb.add_button('Да', color=VkKeyboardColor.POSITIVE)
        kb.add_button('Нет, изменить', color=VkKeyboardColor.NEGATIVE)
        kb.add_line()
        kb.add_button('Меню', color=VkKeyboardColor.SECONDARY)
    elif response == 'хочу вступить в мс' or response == 'нет, изменить':
        kb.add_button('Культурно-массовые мероприятия', color=VkKeyboardColor.PRIMARY)
        kb.add_button('Информационное', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('Корпоративная культура', color=VkKeyboardColor.PRIMARY)
        if determine_gender(user_id) == 'w':
            kb.add_button('Не определилась', color=VkKeyboardColor.PRIMARY)
        else:
            kb.add_button('Не определился', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('Меню', color=VkKeyboardColor.SECONDARY)
    elif response == 'структура' or response == '1. кульурно-массовые мероприятия' \
            or response == '2. информационное направление' \
            or response == '3. корпоративная культура':
        kb.add_button('1. Кульурно-массовые мероприятия', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('2. Информационное направление', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('3. Корпоративная культура', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('Меню', color=VkKeyboardColor.SECONDARY)
        kb.add_button('Хочу вступить в МС', color=VkKeyboardColor.POSITIVE)
    elif superuser and response == 'для админов':
        kb.add_button('Рассылка', color=VkKeyboardColor.PRIMARY)
        kb.add_button('Меню', color=VkKeyboardColor.SECONDARY)
    else:
        kb.add_button('Структура', color=VkKeyboardColor.PRIMARY)
        kb.add_button('Контакты', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        # kb.add_button('Нормативная база', color=VkKeyboardColor.PRIMARY)
        kb.add_button('Шар судьбы', color=VkKeyboardColor.SECONDARY)
        kb.add_button('Ярмарка учебных мест', color=VkKeyboardColor.PRIMARY)
        kb.add_line()
        kb.add_button('Хочу вступить в МС', color=VkKeyboardColor.POSITIVE)
        if superuser:
            kb.add_line()
            kb.add_button('Для админов', color=VkKeyboardColor.NEGATIVE)

    kb = kb.get_keyboard()
    return kb


@logger.catch()
def bot():  # Основная функция
    global event, keyboard, userdata, user_id
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:

                    try:
                        vk.method('groups.enableOnline', {'group_id': event.group_id})  # Включить Онлайн в сообществе
                    except Exception:
                        pass

                    response = event.obj.text.lower()
                    user_id = event.obj.from_id

                    superuser = False
                    for manager in session.groups.getMembers(group_id=event.group_id, filter='managers')['items']:
                        if manager['id'] == user_id and manager['role'] in ('administrator', 'creator', 'editors'):
                            superuser = True

                    if users.get(user_id) is None:
                        users[user_id] = SetUnicVariables(user_id)

                    keyboard = create_keyboard(response, user_id=user_id, superuser=superuser)
                    if response == 'начать' or response == 'меню' or response == 'привет':
                        send_message("Меню:", keyboard)

                    # Кнопки основного меню
                    elif response == 'структура':
                        send_message(messages.structure, keyboard)
                    elif response == 'нормативная база':
                        send_message("Нормативная база появится позже", keyboard)
                    elif response == 'контакты':
                        for leader in messages.leaders:
                            send_message(leader, keyboard)
                    elif response == 'хочу вступить в мс':
                        send_message(messages.enter_ms, keyboard)
                    elif response == 'шар судьбы':
                        send_message(f"Шар судьбы говорит:\n\n«{random.choice(ball)}»", keyboard)

                    # Кнопки для superuser
                    elif response == 'для админов' and superuser:
                        send_message('Функции доступные только для администраторов и редакторов сообщества', keyboard)
                    elif response == 'рассылка' and superuser:
                        send_message('Пользователи подписанные на основную рассылку сообщества '
                                     '(Запрос займёт некоторое время)', keyboard)
                        mailing_subscribers()

                    # Кнопки меню структуры
                    elif response == '1. кульурно-массовые мероприятия':
                        send_message(messages.kmm, keyboard)
                    elif response == '2. информационное направление':
                        send_message(messages.inf, keyboard)
                    elif response == '3. корпоративная культура':
                        send_message(messages.corp, keyboard)

                    # Кнопка Ярмарки учебных мест
                    elif response == 'ярмарка учебных мест':
                        send_message(messages.ya_u_m(vk.method('users.get',
                                                               {'user_ids': user_id, 'fields': 'sex'})[0]['sex']),
                                     keyboard)

                    # Кнопки меню вступления в МС
                    elif response == 'культурно-массовые мероприятия':
                        userdata = users[user_id].voter(v='культурно-массовые мероприятия')
                    elif response == 'информационное':
                        userdata = users[user_id].voter(v='информационное')
                    elif response == 'корпоративная культура':
                        userdata = users[user_id].voter(v='корпоративная культура')
                    elif response == 'не определился' or response == 'не определилась':
                        if determine_gender(user_id) == 'w':
                            userdata = users[user_id].voter(v='не определилась')
                        else:
                            userdata = users[user_id].voter(v='не определился')

                    # Подтвержение вступления в МС
                    elif response == 'да':
                        vk.method('messages.send',
                                  {'chat_id': 5,
                                   'message': f"@id{event.obj.from_id}({full_name}) "
                                              f"хочет вступить в Молодёжное самоуправление.\nНа направление: {userdata}",
                                   'random_id': get_random_id(), 'attachment': None,
                                   'keyboard': None})

                        keyboard = create_inline_kb()
                        send_message('Руководители уведомлены о тебе\nТеперь можешь вступить в нужные беседы', keyboard)
                        keyboard = create_keyboard(response)
                        send_message('Меню', keyboard)

                    elif response == 'нет, изменить':
                        send_message("Выбери направление", keyboard)
                    else:
                        message_id = vk.method('messages.getHistory', {'user_id': user_id})['count']

                        session.messages.send(
                            chat_id=5,
                            message='Новое сообщение в группе',
                            random_id=get_random_id(),
                            forward=json.dumps({'peer_id': user_id,
                                                'conversation_message_ids': message_id+1})
                        )

                        send_message("Мы скоро тебе ответим. Также ты можешь обратиться лично к любому руководителю "
                                     "Молодёжного самоуправления, для этого нажми кнопку 'Контакты'", keyboard)

        except KeyboardInterrupt:
            logger.info('Bot stopped')
            break
        except TimeoutError:
            logger.error('Ошибка времени ожидания. (Вероятно перезагрузка серверов VK)')
        except:
            logger.error(traceback.format_exc())
