from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import *


def create_category():
    category = Category.objects.create(name='main', slug='main')
    return category


def create_good(category):
    good = Goods.objects.create(
        name='test',
        manufacturer='test_man',
        description='test_desc',
        category=category,
        slug='test_slug',
        price=10
    )
    return good


def create_user(client):
    user = User.objects.create_superuser('admin_user', 'fegesg@test.ru', '123456')
    client.force_authenticate(user=user)
    return user


def create_post(author, category):
    post = Post.objects.create(
        title='test_post',
        text='test_text',
        slug='test_slug',
        author=author,
        category=category
    )
    return post


def create_comment(author, post):
    comment = Comment.objects.create(author=author, text='test_text', post=post)
    return comment


def create_promo():
    promo = PromoCode.objects.create(
        name='test',
        discount_value=5
    )
    return promo


class FavoriteTests(APITestCase):

    def test_create_favorite(self):
        """Добавление в избранное"""
        category = create_category()
        good = create_good(category)
        user = create_user(self.client)
        data = {
            'good': good.id
        }
        request = self.client.post(
            reverse('favorite_create'),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteGood.objects.count(), 1)
        self.assertEqual(FavoriteGood.objects.get().good, good)

    def test_get_favorite(self):
        """Получение избранного"""
        user = create_user(self.client)
        request = self.client.get(
            reverse('favorite_create'),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_favorite(self):
        """Удаление из избранного"""
        FavoriteGood.objects.create(good=create_good(create_category()), client_id=create_user(self.client).id)
        good = FavoriteGood.objects.values('good').get()
        request = self.client.delete(
            reverse('favorite_delete', args=[good['good']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FavoriteGood.objects.count(), 0)


class CategoryTests(APITestCase):
    def test_create_category(self):
        """Создание категории"""
        user = create_user(self.client)
        data = {
            "name": "test_cat",
            "description": "test_desc"}
        request = self.client.post(
            reverse('category_create'),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().name, 'test_cat')
        request = self.client.get(
            reverse('category_list'),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 4)
        category = Category.objects.values('id').first()
        request = self.client.get(
            reverse('category_ops', args=[category['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 5)
        data = {"name": "put_test_cat"}
        request = self.client.put(
            reverse('category_ops', args=[category['id']]),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().name, 'put_test_cat')
        data = {"description": "new_test_desc"}
        request = self.client.patch(
            reverse('category_ops', args=[category['id']]),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().description, 'new_test_desc')
        request = self.client.delete(
            reverse('category_ops', args=[category['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class PostsTests(APITestCase):
    def test_posts(self):
        user = create_user(self.client)
        category = create_category()
        data = {
            "title": "test_post",
            "text": "test_text",
            "slug": "test_slug",
            "category": 1}
        request = self.client.post(
            reverse('post_create'),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'test_post')
        request = self.client.get(
            reverse('posts_get')
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        post = Post.objects.values('id').first()
        request = self.client.get(
            reverse('post_edit', args=[post['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 8)
        data = {'text': 'new_test_text'}
        request = self.client.patch(
            reverse('post_edit', args=[post['id']]),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.first().text, 'new_test_text')
        data = {
            'title': 'new_test_title',
            "text": "new_test_text",
            "slug": "new_test_slug",
            }
        request = self.client.put(
            reverse('post_edit', args=[post['id']]),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.first().title, 'new_test_title')
        request = self.client.delete(
            reverse('post_edit', args=[post['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class TestGoods(APITestCase):
    def test_goods(self):
        user = create_user(self.client)
        category = create_category()
        data = {
            'name': 'test_good_name',
            'manufacturer': 'test_man',
            'category': 1,
            'short_text': 'test_short',
            'slug': 'test_slug',
            'description': 'test_desc'
        }
        request = self.client.post(
            reverse('good_create'),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goods.objects.count(), 1)
        self.assertEqual(Goods.objects.first().slug, 'test_slug')
        request = self.client.get(
            reverse('good_create')
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = self.client.get(
            reverse('goods_by_cat', args=[category.id])
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 4)
        good = Goods.objects.values('id').first()
        request = self.client.get(
            reverse('good_edit', args=[good['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 14)
        data = {'name': 'new_test_name'}
        request = self.client.patch(
            reverse('good_edit', args=[good['id']]),
            data,
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Goods.objects.first().name, 'new_test_name')
        request = self.client.delete(
            reverse('good_edit', args=[good['id']]),
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Goods.objects.count(), 0)


class TestComments(APITestCase):
    def test_create_comment(self):
        """Добавление комментария"""
        user = create_user(self.client)
        post = create_post(user, create_category())
        data = {
            'author': user.id,
            'text': 'test_text',
            'post': post.id
        }
        response = self.client.post(
            reverse('create_comment'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().post, post)

    def test_get_comment(self):
        """Получение комментария"""
        response = self.client.get(reverse('create_comment'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_comment(self):
        """Редактирование комментария"""
        data = {'text': 'new_test_text'}
        user = create_user(self.client)
        comment = create_comment(author=user, post=create_post(author=user, category=create_category()))
        response = self.client.patch(
            reverse('comment_ops', args=[comment.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.first().text, 'new_test_text')

    def test_delete_comment(self):
        """Удаление комментария"""
        user = create_user(self.client)
        comment = create_comment(author=user, post=create_post(author=user, category=create_category()))
        response = self.client.delete(
            reverse('comment_ops', args=[comment.id]),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_create_subcomment(self):
        """Добавление дочернего комментария"""
        user = create_user(self.client)
        data = {'text': 'subcomment_text', 'author': user.id}
        comment = create_comment(author=user, post=create_post(author=user, category=create_category()))
        response = self.client.post(
            reverse('create_subcomment', args=[comment.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(comment.child_comment.count(), 1)


class CartTest(APITestCase):
    def test_add_to_cart(self):
        """Добавление в корзину"""
        user = create_user(self.client)
        category = create_category()
        good = create_good(category)
        data = {
            'quantity': 2,
            'good': good.id
        }
        response = self.client.post(
            reverse('to-cart'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GoodsInCart.objects.count(), 1)
        self.assertEqual(Cart.objects.get(customer=user).amount_items, 20)
        self.assertEqual(Cart.objects.get(customer=user).promo_price, None)
        """Промо код"""
        promo = create_promo()
        data = {'promo_code': 'test'}
        response = self.client.post(
            reverse('promo'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.get(customer=user).promo_price, 15)

    def get_cart(self):
        """Получение элементов корзины"""
        user = create_user(self.client)
        response = self.client.get(
            reverse('to-cart'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def edit_cart(self):
        """Изменение количества товара в корзине"""
        user = create_user(self.client)
        category = create_category()
        good = create_good(category)
        good_cart = GoodsInCart.objects.create(good=good, cart__customer=user, quantity=1)
        data = {'quantity': 2}
        response = self.client.put(
            reverse('cart-edit', args=[good.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(good_cart.quantity, 2)

    def delete_carts_good(self):
        """Удаление товара из корзины"""
        user = create_user(self.client)
        category = create_category()
        good = create_good(category)
        GoodsInCart.objects.create(good=good, cart__customer=user, quantity=1)
        response = self.client.delete(
            reverse('cart-edit', args=[good.id]),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GoodsInCart.objects.count(), 0)


class OrderTest(APITestCase):
    def test_order(self):
        """Создание заказа и получение в истории"""
        user = create_user(self.client)
        category = create_category()
        good = create_good(category)
        promo = create_promo()
        cart = Cart.objects.get(customer=user, accepted=False)
        GoodsInCart.objects.create(good=good, cart=cart, quantity=1)
        cart.promo_code = promo
        cart.save()
        data = {
            #'comment': 'test_comment',
            'delivery_address': 'test_address',
            'receiver_name': 'test_name'
        }
        response = self.client.popyst(
            reverse('add_order'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        #self.assertEqual(Order.objects.first().comment, 'test_comment')
        self.assertEqual(Order.objects.first().amount, 5)
        """Проверка в истории заказов"""
        response = self.client.get(
            reverse('order_history'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        """Проверка состава заказа в истории"""
        order = Order.objects.first()
        response = self.client.get(
            reverse('order_list', args=[order.id]),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
