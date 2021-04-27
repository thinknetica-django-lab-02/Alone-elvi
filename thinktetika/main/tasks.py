import random

from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import Product, Subscriber, sending_html_mail, SMSConfirm

from thinktetika.celery import celery_app
from thinktetika import settings

from celery import shared_task

from main.email import new_products_by_scheduler_email_template
from main.sms.twilio_sms import send_sms


@celery_app.task(name="sending_new_products_by_scheduler", routing_key="sending_new_products_by_scheduler")
def sending_new_products_by_scheduler():
    """Метод ответственный за отправку сообщений пользователям о новинках недели"""
    year, week, _ = now().isocalendar()

    emails = [e.user.email for e in Subscriber.objects.all()]
    products = Product.objects.filter(pub_date__iso_year=year, pub_date__week=week)
    subject = new_products_by_scheduler_email_template.subject
    text_content = new_products_by_scheduler_email_template.text_content
    html_content = new_products_by_scheduler_email_template.html_content
    for product in products:
        text_content += f"{product.title}, "
        html_content += f"""<p>{product.title}</p><br>"""
    from_email = new_products_by_scheduler_email_template.from_email
    sending_html_mail(subject, text_content, html_content, from_email, emails)


@celery_app.task
def send_phone_code(phone_number, user_id):
    number = random.randint(1000, 9999)
    status = send_sms(phone_number, number)
    sms = SMSConfirm.objects.create(code=number, status=status)
    user = User.objects.get(id=user_id)
    user.smslog_set.add(sms)
