from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

FONT_SIZE = 14
X_POS = 10
Y_POS = 700
INDENTATION = 30


def create_pdf(ingredients):

    response = HttpResponse(content_type='application/pdf,charset=utf8')
    canvas = Canvas(response, pagesize=A4)
    x_position, y_position = X_POS, Y_POS
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf', 'utf-8'))

    canvas.setFont('DejaVuSans', FONT_SIZE)

    for ingredient in ingredients:
        canvas.drawString(
            x_position,
            y_position - INDENTATION,
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
        )
        y_position += INDENTATION
    canvas.showPage()
    canvas.save()
    return response
