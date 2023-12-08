from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
import qrcode
from io import BytesIO

from .models import Item


class CashMachineView(APIView):
    def post(self, request):
        # Получение списка id товаров из запроса
        item_ids = request.data.get('items', [])

        # Получение объектов товаров
        items = Item.objects.filter(id__in=item_ids)

        # Генерация PDF-чека
        template = get_template('receipt_template.html')
        html_content = template.render({'items': items})
        pdf = pdfkit.from_string(html_content, False)

        # Сохранение PDF-чека в папку media
        pdf_path = 'media/invoice.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf)

        # Генерация QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pdf_path)
        qr.make(fit=True)

        # Создание QR-кода в виде изображения
        img = qr.make_image(fill_color="black", back_color="white")

        # Сохранение QR-кода в папку media
        qr_path = 'media/qrcode.png'
        img.save(qr_path)

        # Отправка QR-кода в ответе на запрос
        return Response({'qr_code': qr_path})
