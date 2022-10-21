from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)        #Категории новостей/статей темы, которые они отражают;

    def __str__(self):
        return f'{self.category_name}'


class Publication(models.Model):
    announcement = 'ОБ'
    news = 'НО'
    ANNOUCEMENT_NEWS = [
        (announcement, 'Объявление'),
        (news, 'Новость'),
    ]
    publication_author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_announcement_news = models.CharField(max_length=2,
                                choices=ANNOUCEMENT_NEWS,
                                default=news)
    publication_time_publication = models.DateTimeField(auto_now_add=True)
    publication_header_announcement_news = models.CharField(max_length=255)
    publication_content = RichTextUploadingField()
    publication_categories = models.ManyToManyField(Category, through='PublicationCategory')

    def get_absolute_url(self):
        return reverse('publication_list')


class PublicationCategory(models.Model):
    pc_publication = models.ForeignKey(Publication, on_delete=models.CASCADE)           #связь «один ко многим» с моделью Publication;
    pc_category = models.ForeignKey(Category, on_delete=models.CASCADE)   #связь «один ко многим» с моделью Category;

    def __str__(self):
        return f'Публикация: {self.pc_publication}\nКатегория: {self.pc_category}'



class Reaction(models.Model):
    considered = 'РА'
    accept = 'ПР'
    rejected = 'ОТ'
    STATUS_REACTION = [
        (considered, 'Рассматривается'),
        (accept, 'Принят'),
        (rejected, 'Отклонён'),
    ]
    reaction_to_publication = models.ForeignKey(Publication, on_delete=models.CASCADE)   # связь «один ко многим» с моделью Publication;
    reaction_user = models.ForeignKey(User, on_delete=models.CASCADE)      # связь «один ко многим» со встроенной моделью User;
    reaction_text = models.TextField(default="Текст отклика отсутствует")   # текст отклика;
    reaction_time_publication = models.DateTimeField(auto_now_add=True)    # дата и время создания отклика;
    reaction_status = models.CharField(max_length=2,
                                choices=STATUS_REACTION,
                                default=considered)






