import random
import requests
import vk_api

def send_doc(event_peer_id, docx):
    """
    Отправляет готовый(собраный) документ пользователю
    :param event_peer_id: передать id пользователся, которому был сделан документ
    :param docx: передать название готового документа для пользователя
    :return: отправляет готовый доклад
    """

    # Документ собранный открывается, готовый для отправки
    openFile = open(docx, 'rb')

    # Авторизация группы в Вконтакте с помощью токена
    token = "082f0cf6b4235f530b59eda2d166b89955861632ff559c6a16352f97625eab33402fe481f36fd453fcc22"
    vk_session = vk_api.VkApi(token=token)
    session_api = vk_session.get_api()

    # Получение ссылки на место на сервере Вконтакте
    uploadFile = vk_session.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": '{}'.format(event_peer_id)})['upload_url']

    # Отправка файла на сервер Вконтакте
    requestsFile = requests.post(uploadFile, files={'file': openFile}).json()

    # Сохранение файла на сервере Вконтакте
    savefail = vk_session.method('docs.save', requestsFile)

    # Ссылка на сохранённый файл на сервере Вконтакте
    a = savefail['doc']['owner_id']
    b = savefail['doc']['id']

    # Отправка собраного документа(docx) пользователю
    session_api.messages.send(peer_id=event_peer_id,
                              message='''Пожалуйста, твой доклад в твоих руках 😋

И ещё! Просьба оставить отзыв о работе с ботом, замеченных багах или просто написать свои предложения по улучшению 🙏
👉Туть: https://vk.com/topic-189633572_40235641''',
                              random_id=random.randint(-2147483648, +2147483648),
                              attachment='doc{0}_{1}'.format(a, b))