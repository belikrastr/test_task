# Cash Register. «Кассовый аппарат»
### Описание
«Кассовый аппарат» для вымышленного магазина. Формирует чек в формате PDF. Так же формирует ссылку на этот PDF-файл и кодирует его в QR-код, по которому можно получить чек.

### Технологии
- Python 3 
- Django 
- Django REST Framework

### Подготовка к запуску проекта
- Склонировать репозиторий на локальную машину
```bash
git clone git@github.com:belikrastr/test_task.git
```
- Перейти в директорию test_task
```bash
cd test_task/
```
- Cоздать и активировать виртуальное окружение
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
- Обновить пакеты pip
```bash
python -m pip install --upgrade pip
```
- Установить зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```
- Перейти в директорию my_project
```bash
cd my_project/
```
- Выполнить миграции
```bash
python manage.py migrate
```


### Запуск проекта 
- При запуске приложения указывайте IP-адрес вашей машины в локальной сети. Например: python manage.py runserver 192.168.0.1:8000
```bash
python manage.py runserver 192.168.1.68:8000
```

### Примеры запросов к API.
- Получение чека(.pdf)
###
GET http://192.168.1.68:8000/get_pdf/receipt_template.pdf


- Формирование чека
###
POST http://192.168.1.68:8000/cash_register/
Content-Type: application/json
```js
{
	"items": [1, 2, 3]
}
```

### Автор проекта
Беликов Владимир - [Telegram](https://t.me/belikrastr) - belikrastr@yandex.ru

Project Link: [https://github.com/belikrastr/test_task.git](https://github.com/belikrastr/test_task.git)
