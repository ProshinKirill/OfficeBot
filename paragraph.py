import docx
from docx.shared import Pt
import paragraph

def paragraphs_break(text):
    """
    Вставляет текст от пользователя, учитывая пробелы
    :param text: текст от пользователя
    :return: Сохраняет новый конечный файл
    """
    document = docx.Document('report.docx')
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    paragraph.style = document.styles['Normal']
    document.add_paragraph(text)
    document.save('doklad.docx')