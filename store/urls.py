from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/<int:product_id>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update_cart/<int:product_id>', views.UpdateCartView.as_view(), name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', views.product, name='products_detail'),
    path('product/<int:id>/', views.product, name='product-detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)