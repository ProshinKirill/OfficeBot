from docxtpl import DocxTemplate

def creation_template_1(tema, klass, name, gorod, school, pol):
    """
    Для Википедиа
    Подстановка данных в Шаблон
    Создание титульного листа
    :param tema: Передать тему доклада
    :param klass: Передать класс пользователя
    :param name: Передать ФИО
    :param gorod: Передать город
    :return: Собранный титульный лист в файл
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