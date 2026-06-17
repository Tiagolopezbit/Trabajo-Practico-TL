from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('registro/', TemplateView.as_view(template_name='registro.html')),
    path('carrito/', TemplateView.as_view(template_name='carrito.html')),
    path('admin-panel/', TemplateView.as_view(template_name='admin.html')),
    path('pago/', TemplateView.as_view(template_name='pago.html')),
]