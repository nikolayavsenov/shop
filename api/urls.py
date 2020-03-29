from . import views
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from allauth.account.views import confirm_email, ConfirmEmailView, PasswordResetView

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
    re_path('rest-auth/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='confirm_email'),
    path('cat-create/', views.CategoryCreate.as_view()),
    path('cat-ops/<id>', views.CategoryOperations.as_view()),
    path('category/', views.CatList.as_view()),
    #path('cat/', views.CategoryList.as_view()),
    path('post/', views.PostList.as_view()),
    path('post-create/', views.PostCreate.as_view()),
    path('post-ops/<id>', views.PostOperations.as_view()),
    path('goods/', views.GoodsList.as_view()),
    path('goods-ops/<id>',views.GoodsOperations.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('carts/', views.CartList.as_view()),
    path('carts-ops/<id>', views.CartOps.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]