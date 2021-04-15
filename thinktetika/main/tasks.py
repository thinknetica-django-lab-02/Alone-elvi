from celery import shared_task
from thinktetika.celery import celery_app

from django.utils.timezone import now
from .models import Product, Subscriber, sending_html_mail

from main.email import new_products_by_scheduler_email_template


@celery_app.task
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
