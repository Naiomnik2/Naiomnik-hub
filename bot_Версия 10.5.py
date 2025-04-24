import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import json
import time
import threading
from datetime import datetime, timedelta
import pytz
import re

vk_session = vk_api.VkApi(token='vk1.a.xkhS77ySTQElRlJSkLHLk-3tCAAnLYyqhZqQQwaci5wszrGkbmQhSBy3SndQipkLilvn-oH0vL71Raj-NCaSRNqq0KlzEO9ZMlDHD-wKuYLuwNlOqcoxByOMS2ZtByMQCsAYuoSMgGulqBN2hiHILiAAGUXcOKnD9TjIBPQUq0WRQybkEYw8d-Zzyho9PlYU9w6lL8_U5aAfjHTP9483VA')
longpoll = VkBotLongPoll(vk_session, 186994521)

def sender(chat_id, text, message_id=None):
    chat_id_with_prefix = 2000000000 + chat_id  # Для группового чата нужно добавить 2000000000
    send_params = {
        'peer_id': chat_id_with_prefix,  # Используем 'peer_id' для беседы
        'message': text,
        'random_id': int(time.time())
    }

    if message_id:  # Если нужно ответить на сообщение
        send_params['forward'] = json.dumps({
            "peer_id": chat_id_with_prefix,
            "conversation_message_ids": [message_id],  # Указываем ID сообщения
            "is_reply": True  # Указываем, что это ответ на сообщение
        })

    vk_session.method('messages.send', send_params)









def get_user_id_from_link(link):
    match = re.search(r'(id\d+|[\w.]+)$', link)
    if match:
        user_identifier = match.group(1)

        if user_identifier.startswith('id'):
            return int(user_identifier[2:])
        else:
            try:
                response = vk_session.method('users.get', {'user_ids': user_identifier})
                return response[0]['id']
            except vk_api.exceptions.VkApiError as e:
                return None
    return None

def get_user_id_from_link(link):
    match = re.search(r'(id\d+|[\w.]+)$', link)
    if match:
        user_identifier = match.group(1)

        if user_identifier.startswith('id'):
            return int(user_identifier[2:])
        else:
            try:
                response = vk_session.method('users.get', {'user_ids': user_identifier})
                return response[0]['id']
            except vk_api.exceptions.VkApiError as e:
                return None
    return None

def get_chat_title(chat_id):
    try:
        response = vk_session.method('messages.getConversationsById', {'peer_ids': 2000000000 + chat_id})
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['chat_settings']['title']
    except vk_api.exceptions.VkApiError as e:
        return f"Беседа с ID {chat_id}"
    return f"Беседа с ID {chat_id}"

def kick_user(user_id, chat_id):
    try:
        vk_session.method('messages.removeChatUser', {'chat_id': chat_id, 'user_id': user_id})
    except vk_api.exceptions.VkApiError as e:
        pass  # Пропустить блок в случае исключения
    except Exception as ex:
        pass  # Пропустить блок в случае исключения




