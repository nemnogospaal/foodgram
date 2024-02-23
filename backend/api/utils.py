from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

# def download_shopping_list(shopping_list):
#     file = 'shopping_list.txt'
#     text = []
#     for position in shopping_list:
#         name = position['ingredient__name']
#         measurement_point = position['ingredient__measurement_unit']
#         amount = position['all_ingredients']
#         text.append(f'{name} | {measurement_point} ---- {amount}')
#     content = '\n'.join(text)
#     response = HttpResponse(content, content_type='text/plain,charset=utf8')
#     response['Content-Disposition'] = f'attachment; filename="{file}"'
#     return response

def create_pdf(ingredients):
    response = HttpResponse(content_type='application/pdf')
    canvas = Canvas(response, pagesize=A4)
    x, y = 50, 80

    canvas.drawString(x, y, 'Список покупок:')
    canvas.setFont('List', 16)

    for i, recipe in enumerate(ingredients, start=1):
        canvas.drawString(
            x,
            y + 20,
            f'{i} {recipe["recipe__ingredient__name"]} - '
            f'{recipe["amount"]}'
            f'{recipe["recipe__ingredient__measurement_unit"]}'
        )
        y += 20
        canvas.showPage()
        canvas.save()
        return response
