from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from django.contrib.auth.models import *
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save, post_init
from rest_framework.fields import CurrentUserDefault


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
    short_text = models.TextField('Краткое описание', max_length=1000, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField('slug', max_length=15, unique=True)
    image = models.ImageField("Изображения", upload_to="post/", null=True, blank=True)
    edit_date = models.DateTimeField(
            "Дата редактирования",
            default=timezone.now,
            blank=True,
            null=True
    )
    # https://trello.com/c/e7HSIK5r/14-%D0%BF%D0%BE%D1%81%D1%82%D1%8B#
    # published_date = models.DateTimeField(
    #         "Дата публикации",
    #         default=timezone.now,
    #         blank=True,
    #         null=True
    # )

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
        ordering = ['sort', '-created_date']


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
        null=True,
    )
    child_comment = models.ManyToManyField(
        'self',
        verbose_name="Дочерний комментарий",
        blank=True,
        related_name='parent',
    )

    def __str__(self):
        return str(self.post)

    class Meta:
        ordering = ['author']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Goods(models.Model):
    name = models.TextField(max_length=1000)
    manufacturer = models.TextField(max_length=1000)
    issue_year = models.PositiveIntegerField('Год выпуска', null=True, blank=True)
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
    discount = models.PositiveSmallIntegerField('Скидка', default=0)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    slug = models.SlugField('url', max_length=30)
    short_text = models.CharField('Краткое описание', max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class PromoCode(models.Model):
    name = models.CharField('Название промо кода', max_length=20)
    description = models.CharField('Описание промо кода', max_length=1000)
    start_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField('Дата истечения действия', null=True, blank=True)
    discount_value = models.SmallIntegerField(
        'Скидка',
        default=0,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-expiration_date']
        verbose_name = 'Промо код'
        verbose_name_plural = 'Промо коды'


class Cart(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name="Покупатель",
        on_delete=models.CASCADE,
    )
    accepted = models.BooleanField("Принято к заказу", default=False)
    promo_code = models.ForeignKey(
        PromoCode,
        related_name='discount',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def get_goods(self):
        return GoodsInCart.objects.filter(cart=self.pk)

    @property
    def amount_items(self):
        total = 0
        for items in GoodsInCart.objects.filter(cart=self):
            total += items.amount
        return total

    @property
    def promo_price(self):
        if self.promo_code is not None:
            return self.amount_items-self.promo_code.discount_value
        else:
            return None

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class GoodsInCart(models.Model):
    good = models.ForeignKey(
        Goods,
        verbose_name='Товар',
        related_name='cart_goods',
        on_delete=models.DO_NOTHING,
    )
    cart = models.ForeignKey(
        Cart,
        related_name='goods_cart',
        verbose_name="Товар в корзине",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        'Единиц товара',
        default=1,
        validators=[MinValueValidator(1)])
    amount = models.PositiveIntegerField('Общая сумма', default=0)

    class Meta:
        ordering = ['cart']
        """"Проверка уникальности товара в рамках одной корзины"""
        constraints = [
            models.UniqueConstraint(fields=['good', 'cart'], name='goods unique')
        ]
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.amount = self.quantity * (self.good.price-self.good.discount)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.cart)


class FavoriteGood(models.Model):
    client = models.ForeignKey(
        User,
        verbose_name='В избранном у пользователя',
        on_delete=models.CASCADE,
    )
    good = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        verbose_name='Товар в избранном'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'good'], name='favorite unique')
        ]
        ordering = ['-client']
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

    def __str__(self):
        return str(self.client)


class Order(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="Комментарий к заказу", max_length=1000, null=True)
    done = models.BooleanField(verbose_name="Заказ выполнен", default=False)
    date = models.DateTimeField('Дата заказа', default=timezone.now)
    amount = models.PositiveIntegerField('Итоговая сумма заказа', default=0)
    receiver_name = models.CharField("Имя и отчетство получателя", max_length=70, null=True)
    receiver_surname = models.CharField('Фамилия', max_length=100, null=True)
    receiver_mail = models.EmailField('Почта получателя', null=True)
    is_save_info = models.BooleanField('Сохранить информацию заказа', default=False)
    delivery_address = models.CharField('Адрес доставки', max_length=1000, null=True)
    
    def save(self, *args, **kwargs):
        self.amount = self.cart.amount_items
        if self.cart.promo_code is not None:
            self.amount -= self.cart.promo_code.discount_value
        self.cart.accepted = True
        self.cart.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.cart)

    class Meta:
        ordering = ['cart']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """Создаём пустую корзину для пользователя при успешной регистрации."""
    if created:
        blank_cart = Cart()
        blank_cart.customer = User.objects.get(username=instance)
        #blank_cart.good = ""
        blank_cart.save()


# @receiver(post_save, sender=GoodsInCart)
# def update_cart_amount(instance, **kwargs):
#     cart = Cart.objects.get(customer__username=instance, accepted=False)
#     goods = GoodsInCart.objects.filter(cart=cart)
#     total = 0
#     for items in goods:
#         total += items.amount
#     cart.total_amount = total
#     cart.save()



