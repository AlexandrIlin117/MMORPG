from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from .models import Publication, PublicationCategory, Category, User, Reaction
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст


@receiver(post_save,sender=Reaction)
def post_save_recent_article(sender, instance,action="post_add", *args, **kwargs, ):
    print(instance)
    if action == "post_add":
        session_reaction = instance
        print(instance.reaction_to_publication)
        session_publication = instance.reaction_to_publication
        print(f'Пользователь написавщий отклик - {session_reaction.reaction_user}')
        session_reaction_user = session_reaction.reaction_user
        print(f'Отклик написан пользователю - {session_publication.publication_author}')
        session_publication_author = session_publication.publication_author
        print(f'заголовок объявления - {session_publication.publication_header_announcement_news}')
        session_announcement = session_publication.publication_header_announcement_news
        print(f'Индефикатор объявления - {session_publication.id}')
        session_publication_id = session_publication.id
        print(session_publication_author.email)


        html = render_to_string(
            'Response_Notification.html', {'session_announcement': session_announcement, 'session_publication_id': session_publication_id,
                                        'session_reaction_user': session_reaction_user, 'session_publication_author': session_publication_author},
            # передаем в шаблон любые переменные
        )
        msg = EmailMultiAlternatives(
            subject=f'Уважаемый {session_publication_author.first_name} {session_publication_author.last_name} ({session_publication_author}) есть отклик на ваше объявление!',
            from_email='ilin.run1979@yandex.ru',
            to=[session_publication_author.email]  # отправляем всем из списка
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        print('OK')
