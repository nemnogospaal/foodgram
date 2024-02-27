from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def create_pdf(ingredients):
    response = HttpResponse(content_type='application/pdf')
    canvas = Canvas(response, pagesize=A4)
    x, y = 10, 10
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

    canvas.drawString(x, y, 'Список покупок:')
    canvas.setFont('Vera', 14)

    for ingredient in ingredients:
        canvas.drawString(
            x,
            y,
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amount"]}'
            f'{ingredient["ingredient__measurement_unit"]}'
        )
        y += 20
        canvas.showPage()
        canvas.save()
        return response
