from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('usuarios.urls')),
    path('api/productos/', include('productos.urls')),
    path('api/carrito/', include('carrito.urls')),
    path('api/ordenes/', include('ordenes.urls')),
    path('api/cupones/', include('cupones.urls')),

    # Frontend
    path('', TemplateView.as_view(template_name='index.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('registro/', TemplateView.as_view(template_name='registro.html')),
    path('carrito/', TemplateView.as_view(template_name='carrito.html')),
    path('admin-panel/', TemplateView.as_view(template_name='admin.html')),
    path('pago/', TemplateView.as_view(template_name='pago.html')),
    path('ordenes/', TemplateView.as_view(template_name='ordenes.html')),
]