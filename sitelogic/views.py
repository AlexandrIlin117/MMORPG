from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Publication, PublicationCategory, Category, Reaction
from .forms import PublicationForm
from .filters import PublicationFilter
# Create your views here.

class PublicationList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Publication
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-publication_time_publication'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'main_page.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'id'
    # paginate_by = 5  # вот так мы можем указать количество записей на странице

    # # Переопределяем функцию получения списка статей;
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PublicationFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список статей;
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context



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
    #permission_denied_message ='Хотите создавать статьи и новости?!
    # Воспользуйтесь нашим специальным предложением на странице своего профиля!'
    redirect_field_name = ('publication_list')
    # Указываем нашу разработанную форму
    form_class = PublicationForm
    # модель товаров
    model = Publication
    # и новый шаблон, в котором используется форма.
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
    return redirect('private_page_list')
