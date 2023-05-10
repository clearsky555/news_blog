# админ заходит и создает новый пост, всем пользователям приходит рассылка, что пришёл новый пост
from apps.accounts.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from .models import Post

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site



# user_admin = User.objects.get(email='admin@gmail.com')
# User = get_user_model()
#
#
# @receiver(post_save, sender=Post)
# def send_post_notification(sender, instance, created, **kwargs):
#     if created and instance.author == user_admin:
#         print('создан пост')
#         emails = User.objects.exclude(email=user_admin.email).values_list('email', flat=True)
#         print(emails)
#         subject = 'Новый пост на сайте newsblog.com'
#         message = f'Здравствуйте! Администратор сайта newsblog.com создал новый пост: {instance.title}'
#         email = EmailMessage(subject, message, to=emails)
#         email.send(fail_silently=True)


# new
@receiver(post_save, sender=Post)
def email_notification(sender, instance, created, **kwargs):
    if created: # если был создан абсолютно новый пост
        DOMAIN = 'localhost:8000'
        email_subject = 'новые посты на newsblog.com'
        posts = Post.objects.filter(is_active=True).order_by('-created_add')[:3]
        message = render_to_string('new_posts_email.html', {'posts': posts, 'domain': DOMAIN})
        to_emails = User.objects.all().values_list('email', flat=True)
        email = EmailMessage(email_subject, message, to=to_emails)
        email.content_subtype = 'html'
        email.send()