from django.conf import settings
from django.db import models
from expense.models import Expense
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Создание модели
class Category(models.Model):
    user = models.ForeignKey(User, related_name='category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return self.name

    @property
    def total_expense_cost(self):
        expenses = Expense.ojects.all().filter(category=self.id)
        return sum([expenses.amount for expense in expenses])


# Сигналы, которые автоматически создают категории по умолчанию при создании нового пользователя
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs) -> None:
    if created:
        Category.objects.create(user=instance, name='Забота о себе')
        Category.objects.create(user=instance, name='Зарплата')
        Category.objects.create(user=instance, name='Здоровье и фитнес')
        Category.objects.create(user=instance, name='Кафе и рестораны')
        Category.objects.create(user=instance, name='Машина')
        Category.objects.create(user=instance, name='Образование')
        Category.objects.create(user=instance, name='Отдых и развлечения')
        Category.objects.create(user=instance, name='Платежи, комиссии')
        Category.objects.create(user=instance, name='Покупки: одежда, техника')
        Category.objects.create(user=instance, name='Продукты')
        Category.objects.create(user=instance, name='Проезд')
