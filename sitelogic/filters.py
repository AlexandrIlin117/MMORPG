from django_filters import FilterSet, DateFilter, ChoiceFilter
from .models import Publication, Category,Reaction
import django.forms
import django.forms.widgets



class PublicationFilter(FilterSet):
    # Для того что бы была возможность выбирать категорию из выпадающего списка при условии что категорий будет произвольное
    # количество и изначально поле модели и поле формы представляет собою простой CharField делаем следующее:
    # - подготавливаем для поля choices список с имеющимися категориями;
    # - загружаем все элементы(категории в нашем случае) модели Category в столбце 'category_name';
    # - это query set поэтому в цикле достаём каждый его елемент представляющий словарь;
    # - количество словарей будет равно числу категорий и каждый будет иметь вид {'category_name': 'Политика'};
    # - дальше небольшая эквилибристика n_k = list((list(next_category.items()))[0])
    # - получаем пару "ключ-значение" это словарь спрятаный в dict_item;
    # - из dict_item получаем список используя первый list;
    # - из него достаём единственный кортеж и вторым листом делаем из него список;
    # - в этом списке меняеи 1вый елемент на значение второго и снова делаем список кортежем :);
    # - сам  от себя в шоке :) ;
    # - всё это добавляется к формирующемуся списку ARTICLE_NEWS;
    # - остаётся только применить к полю фильтр ChoiceFilter;

    ANNOUCEMENT_NEWS = []
    list_category = Category.objects.all().values('category_name')
    for next_category in list_category:
        # print(next_category.items())
        n_k = list((list(next_category.items()))[0])
        n_k[0] = n_k[1]
        # print(n_k)
        n_k = tuple(n_k)
        ANNOUCEMENT_NEWS.append(n_k)
    # print(ARTICLE_NEWS)

    publication_time_publication = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        ))

    publication_categories__category_name = ChoiceFilter(
        # lookup_expr='exact',
        choices=ANNOUCEMENT_NEWS,
        widget=django.forms.Select(
            attrs={
                'type': 'choices'
            },
        ))

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Publication
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           'id': ['icontains'],
           'publication_header_announcement_news': ['icontains'],
           'publication_announcement_news': ['icontains'],
           'publication_author__username': ['icontains'],
       }
