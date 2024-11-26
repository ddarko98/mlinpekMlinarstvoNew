from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from store import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('update_item/', views.updateItem, name="update_item"),
    path('rosetta/', include('rosetta.urls'))
  
]


# Define i18n patterns
urlpatterns += i18n_patterns(
    path('', views.store, name="store"),
    path('kontakt/', views.kontakt, name="kontakt"),
    path('pecanje/', views.pecanje, name="pecanje"),
    path('pesme/', views.pesme, name="pesme"),
    path('zbirkaPesama/', views.zbirkaPesama, name='zbirkaPesama'),
    path('pricesaterena/', views.pricesaterena, name="pricesaterena"),
    path('prica1/', views.prica1, name="prica1"),

    path('trgovina/', views.trgovina, name="trgovina"),
    path('trgovinaDetaljnije/<str:pk>/', views.trgovinaDetaljnije, name="trgovinaDetaljnije"),

    path('kurs/', views.kurs, name="kurs"),
    path('kursTehnologije/', views.kursTehnologije, name='kursTehnologije'),

    path('cart/', views.cart, name="cart"),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name="deleteOrder"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkoutConfirm/', views.checkoutConfirm, name='checkoutConfirm'),

    path('registerPage/', views.registerPage, name="registerPage"),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
    path('searchProducts/', views.searchProducts, name='searchProducts'),
    path('set_language/', views.set_language, name='set_language'),
    # ... other i18n-specific URL patterns ...
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
