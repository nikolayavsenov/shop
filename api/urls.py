from . import views
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from allauth.account.views import confirm_email, ConfirmEmailView, PasswordResetView
from rest_auth.registration.views import VerifyEmailView

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description='Some desc',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    #re_path('rest-auth/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='confirm_email'),
    path('favorite/', views.FavoriteList.as_view(), name='favorite_create'),
    path('favorite/<int:good>', views.FavoriteDelete.as_view(), name='favorite_delete'),
    path('cat-create/', views.CategoryCreate.as_view(), name='category_create'),
    path('cat-ops/<int:id>', views.CategoryOperations.as_view(), name='category_ops'),
    path('category/', views.CatList.as_view(), name='category_list'),
    #path('cat/', views.CategoryList.as_view()),
    path('order/', views.OrderList.as_view(), name='add_order'),
    path('order-history/<int:id>', views.OrderListInHistory.as_view(), name='order_list'),
    path('order-history/', views.OrderHistory.as_view(), name='order_history'),
    path('posts/', views.PostList.as_view(), name='posts_get'),
    path('post-create/', views.PostCreate.as_view(), name='post_create'),
    path('post-ops/<int:id>', views.PostOperations.as_view(), name='post_edit'),
    path('goods/', views.GoodsList.as_view(), name='good_create'),
    path('goods/category=0', views.GoodsList.as_view()),
    path('goods/category=<int:category>', views.GoodsByCategory.as_view(), name='goods_by_cat'),
    path('goods-ops/<int:pk>', views.GoodsOperations.as_view(), name='good_edit'),
    path('goods-random/', views.RandomGoods.as_view()),
    path('comments/', views.CommentList.as_view(), name='create_comment'),
    path('comments/post_id=<int:post>', views.CommentsById.as_view()),
    path('comments/<int:id>', views.CreateSubComment.as_view(), name='create_subcomment'),
    path('comment-ops/<int:pk>', views.CommentOps.as_view(), name='comment_ops'),
    path('promo/', views.GetPromo.as_view(), name='promo'),
    path('carts/', views.CartList.as_view()),
    path('carts-ops/<id>', views.CartOps.as_view()),
    path('to-cart/', views.AddGoodToCart.as_view(), name='to-cart'),
    path('cart-edit/<int:good>', views.GoodsInCartEdit.as_view()),
    path('rest-auth/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('rest-auth/login/', views.CustomLoginView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('swagger(P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