def handle_kick_command_sledaki(event, command_text, chat_list, group_id):
    chat_id = event.chat_id
    peer_id = event.object.message['peer_id']

    link = command_text.split(' ')[1]  # Ссылка должна идти после команды !кик
    user_id = get_user_id_from_link(link)
    
    if not user_id:
        sender(chat_id, "Не удалось получить ID пользователя.", event.message['conversation_message_id'])
        return
    
    
    # Преобразуем group_id в список, если это одиночное значение
    if not isinstance(group_id, list):
        group_id = [group_id]  # Преобразуем в список для унификации логики

    # Перебираем все group_id и выполняем необходимые действия
    for gid in group_id:
        try:
            #API Платона
            vk_session = vk_api.VkApi(token='vk1.a.UFM5HkF4sv5Rt_SgqgVh5ZLyZMHffvCc91g5GvZZKHlpAgOg1v7XDkEE9e2oRZbCQdn26VRhfQivN-ZZEAJHuVhb_aRseyJnt7dkSDSMpZqTQ7rGSoANG9ThJMfH-MuylSxeehwnK7jBJiRpzc2KzEbjIfcyDuMVTTp4xumLk2z2RRvqm-uQCpd0S6A86wABcUxofkErjlD98hNolFVDig')
            # Забираем права у пользователя в каждом сообществе
            vk_session.method('groups.editManager', {
                'group_id': gid,
                'user_id': user_id,
                'role': 0  # Установка роли на 0 - убирает все права
            })
        except vk_api.exceptions.VkApiError as e:
            #Апи бота
            vk_session = vk_api.VkApi(token='vk1.a.xkhS77ySTQElRlJSkLHLk-3tCAAnLYyqhZqQQwaci5wszrGkbmQhSBy3SndQipkLilvn-oH0vL71Raj-NCaSRNqq0KlzEO9ZMlDHD-wKuYLuwNlOqcoxByOMS2ZtByMQCsAYuoSMgGulqBN2hiHILiAAGUXcOKnD9TjIBPQUq0WRQybkEYw8d-Zzyho9PlYU9w6lL8_U5aAfjHTP9483VA')
            #sender(chat_id, f"Не удалось убрать права у пользователя в сообществе  https://vk.com/club{gid}: {e}", event.message['conversation_message_id'])
            continue

    chats_where_kicked = []
    chats_with_admin_rights = []
    #Апи бота
    vk_session = vk_api.VkApi(token='vk1.a.xkhS77ySTQElRlJSkLHLk-3tCAAnLYyqhZqQQwaci5wszrGkbmQhSBy3SndQipkLilvn-oH0vL71Raj-NCaSRNqq0KlzEO9ZMlDHD-wKuYLuwNlOqcoxByOMS2ZtByMQCsAYuoSMgGulqBN2hiHILiAAGUXcOKnD9TjIBPQUq0WRQybkEYw8d-Zzyho9PlYU9w6lL8_U5aAfjHTP9483VA')

    # Перебор конкретных значений chat_list
    for chat_index in chat_list:
        try:
            members = vk_session.method('messages.getConversationMembers', {'peer_id': 2000000000 + chat_index})

            if 'items' not in members:
                continue

            member_info = next((m for m in members['items'] if m['member_id'] == user_id), None)

            if member_info:
                is_admin = 'is_admin' in member_info and member_info['is_admin']
                chat_title = get_chat_title(chat_index)  # Получаем название беседы

                if is_admin:
                    chats_with_admin_rights.append(chat_title)
                else:
                    kick_user(user_id, chat_index)  # Передаем chat_id без прибавления
                    chats_where_kicked.append(chat_title)

        except vk_api.exceptions.VkApiError as e:
            pass  # Пропустить блок в случае исключения
        except Exception as ex:
            pass  # Пропустить блок в случае исключения

    # Формируем сообщение о результате
    kicked_message = "Пользователь был успешно исключен из следующих бесед:\n"
    if chats_where_kicked:
        kicked_message += '\n'.join([f"{i + 1}) {chat}" for i, chat in enumerate(chats_where_kicked)]) + "\n"
    else:
        kicked_message = "❗⛔❗ (Error) ❗⛔❗ \nПользователь не состоит ни в одной из бесед.\n"

    if chats_with_admin_rights:
        admin_rights_message = "\n❗ Не удалось исключить пользователя в беседах, где у него есть права администратора:\n"
        admin_rights_message += '\n'.join([f"{i + 1}) {chat}" for i, chat in enumerate(chats_with_admin_rights)])
        kicked_message += admin_rights_message
        
    kicked_message += '\n\n'

    # Флаг для отслеживания, исключен ли пользователь хотя бы из одного сообщества
    user_kicked = False

    # Перебираем все group_id и выполняем необходимые действия
    for gid in group_id:
        try:
            # Проверка, является ли пользователь членом сообщества
            vk_session = vk_api.VkApi(token='vk1.a.UFM5HkF4sv5Rt_SgqgVh5ZLyZMHffvCc91g5GvZZKHlpAgOg1v7XDkEE9e2oRZbCQdn26VRhfQivN-ZZEAJHuVhb_aRseyJnt7dkSDSMpZqTQ7rGSoANG9ThJMfH-MuylSxeehwnK7jBJiRpzc2KzEbjIfcyDuMVTTp4xumLk2z2RRvqm-uQCpd0S6A86wABcUxofkErjlD98hNolFVDig')

            is_member = vk_session.method('groups.isMember', {
                'group_id': gid,
                'user_id': user_id
            })

            # Если пользователь состоит в сообществе, исключаем его
            if is_member:
                vk_session.method('groups.removeUser', {
                    'group_id': gid,
                    'user_id': user_id
                })
                kicked_message += f"✅ Пользователь успешно исключен из сообщества https://vk.com/club{gid} \n"
                user_kicked = True  # Устанавливаем флаг, что пользователь был исключен

        except vk_api.exceptions.VkApiError as e:
            # Если произошла ошибка, логируем ее и продолжаем
            vk_session = vk_api.VkApi(token='vk1.a.xkhS77ySTQElRlJSkLHLk-3tCAAnLYyqhZqQQwaci5wszrGkbmQhSBy3SndQipkLilvn-oH0vL71Raj-NCaSRNqq0KlzEO9ZMlDHD-wKuYLuwNlOqcoxByOMS2ZtByMQCsAYuoSMgGulqBN2hiHILiAAGUXcOKnD9TjIBPQUq0WRQybkEYw8d-Zzyho9PlYU9w6lL8_U5aAfjHTP9483VA')
            continue

    # Если пользователь не был исключен ни из одного сообщества
    if not user_kicked:
        kicked_message += "❗⛔❗ (Error) ❗⛔❗ \nПользователь не состоит ни в одном из сообществ.\n"

    # API бота
    vk_session = vk_api.VkApi(token='vk1.a.xkhS77ySTQElRlJSkLHLk-3tCAAnLYyqhZqQQwaci5wszrGkbmQhSBy3SndQipkLilvn-oH0vL71Raj-NCaSRNqq0KlzEO9ZMlDHD-wKuYLuwNlOqcoxByOMS2ZtByMQCsAYuoSMgGulqBN2hiHILiAAGUXcOKnD9TjIBPQUq0WRQybkEYw8d-Zzyho9PlYU9w6lL8_U5aAfjHTP9483VA')

    # Отправка сообщения о результате в чат
    sender(chat_id, kicked_message, event.message['conversation_message_id'])








