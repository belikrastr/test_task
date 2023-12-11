import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import get_template
import pdfkit
import qrcode
from django.db.models import Sum
import datetime

from .models import Item


class CashMachineView(APIView):
    def post(self, request):
        # Получение списка id товаров из запроса
        item_ids = request.data.get('items', [])

        # Получение объектов товаров
        items = Item.objects.filter(id__in=item_ids)

        # Вычисление общего количества товаров и общей стоимости
        total_quantity = items.aggregate(Sum('quantity'))['quantity__sum']
        total_price = items.aggregate(Sum('total_price'))['total_price__sum']

        # Генерация PDF-чека
        template = get_template('receipt_template.html')
        generated_at = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        html_content = template.render(
            {'items': items,
             'total_price': total_price,
             'total_quantity': total_quantity,
             'generated_at': generated_at
             }
        )

        # Создание папки media, если она не существует
        media_folder = os.path.join(settings.BASE_DIR, 'media')
        os.makedirs(media_folder, exist_ok=True)

        # Путь для сохранения PDF-чека
        pdf_path = os.path.join(media_folder, 'receipt_template.pdf')

        # Сохранение PDF-чека в папку media
        pdfkit.from_string(html_content, pdf_path)

        # Получение URL-адреса представления GetPDFView через reverse
        pdf_url = reverse('get_pdf', args=['receipt_template.pdf'])

        # Построение абсолютного URL
        pdf_uri = request.build_absolute_uri(pdf_url)

        # Генерация QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pdf_uri)
        qr.make(fit=True)

        # Создание QR-кода в виде изображения
        img = qr.make_image(fill_color="black", back_color="white")

        # Сохранение QR-кода в папку media
        qr_path = 'media/qrcode.png'
        img.save(qr_path)

        # Отправка QR-кода в ответе на запрос
        return Response({'qr_code': qr_path})


class GetPDFView(APIView):
    def get(self, request, file_name):
        # Формирование пути к файлу
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Проверка наличия файла
        if os.path.exists(file_path):
            # Отправка файла в ответе на запрос
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/pdf'
                )
                response['Content-Disposition'] = (
                    f'inline; filename="{file_name}"'
                )
                return response
        else:
            # Отправка ответа с кодом 404, если файл не найден
            return HttpResponse("File not found", status=404)
