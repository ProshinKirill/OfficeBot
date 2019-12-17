import re
import wikipediaapi
from paragraph import paragraphs_break
from send_docx import send_doc

def wiki(id, tema_docl):
    """
    Находит доклад по теме в Википедиа, если находит присылает
    готовый доклад, если нет то возвращает False
    :param id: id пользователя
    :param tema_docl: тема доклада
    :return: Гототвый доклад, либо False
    """
    # Язык, формат
    wiki_wiki = wikipediaapi.Wikipedia(
        language='ru',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    # Находит в вики страницу с заданной темой (wiki -> str)
    p_wiki = wiki_wiki.page(tema_docl)

    # Если нашлось присылает файл, если нет то False
    if len(p_wiki.text) != 0:
        text = p_wiki.text
        # Уборка в конце доклада не нужных ссылок и тд
        try:
            item_position = text[:text.index('См. также')]
        except ValueError:
            item_position = text[:text.index('Примечания')]

        # Ставит пробел после [.,!?]
        finish_text = re.sub(r'([.,!?])', r' \1 ', item_position)

        # Вставка текста в доклад найденный в Википедиа
        paragraphs_break(text=item_position)

        # Отправляет готовый файл пользователю
        send_doc(event_peer_id=id, docx='doklad.docx')
    else:
        return False