import time  # Для добавления задержки

def check_admin_rights(chat_index):
    try:
        # Запрос информации о беседе
        response = vk_session.method('messages.getConversationsById', {'peer_ids': 2000000000 + chat_index})

        # Проверка наличия данных о беседе
        if 'items' in response and len(response['items']) > 0:
            conversation = response['items'][0]

            # Проверяем права администратора для сообщества
            if 'chat_settings' in conversation:
                admins = conversation['chat_settings'].get('admin_ids', [])
                if -186994521 in admins:
                    return True
        return False
    except vk_api.exceptions.VkApiError as e:
        print(f"Ошибка при проверке прав администратора в беседе {chat_index}: {e}")
        return False
    except Exception as ex:
        print(f"Неожиданная ошибка при проверке чата {chat_index}: {ex}")
        return False

def handle_check_command(event):
    chat_id = event.chat_id
    peer_id = event.object.message['peer_id']

    # Сообщение об инициализации проверки
    sender(chat_id, "Начинаю проверку прав администратора в беседах от 1 до 140.", event.message['conversation_message_id'])

    # Перебор чатов от 1 до 120
    for chat_index in range(1, 141):
        is_admin = check_admin_rights(chat_index)
        if is_admin:
            result_message = f"✅ Админка есть. ID беседы: {chat_index}."
        else:
            result_message = f"❌ Админки нет. ID беседы: {chat_index}.\n@id637957523 (Anastasia_MacAlister), @iid0901 (Dmitriy_Polanski), @laplandec125 (Alexandr_Silych)."
            # Отправка сообщения о результате в текущий чат
            sender(chat_index, result_message)

        

        # Логирование результата
        print(f"Лог: {result_message}")

        # Задержка между запросами, чтобы избежать возможных ограничений
        time.sleep(1.0)






















# Переменная для хранения результата
cached_result = None

# Переменная для хранения времени последнего использования команд
cooldowns = {
    '!сос': 0,
    '!сос 3+': 0,
    '!созыв': 0
}
cooldown_time = 300  # 5 минут в секундах

# Функция для проверки кулдауна
def is_on_cooldown(command):
    return time.time() - cooldowns[command] < cooldown_time

