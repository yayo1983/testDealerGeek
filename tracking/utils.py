import xlwt
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import os


def choices(em):
    return [(e.name, e.value) for e in em]


def send_user_mail(email, id):
    try:
        subject = 'Correo de aviso de paquete arrivado'
        template = get_template(os.path.join(settings.BASE_DIR, 'Templates/email_template.html'))
        content = template.render({
            'email': email,
            'id': id
        })

        message = EmailMultiAlternatives(subject=subject, body='', from_email=settings.EMAIL_HOST_USER, to=[email])
        message.attach_alternative(content, 'text/html')
        message.send()
        return True
    except:
        return False


def put_status_e_to_end(data):
    for index, obj in enumerate(data):
        if obj['status'] == 'E':
            data.append(obj)
            data.pop(index)
    return data


def export_users_xls(response, columns, rows, nameSheet='default'):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(nameSheet)  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response