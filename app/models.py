from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from django.contrib.auth.models import *
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save, post_init


class Category(MPTTModel):
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField('url', max_length=100)
    description = models.TextField("Описание категории", max_length=1000, default="Описание категории", blank=True)
    parent = TreeForeignKey(
        'self',
        verbose_name='Parent_category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='Child_category'
    )
    published = models.BooleanField("Отображение категории", default=0)
    sort = models.PositiveIntegerField('Сортировка по приоритету', default=10)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=1000)
    text = models.TextField(max_length=3000)
    subtitle = models.TextField('Краткое описание', max_length=1000, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField('slug', max_length=15, unique=True)
    image = models.ImageField("Изображения", upload_to="post/", null=True, blank=True)
    edit_date = models.DateTimeField(
            "Дата редактирования",
            default=timezone.now,
            blank=True,
            null=True
    )
    published_date = models.DateTimeField(
            "Дата публикации",
            default=timezone.now,
            blank=True,
            null=True
    )

    category = models.ForeignKey(
            Category,
            verbose_name='Категория',
            on_delete=models.CASCADE,
        )
    published = models.BooleanField("Опубликован?", default=True)
    viewed = models.PositiveIntegerField("Просмотры", default=0)
    status = models.BooleanField("Для зарегистрированных", default=False)
    sort = models.PositiveIntegerField("Сортировка по приоритету", default=10)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост",
        verbose_name_plural = "Посты"
        ordering = ['sort', '-published_date']


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE
    )
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(default=True)
    post = models.ForeignKey(
        Post,
        verbose_name='Посты',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.post

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Goods(models.Model):
    name = models.TextField(max_length=1000)
    manufacturer = models.TextField(max_length=1000)
    issue_year = models.PositiveIntegerField('Год выпуска', null=True, blank=True)  #допилить, не отображается при сериализации
    sort = models.PositiveIntegerField("Сортировка по приоритету", default=10)
    published_date = models.DateTimeField(
            "Дата публикации",
            default=timezone.now,
            blank=True,
            null=True
    )
    photo = models.ImageField("Изображения", upload_to="goods/", null=True, blank=True)
    left = models.PositiveIntegerField('Остаточнок количество', default=0)
    description = models.TextField(max_length=1000)
    price = models.PositiveIntegerField('Цена', default=0)
    discount = models.PositiveSmallIntegerField('Скидка', default=0) #допилить, не отображается при сериализации
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    slug = models.SlugField('url', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Cart(models.Model):
    customer = models.OneToOneField(
        User,
        verbose_name="Покупатель",
        on_delete=models.CASCADE,
    )
    goods = models.ManyToManyField(
        Goods,
        verbose_name="Товары в корзине",
        related_name='goods',
    )
    comment = models. CharField('Комментарий к заказу', max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        ordering = ['-id']
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """Создаём пустую корзину для пользователя при успешной регистрации."""
    if created:
        blank_cart = Cart()
        blank_cart.customer = User.objects.get(username=instance)
        blank_cart.good = ""
        blank_cart.comment = ""
        blank_cart.save()
    """Необходимо реализовать удаление корзины при удалении пользователя!"""
