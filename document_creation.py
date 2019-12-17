from docxtpl import DocxTemplate
from send_docx import send_doc
from paragraph import paragraphs_break

def creation_template(tema, klass, name, gorod, text, school, pol, id):
    """
    Подстановка данных в Шаблон
    Создание титульного листа
    :param tema: Передать тему доклада
    :param klass: Передать класс пользователя
    :param name: Передать ФИО
    :param gorod: Передать город
    Создание доклада
    :param text: Передать текст Доклада
    :return:
    """

    # Информация для вставки в шаблон
    shablon = {'tema': tema,
               'klass': klass,
               'name': name,
               'gorod': gorod,
               'school': school,
               'pol': pol
               }

    # Открытие шаблона документа
    doc = DocxTemplate("shablon.docx")

    # Вставка в шаблон предоставленной информации
    doc.render(shablon)

    # Сохранение готового документа
    doc.save("report.docx")

    # Вставка текста в доклад с 14 шрифтом
    paragraphs_break(text)

    # Отправить готовый файл пользователю
    send_doc(event_peer_id=id, docx='doklad.docx')


