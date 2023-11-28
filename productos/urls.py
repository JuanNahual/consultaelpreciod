# productos/urls.py
from django.urls import path
from .views import detalle_producto, crear_producto, ListaProductosView,cargar_productos_desde_xlsx
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('detalle/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('crear/', crear_producto, name='crear_producto'),
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('cargar_productos/', cargar_productos_desde_xlsx, name='cargar_productos_desde_xlsx'),
] 
