from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def create_pdf(ingredients):

    response = HttpResponse(content_type='application/pdf,charset=utf8')
    canvas = Canvas(response, pagesize=A4)
    x, y = 10, 500
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf', 'utf-8'))

    canvas.setFont('DejaVuSans', 14)

    for ingredient in ingredients:
        canvas.drawString(
            x,
            y-30,
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
        )
        y += 50
    canvas.showPage()
    canvas.save()
    return response