# Функция для получения оставшегося времени кулдауна в минутах и секундах
def get_time_left(command):
    time_left = cooldown_time - (time.time() - cooldowns[command])
    minutes = int(time_left // 60)  # Получаем минуты
    seconds = int(time_left % 60)  # Получаем секунды
    return minutes, seconds

# Функция для обновления данных
def update_data():
    global cached_result
    url = 'https://script.google.com/macros/s/AKfycbwB0g8jf8f7kxrViXGEEMj36aMvpyx3VCVUmXY-KaQxn6VmhxwGCpE9zDckCtwzDt_3YQ/exec'
    while True:
        try:
            response = requests.get(url)
            data = response.content
            cached_result = json.loads(data)  # Обновляем кеш, данные в формате списка списков
        except:
            cached_result = [["Данные ещё не получены. Попробуйте позже."], ["Данные ещё не получены. Попробуйте позже."], ["Данные ещё не получены. Попробуйте позже."]]
        time.sleep(60)  # Обновляем данные раз в минуту

# Функция для рассчета времени следующей отправки
def calculate_next_send_time(current_time):
    # Определяем время начала и конца интервала
    start_time = current_time.replace(hour=12, minute=15, second=0, microsecond=0)
    end_time = current_time.replace(hour=1, minute=15, second=0, microsecond=0) + timedelta(days=1)

    # Если текущее время за пределами интервала (после 1:15), добавляем день к start_time
    if current_time > end_time:
        start_time += timedelta(days=1)

    # Определяем ближайшее допустимое время отправки
    interval = timedelta(minutes=30)
    next_send_time = start_time
    while next_send_time <= current_time:
        next_send_time += interval

    # Если next_send_time больше 1:15 следующего дня, устанавливаем его на 12:15 следующего дня
    if next_send_time.hour == 1 and next_send_time.minute == 15:
        next_send_time = start_time + timedelta(days=1)

    return next_send_time

# Функция для отправки системного уведомления
def send_system_notification():
    global cached_result
    while True:
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        next_send_time = calculate_next_send_time(current_time)
        
        while True:
            try:
                # Рассчитываем оставшееся время до следующего интервала
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                wait_time = (next_send_time - current_time).total_seconds()

                if wait_time > 0:
                    time.sleep(wait_time)

                if cached_result and len(cached_result) > 2:
                    message = f"[Системное оповещение]\n{cached_result[2][0]}"
                    sender(2, message)

                # Переопределяем следующее время отправки
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                next_send_time = calculate_next_send_time(current_time)

            except Exception as e:
                time.sleep(3)
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                next_send_time = calculate_next_send_time(current_time)

# Запуск обновления данных и системных уведомлений в отдельных потоках
threading.Thread(target=update_data, daemon=True).start()
threading.Thread(target=send_system_notification, daemon=True).start()






from datetime import datetime, timedelta
import pytz
import threading
import time

# Функция для расчета времени следующей отправки уведомления в 15:00, 18:00 или 21:00
def calculate_next_notification_time(current_time):
    # Задаем список фиксированных времени уведомлений
    notification_times = [
        current_time.replace(hour=15, minute=0, second=0, microsecond=0),
        current_time.replace(hour=18, minute=0, second=0, microsecond=0),
        current_time.replace(hour=21, minute=0, second=0, microsecond=0)
    ]
    
    # Находим ближайшее допустимое время отправки
    next_notification_time = None
    for time_point in notification_times:
        if time_point > current_time:
            next_notification_time = time_point
            break
    
    # Если текущее время больше 21:00, устанавливаем следующую отправку на 15:00 следующего дня
    if next_notification_time is None:
        next_notification_time = notification_times[0] + timedelta(days=1)
    
    return next_notification_time

# Функция для отправки системного уведомления
def send_new_system_notification():
    global cached_result
    while True:
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        next_notification_time = calculate_next_notification_time(current_time)
        
        while True:
            try:
                # Рассчитываем оставшееся время до следующего интервала
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                wait_time = (next_notification_time - current_time).total_seconds()

                if wait_time > 0:
                    time.sleep(wait_time)

                if cached_result and len(cached_result) > 4:
                    message = f"[Системное оповещение]\n{cached_result[4][0]}"
                    sender(2, message)

                # Переопределяем следующее время отправки
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                next_notification_time = calculate_next_notification_time(current_time)

            except Exception as e:
                time.sleep(3)
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))
                next_notification_time = calculate_next_notification_time(current_time)

