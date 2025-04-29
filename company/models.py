from django.db import models

class ResidentialComplex(models.Model):
    name = models.CharField("Название ЖК", max_length=200)
    description = models.TextField("Описание")
    price = models.IntegerField("Средняя цена за м²")
    completion_date = models.DateField("Срок сдачи")
    image = models.ImageField(upload_to="complexes/")

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    message = models.TextField("Сообщение")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

from django.db import models

from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=100, default='Без категории')  # Значение по умолчанию
    preview = models.TextField()
    full_text = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

    def __str__(self):
        return self.title


