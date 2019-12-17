from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from document_creation import creation_template
from doc_cr import creation_template_1
from wiki import wiki
import vk_api
import random

# Авторизация Вконтакте
token = "082f0cf6b4235f530b59eda2d166b89955861632ff559c6a16352f97625eab33402fe481f36fd453fcc22"
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()

# Создаёт longpoll Вконтакте
longpoll = VkBotLongPoll(vk_session, 189633572)

# Словарь в котором ключ это id пользователя, и объект это словарь с состоянием вопроса пользователя, данных для доклада
sost_id = {
}

# Словарь в котором ключ это id пользователя, а объект текст доклада
text_dict = {
}

# Список текстов от пользователя для объединения после ввода несколькими сообщениями
text_user = []


# Создания клавиатуры для сообщений
def create_keyboard(payload):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
    if payload != None:
        keyboard.add_button('Выход', payload=2, color=VkKeyboardColor.PRIMARY)
        if payload == 3:
            keyboard.add_button('Готово', payload=3, color=VkKeyboardColor.PRIMARY)
        elif payload == 1:
            keyboard.add_button('Далее', payload=3, color=VkKeyboardColor.PRIMARY)
        elif payload == 4:
            keyboard.add_button('Мужской♂', payload=4, color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Женский♀', payload=5, color=VkKeyboardColor.PRIMARY)
        elif payload == 5:
            keyboard.add_button('Авто', payload=6, color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Свой текст', payload=7, color=VkKeyboardColor.PRIMARY)
        elif payload == 6:
            keyboard.add_button('Свой текст', payload=7, color=VkKeyboardColor.PRIMARY)
    else:
        keyboard.add_button('Начать', payload=1, color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


# Слушает longpoll Вконтакте, принимает новые сообщения от пользователей
while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            #print('Текст сообщения: ' + str(event.obj.text))

            # Опускает текст сообщения для прочтение ботом
            response = event.obj.text.lower()

            # Передаёт None если клавиатура была не использованна
            if event.obj.payload != None:
                payload = int(event.obj.payload)
            else:
                payload = None

            # Создание клавиатуры, передача в аргумент какую клавиатуру нужно вызвать
            keyboard = create_keyboard(payload)

            # Проверка на наличие пользователя в списке sost_id, для предотвращения использование "Начать" в заполнение
            if not event.obj.peer_id in sost_id:
                if not response == 'начать' and payload == None:
                    session_api.messages.send(peer_id=event.obj.peer_id,
                                              message='Неизвестная команда',
                                              random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)

            # Если пользователь передал команду "Начать" начать работу логике бота
            if response == 'начать' or payload == 1:
                if not event.obj.peer_id in sost_id:
                    if response == 'начать':
                        keyboard = create_keyboard(1)
                        session_api.messages.send(peer_id=event.obj.peer_id,
                                                  message='''Приветствую 👻 
Ну что, приступим к составлению твоего доклада? 
✅Готов? Жми "Далее" 
⛔Если решишь сделать другой доклад или напортачишь с данными, кликай на "Выход"''',
                                                  random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)
                elif payload == 1:
                    session_api.messages.send(peer_id=event.obj.peer_id,
                                              message='''Приветствую 👻 
Ну что, приступим к составлению твоего доклада? 
✅Готов? Жми "Далее" 
⛔Если решишь сделать другой доклад или напортачишь с данными, кликай на "Выход"''',
                                              random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)

            # Запуск заполнение данных для создания доклада
            # При команде "далее" создаёт словарь в словаре sost_id, в котром ключ это id, а объект это словарь данных
            elif response == 'далее' or payload == 1:
                if not event.obj.peer_id in sost_id:
                    id = event.obj.peer_id
                    sost_id.setdefault(id, {'sost': '0', 'tema': '', 'klass': '', 'name': '', 'gorod': '',
                                            'school': '', 'pol': ''})
                    keyboard = create_keyboard(2)
                    session_api.messages.send(peer_id=event.obj.peer_id,
                                              message='''📝Приступим к заполнению титульного листа!
👉Напиши, пожалуйста, название своего учебного заведения (смотри пример)''',
                                              random_id=random.randint(-2147483648, +2147483648),
                                              attachment=['photo-189633572_457239051', 'photo-189633572_457239050'],
                                              keyboard=keyboard)

            # При команде "выход" удаляет из sost_id пользователя и точки остановки и данные введёные пользователем
            # Начинает с начала и кнопки "Начать"
            elif response == 'выход' or payload == 2:
                keyboard = create_keyboard(None)
                sost_id.pop(event.obj.peer_id, None)
                session_api.messages.send(peer_id=event.obj.peer_id,
                                          message='Данные удаленны, можете начать сначало - нажав кнопку "Начать"',
                                          random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)

            # Записывает данные согласно точки остановки конкретного пользователя
            elif event.obj.peer_id in sost_id:
                if sost_id[event.obj.peer_id]['sost'] == '0':
                    sost_id[event.obj.peer_id]['school'] = event.obj.text
                    keyboard = create_keyboard(2)
                    session_api.messages.send(peer_id=event.obj.peer_id, message='''Теперь, набери тему доклада 🤔''',
                                              random_id=random.randint(-2147483648, +2147483648),
                                              attachment=['photo-189633572_457239049', 'photo-189633572_457239048'],
                                              keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '1'

                elif sost_id[event.obj.peer_id]['sost'] == '1':
                    sost_id[event.obj.peer_id]['tema'] = event.obj.text
                    keyboard = create_keyboard(4)
                    session_api.messages.send(peer_id=event.obj.peer_id, message='''Понял! 🌸
Укажи свой пол🔥''',
                                              random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '2'

                # Выявление пола c помощью клавиатуры, подставляет согласно выбраной кнопке пол в шаблоне
                elif sost_id[event.obj.peer_id]['sost'] == '2':
                    keyboard = create_keyboard(2)
                    if response == 'мужской♂':
                        sost_id[event.obj.peer_id]['pol'] = 'Выполнил: ученик'
                    elif response == 'женский♀':
                        sost_id[event.obj.peer_id]['pol'] = 'Выполнила: ученица'
                    session_api.messages.send(peer_id=event.obj.peer_id,
                                              message='''Хорошо, понял тебя 😌
👉Теперь введи класс/группу, как показано в образце.''',
                                              random_id=random.randint(-2147483648, +2147483648),
                                              attachment=['photo-189633572_457239053', 'photo-189633572_457239052'],
                                              keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '3'

                elif sost_id[event.obj.peer_id]['sost'] == '3':
                    sost_id[event.obj.peer_id]['klass'] = event.obj.text
                    keyboard = create_keyboard(2)
                    session_api.messages.send(peer_id=event.obj.peer_id, message='''Почти готово 😊
Напиши свои фамилию, имя 👀''',
                                              random_id=random.randint(-2147483648, +2147483648),
                                              attachment=['photo-189633572_457239054', 'photo-189633572_457239055'],
                                              keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '4'

                elif sost_id[event.obj.peer_id]['sost'] == '4':
                    sost_id[event.obj.peer_id]['name'] = event.obj.text
                    keyboard = create_keyboard(2)
                    session_api.messages.send(peer_id=event.obj.peer_id, message='''Ну и на последок 🙃
Город, где учишься🏡''',
                                              random_id=random.randint(-2147483648, +2147483648),
                                              attachment=['photo-189633572_457239058', 'photo-189633572_457239056'],
                                              keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '5'
                    text_dict.setdefault(event.obj.peer_id, [])

                elif sost_id[event.obj.peer_id]['sost'] == '5':
                    sost_id[event.obj.peer_id]['gorod'] = event.obj.text
                    keyboard = create_keyboard(5)
                    session_api.messages.send(peer_id=event.obj.peer_id,
                                              message='''Прекрасно, с титульником покончено!😜
📋Далее, давай определимся с самим докладом:

✔Если нет времени, доклад нужен срочно или просто лень морочиться — кликай "Авто"
✔Если хочешь ввести свой уникальный текст или подобного нет в Интернете — вибирай клавишу "Свой текст"''',
                                              random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)
                    sost_id[event.obj.peer_id]['sost'] = '6'

                # Логика авто поиска в Википедиа по теме или ввод самому если не нашлось по теме
                elif sost_id[event.obj.peer_id]['sost'] == '6':
                    if response == "авто":
                        keyboard = create_keyboard(2)
                        sost_id[event.obj.peer_id]['sost'] = '8'
                        session_api.messages.send(peer_id=event.obj.peer_id,
                                                  message='''🔍Коротко и чётко введи тему Доклада!''',
                                                  random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)
                    elif response == "свой текст":
                        keyboard = create_keyboard(3)
                        sost_id[event.obj.peer_id]['sost'] = '7'
                        session_api.messages.send(peer_id=event.obj.peer_id, message='''📝Вводи или вставляй текст доклада.
✅Когда закончишь, не забудь нажать на кнопку "Готово"😉''',
                                                  random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)
                # Если не находит Авто режим по теме, то предлогает ввести свой текст
                elif response == "свой текст":
                    keyboard = create_keyboard(3)
                    sost_id[event.obj.peer_id]['sost'] = '7'
                    session_api.messages.send(peer_id=event.obj.peer_id, message='''📝Вводи или вставляй текст доклада.
                ✅Когда закончишь, не забудь нажать на кнопку "Готово"😉''',
                                              random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)

                # Авто режим поиска по теме
                elif sost_id[event.obj.peer_id]['sost'] == '8':
                    keyboard = create_keyboard(6)
                    tema_docl = event.obj.text

                    # Записывает в переменные для передачи в функцию создания доклада по шаблону,
                    # Запись в переменные происходит из словаря sost_id
                    tema = sost_id[event.obj.peer_id]['tema']
                    klass = sost_id[event.obj.peer_id]['klass']
                    name = sost_id[event.obj.peer_id]['name']
                    gorod = sost_id[event.obj.peer_id]['gorod']
                    school = sost_id[event.obj.peer_id]['school']
                    pol = sost_id[event.obj.peer_id]['pol']
                    creation_template_1(tema=tema, klass=klass, name=name, gorod=gorod, pol=pol, school=school)

                    # Вставка найденого текста в доклад, либо возврат ошибки(False)
                    docc = wiki(id=event.obj.peer_id, tema_docl=tema_docl)
                    if docc == False:
                        session_api.messages.send(peer_id=event.obj.peer_id, message='''⚠Ошибка! Попробуй ещё разок.
Если что, можно воспользоваться функцией "Свой текст"
Вводи тему коротко и корректно (как указано в примере)⚠''', random_id=random.randint(-2147483648, +2147483648),
                                                  attachment='photo-189633572_457239064', keyboard=keyboard)
                    else:
                        # Очистка переменных состояние пользователя и данных для доклада
                        sost_id.pop(event.obj.peer_id, None)
                        text_dict.pop(event.obj.peer_id, None)
                        text_user.clear()
                        text_finish = None

                # При режиме "Свой текст" ожидание кнопки готово для создание доклада, запись текста в словарь где
                # ключ это id пользователя
                elif response != 'готово':
                    if sost_id[event.obj.peer_id]['sost'] == '7':
                        text_dict[event.obj.peer_id].append(event.obj.text)
                        keyboard = create_keyboard(3)
                        session_api.messages.send(peer_id=event.obj.peer_id, message='Записал✔',
                                                  random_id=random.randint(-2147483648, +2147483648), keyboard=keyboard)

                elif response == 'готово':
                    # Объединяет переданные тексты в один единый текст
                    text_finish = ''.join(text_dict[event.obj.peer_id])

                    # Записывает в переменные для передачи в функцию создания доклада по шаблону, запись в переменные
                    # происходит из словаря (sost_id)
                    tema = sost_id[event.obj.peer_id]['tema']
                    klass = sost_id[event.obj.peer_id]['klass']
                    name = sost_id[event.obj.peer_id]['name']
                    gorod = sost_id[event.obj.peer_id]['gorod']
                    school = sost_id[event.obj.peer_id]['school']
                    pol = sost_id[event.obj.peer_id]['pol']
                    creation_template(tema=tema, klass=klass, name=name, gorod=gorod,
                                      text=text_finish, id=event.obj.peer_id, pol=pol, school=school)

                    # Удаляет пользователя из переменной созданий доклада и статуса остановки после завершения и
                    # отправки пользователю
                    sost_id.pop(event.obj.peer_id, None)
                    text_dict.pop(event.obj.peer_id, None)
                    text_user.clear()
                    text_finish = None