# Запуск второго потока для нового уведомления
threading.Thread(target=send_new_system_notification, daemon=True).start()



























TARGET_USER_ID = -168319586
# Обработка событий
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                chat_id = event.chat_id
                msg = event.message['text'].lower()
                message_id = event.message['conversation_message_id']  # Получаем conversation_message_id
                user_id = event.object.message['from_id']  # ID пользователя

                # Проверяем на "!сос"
                if msg in ['!сос', '!cjc']:
                    if chat_id == 2:
                        if not is_on_cooldown('!сос'):
                            if cached_result:
                                response_text = cached_result[0][0]
                                sender(chat_id, response_text, message_id=message_id)  # Добавляем message_id
                                if response_text != "На сервере достаточно администраторов.\nМассовый созыв не требуется.":
                                    if response_text != "Данные ещё не получены. Попробуйте позже.":
                                        cooldowns['!сос'] = time.time()  # Обновляем время последнего вызова только в случае успешного получения данных
                                        cooldowns['!созыв'] = time.time()  # Обновляем время кулдауна
                                        cooldowns['!сос 3+'] = time.time()  # Обновляем время кулдауна
                            else:
                                sender(chat_id, "Данные ещё не получены. Попробуйте позже.", message_id=message_id)
                        else:
                            minutes, seconds = get_time_left('!сос')
                            sender(chat_id, f"Вы сможете использовать '!сос' через {minutes} мин. {seconds} сек.", message_id=message_id)

                # Проверяем на "!сос 3+"
                elif msg in ['!сос 3+', '!cjc 3+']:
                    if chat_id == 2:
                        if is_on_cooldown('!сос'):
                            minutes, seconds = get_time_left('!сос')
                            sender(chat_id, f"Вы сможете использовать '!сос 3+' через {minutes} мин. {seconds} сек.", message_id=message_id)
                        elif not is_on_cooldown('!сос 3+'):
                            if cached_result and len(cached_result) > 1:
                                sender(chat_id, cached_result[1][0], message_id=message_id)  # Добавляем message_id
                                if cached_result[1][0] != "Данные ещё не получены. Попробуйте позже.":
                                    cooldowns['!сос 3+'] = time.time()  # Обновляем время кулдауна
                            else:
                                sender(chat_id, "Данные ещё не получены или недостаточно данных.", message_id=message_id)
                        else:
                            minutes, seconds = get_time_left('!сос 3+')
                            sender(chat_id, f"Вы сможете использовать '!сос 3+' через {minutes} мин. {seconds} сек.", message_id=message_id)

                # Проверяем на "!созыв"
                elif msg in ['!созыв', '!cjpsd']:
                    if chat_id == 2:
                        if not is_on_cooldown('!созыв'):
                            if cached_result and len(cached_result) > 2:
                                sender(chat_id, cached_result[2][0], message_id=message_id)  # Добавляем message_id
                                if cached_result[2][0] != "Данные ещё не получены. Попробуйте позже.":
                                    cooldowns['!созыв'] = time.time()  # Обновляем время кулдауна
                            else:
                                sender(chat_id, "Данные ещё не получены или недостаточно данных.", message_id=message_id)
                        else:
                            minutes, seconds = get_time_left('!созыв')
                            sender(chat_id, f"Вы сможете использовать '!созыв' через {minutes} мин. {seconds} сек.", message_id=message_id)

                # Проверяем на "!таблица"
                elif msg in ['!таблица', '!nf,kbwf']:
                    if chat_id == 2:
                        sender(chat_id, "Админ таблица: https://vk.cc/cvwS5I \n\nТаблица 'кто когда зайдет': https://vk.cc/cuWniP \n• Гугл форма 'кто когда зайдет': https://vk.cc/cu8ws1", message_id=message_id)
                
              
                elif msg.strip() == 'у пользователя нет предупреждений.' and TARGET_USER_ID == user_id:
                    if chat_id == 2:
                        sender(chat_id, "@naiomnik2 (Rostislav_Imenov), у данного администратора накопилось 5/5 предупреждений за игнорирование созывов. Пришло время выдать наказание. 😡", message_id=message_id)
                        
                 # Проверяем на "!отчет"
                elif msg in ['!отчет']:
                    if chat_id == 1:  # Проверка на чат номер 3
                        sender(chat_id, cached_result[3][0], message_id=message_id)  # Добавляем message_id
                
                # Проверяем на "!id chat"
                #elif msg == '!id':
                #    sender(chat_id, f"ID этого чата: {chat_id}")
                    
                    
                elif msg.startswith("!проверка"):
                    if chat_id == 3:
                        sender(chat_id, "Проверка запущена.", message_id=message_id)
                        handle_check_command(event)
                        
                
                # Проверка команды !кик
                elif msg.startswith("!снять"):
                    if chat_id == 3: #админка
                        group_id = 168319586
                        chat_list = [2, 3, 4, 6, 7, 8, 9, 10, 11, 130]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)
                        
                    elif chat_id == 34: # ЧО + следаки
                        group_id = [201608788, 196132489, 193278551, 191215126, 193259114, 213030675, 193278568, 213030692, 193092494, 192691601, 195355311, 193278591, 191215108, 213030656, 193092341, 193092522, 190832343]
                        chat_list = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 131]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 26:  # Старший состав Армия
                        group_id = 192691601
                        chat_list = [27, 96, 90, 94, 95, 89, 26, 93, 60, 67, 109, 29, 30, 91, 97, 131]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 40:  # Старший состав РЖД
                        group_id = 193259114
                        chat_list = [42, 98, 127, 124, 114, 40, 85, 125, 126, 68, 67, 21, 31, 66, 24]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 119:  # Старший состав ГИБДД-П
                        group_id = 191215126
                        chat_list = [102, 64, 116, 58, 112, 119, 67, 21, 31, 13, 19, 91]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 12:  # Старший состав ГИБДД-Н
                        group_id = 191215108
                        chat_list = [41, 103, 121, 12, 104, 120, 108, 67, 21, 31, 13, 19, 91]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 71:  # Старший состав ГИБДД-М
                        group_id = 190832343
                        chat_list = [100, 129, 128, 25, 71, 67, 21, 31, 13, 19, 91]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 107:  # Старший состав ГУВД-П
                        group_id = 193278568
                        chat_list = [99, 59, 65, 106, 105, 107, 117, 65, 67, 21, 31, 19, 91, 23]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 45:  # Старший состав ГУВД-М
                        group_id = 193278591
                        chat_list = [101, 46, 45, 86, 115, 87, 67, 21, 31, 19, 91, 23]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 62:  # Старший состав ГУВД-Н
                        group_id = 193278551
                        chat_list = [82, 80, 84, 62, 83, 81, 67, 21, 31, 19, 91, 23]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 52:  # Старший состав ЦГБ-П
                        group_id = 193092341
                        chat_list = [88, 53, 54, 55, 52, 67, 21, 31, 109, 22, 20, 50, 131]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 57:  # Старший состав ОКБ-М
                        group_id = 193092522
                        chat_list = [77, 56, 78, 79, 57, 67, 21, 31, 109, 22, 20, 50, 131]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 51:  # Старший состав ЦГБ-Н
                        group_id = 193092494
                        chat_list = [49, 28, 48, 47, 51, 67, 21, 31, 109, 22, 20, 50, 131]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 122:  # Старший состав ОПГ-П
                        group_id = 213030656
                        chat_list = [123, 122, 72, 70, 63, 67, 44, 43, 21, 31]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 113:  # Старший состав ОПГ-М
                        group_id = 213030675
                        chat_list = [73, 14, 113, 111, 110, 67, 44, 43, 21, 31]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)

                    elif chat_id == 75:  # Старший состав ОПГ-Н
                        group_id = 213030692
                        chat_list = [74, 61, 92, 76, 75, 69, 67, 44, 43, 21, 31]
                        sender(chat_id, "Процесс запущен...", message_id=message_id)
                        handle_kick_command_sledaki(event, msg, chat_list, group_id)


                        
                

    except:
        time.sleep(3)