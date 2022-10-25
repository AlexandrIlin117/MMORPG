from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Publication, PublicationCategory, Category, Reaction, OneTimeCode, User
from .forms import PublicationForm, BaseRegisterForm
from .filters import PublicationFilter
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
# Create your views here.

class PublicationList(ListView):
    model = Publication
    ordering = '-publication_time_publication'
    template_name = 'main_page.html'
    context_object_name = 'id'


class PrivatePage(LoginRequiredMixin,ListView):
    model = Publication
    ordering = '-publication_time_publication'
    template_name = 'private_page.html'
    context_object_name = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PublicationFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['reaction'] = Reaction.objects.all()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(PrivatePage, self).get_context_data(**kwargs)
    #     context['reaction'] = Reaction.objects.all()
    #     return context


class PublicationCreate(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    permission_required = ('sitelogic.add_publication',
                           'sitelogic.change_publication')
    redirect_field_name = ('publication_list')
    form_class = PublicationForm
    model = Publication
    template_name = 'create.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        if self.request.path =='/sitelogic/create/':
             publication.publication_announcement_news = 'НО'
             return super().form_valid(form)
        if self.request.path =='/announcement/create/':
             publication.publication_announcement_news = 'ОБ'
             return super().form_valid(form)




class PublicationUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/accounts/login/'
    permission_required = ('sitelogic.add_publication',
                           'sitelogic.change_publication')
    redirect_field_name = ('publication_list')
    form_class = PublicationForm
    model = Publication
    template_name = 'create.html'
    success_url = reverse_lazy('private_page_list')

# Представление удаляющее товар.
class PublicationDelete(LoginRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    permission_required = ('sitelogic.add_publication',
                           'sitelogic.change_publication',
                           'sitelogic.delete_publication')
    redirect_field_name = ('publication_list')
    model = Publication
    template_name = 'delete.html'
    success_url = reverse_lazy('private_page_list')

class ReactionDelete(LoginRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    permission_required = ('sitelogic.add_post',
                           'sitelogic.change_post')
    model = Reaction
    template_name = 'delete.html'
    success_url = reverse_lazy('private_page_list')


@login_required
def send_reaction(request):
    user = request.user
    text_reaction = request.POST.get('textfield', None)
    publication_id = request.POST.get('publication.pk')
    # Создаём отклик в базе данных
    Reaction.objects.create(reaction_text=text_reaction, reaction_to_publication_id=publication_id, reaction_user_id=user.id)
    return redirect('publication_list')


@login_required
def change_status(request):
    react_id = request.POST.get('reaction_id')
    react_new_status = request.POST.get('change_status')
    # Меняем статус отклика в базе данных
    Reaction.objects.filter(id=react_id).update(reaction_status=react_new_status)
    session_response_to_reation = Reaction.objects.filter(id=react_id)[0]
    print(session_response_to_reation)

    #Отправляем письмо:
    if session_response_to_reation.reaction_status == 'ПР':
        session_response_to_publication = session_response_to_reation.reaction_to_publication
        print(f'Пользователь написавщий отклик - {session_response_to_reation.reaction_user}')
        session_response_to_reaction_user = session_response_to_reation.reaction_user
        print(f'Автор объявления - {session_response_to_publication.publication_author}')
        session_response_to_author = session_response_to_publication.publication_author
        print(f'Текст отклика - {session_response_to_reation.reaction_text}')
        session_response_to_reaction_text = session_response_to_reation.reaction_text
        print(f'Заголовок объявления - {session_response_to_publication.publication_header_announcement_news}')
        session_response_to_header = session_response_to_publication.publication_header_announcement_news
        print(session_response_to_reaction_user.email)

        html = render_to_string(
            'Response_Reaction.html',
            {'session_announcement': session_response_to_reaction_user, 'session_response_to_reaction_text': session_response_to_reaction_text,
             'session_response_to_author': session_response_to_author, 'session_response_to_header': session_response_to_header},
            # передаем в шаблон любые переменные
        )
        msg = EmailMultiAlternatives(
            subject=f'Уважаемый {session_response_to_reaction_user.first_name} {session_response_to_reaction_user.last_name} ({session_response_to_reaction_user}) на ваш отклик пришёл ответ!',
            from_email='ilin.run1979@yandex.ru',
            to=[session_response_to_reaction_user.email]  # отправляем всем из списка
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        print('OK')

        return redirect('private_page_list')
    return redirect('private_page_list')


def signup(request):
    if request.method == "POST":
        print("А вот сейчас POST")
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            data = form
            # print(form)
            # verification_email(data)
            # form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            print(form.cleaned_data.get('email'))
            print(form.cleaned_data.get('username'))
            print(form.cleaned_data.get('first_name'))
            print(form.cleaned_data.get('last_name'))
            print(form.cleaned_data.get('password1'))
            print(form.cleaned_data.get('password2'))
            session_code = get_random_string(length=32)
            OneTimeCode.objects.create(one_email=form.cleaned_data.get('email'),
                                       one_username=form.cleaned_data.get('username'),
                                       one_first_name=form.cleaned_data.get('first_name'),
                                       one_last_name=form.cleaned_data.get('last_name'),
                                       one_password=form.cleaned_data.get('password1'),
                                       one_check_code=session_code,
                                    )
            # Отправляем код на почту;

            html = render_to_string(
                'send_code.html',
                {'session_code': session_code,
                 },
                # передаем в шаблон любые переменные
            )
            msg = EmailMultiAlternatives(
                subject=f'Код подтверждения!',
                from_email='ilin.run1979@yandex.ru',
                to=[form.cleaned_data.get('email')]  # отправляем всем из списка
            )
            msg.attach_alternative(html, 'text/html')
            msg.send()

            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('ver_email_page')
        else:
            print("Форма не валидна")
            form = BaseRegisterForm()
        return render(request, 'signup.html', {'form': form})
    if request.method == "GET":
        form = BaseRegisterForm()

    return render(request, 'signup.html', {'form': form})


def verification_email(data):
    print(type(data))
    print("тест")
    inform = data
    username = inform.cleaned_data.get('username')
    password = inform.cleaned_data.get('password1')
    print(username)
    print(password)
    ver_email()
    input("Для продолжения намите Enter")
    redirect('ver_email_page')
    # return render('signup.html')

def ver_email(request):
    email = request.POST.get('email', None)
    code = request.POST.get('code', None)
    print(email)
    print(code)
    check_user = OneTimeCode.objects.all()
    for next_user in check_user:
        print(next_user)
        if email == next_user.one_email and code == next_user.one_check_code:
            user = User.objects.create_user(
                username=next_user.one_username,
                password=next_user.one_password,
                first_name=next_user.one_first_name,
                last_name=next_user.one_last_name,
                email=next_user.one_email,
            )
            redirect('publication_list')
    return render(request, 'ver_email_page.html')


