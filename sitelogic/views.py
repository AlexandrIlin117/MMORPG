from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Publication, PublicationCategory, Category, Reaction
from .forms import PublicationForm
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


# Добавляем новое представление для создания Публикаций.
class PublicationCreate(CreateView):
    login_url = '/accounts/login/'
    permission_required = ('news.add_post',
                           'news.change_post')
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



def send_reaction(request):
    print('test')
    user = request.user
    text_reaction = request.POST.get('textfield', None)
    publication_id = request.POST.get('publication.pk')
    # Создаём отклик в базе данных
    Reaction.objects.create(reaction_text=text_reaction, reaction_to_publication_id=publication_id, reaction_user_id=user.id)
    return redirect('publication_list')
