from django.urls import path
# Импортируем созданное нами представление
from .views import PublicationCreate, PublicationList, PrivatePage,PublicationDelete,PublicationUpdate,ReactionDelete
from  .views import send_reaction, change_status
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup, verification_email,ver_email


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем постам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('news/', PublicationList.as_view(), name='publication_list'),
    path('private_page/', PrivatePage.as_view(), name='private_page_list'),
    path('create/', PublicationCreate.as_view(), name='publication_create'),
    path('<int:pk>/private_page/publication_update', PublicationUpdate.as_view(), name='publication_edit'),
    path('<int:pk>/delete/', PublicationDelete.as_view(), name='publication_delete'),
    path('<int:pk>', ReactionDelete.as_view(), name='reaction_delete'),
    path('news/send_reaction', send_reaction, name='send_reaction'),
    path('private_page/change_status', change_status, name='change_status'),

    # path('login/',
    #      LoginView.as_view(template_name = 'sign/login.html'),
    #      name='login'),
    # path('logout/',
    #      LogoutView.as_view(template_name = 'sign/logout.html'),
    #      name='logout'),
    path('signup/',signup,name='signup'),
    path('ver_email_page/verification_email',ver_email,name='ver_email_page'),
]