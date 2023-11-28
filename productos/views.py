# productos/views.py
from django.shortcuts import render, get_object_or_404
from .models import Producto

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            # El código QR ya debería haberse generado automáticamente en el método save del modelo
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear_producto.html', {'form': form})
# productos/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
from .models import Producto
@login_required
class ListaProductosView(View):
    template_name = 'productos/lista_productos.html'
    paginate_by = 20  # Número de productos por página

    def get(self, request, *args, **kwargs):
        productos_list = Producto.objects.all().order_by('id')

        paginator = Paginator(productos_list, self.paginate_by)
        page = request.GET.get('page')

        try:
            productos = paginator.page(page)
        except PageNotAnInteger:
            productos = paginator.page(1)
        except EmptyPage:
            productos = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'productos': productos})
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import Producto
@login_required
def cargar_productos_desde_xlsx(request):
    if request.method == 'POST' and request.FILES['archivo_xlsx']:
        archivo_xlsx = request.FILES['archivo_xlsx']

        try:
            # Leer el archivo xlsx
            df = pd.read_excel(archivo_xlsx)

            # Iterar sobre las filas del DataFrame y crear productos
            for index, row in df.iterrows():
                producto = Producto(
                    nombre=row['Codigo'],
                    descripcion=row['Descripcion'],
                    precio=row['Precios']
                    # Puedes agregar más campos según tu modelo
                )
                producto.save()

            messages.success(request, 'Productos cargados exitosamente.')
            return redirect('lista_productos')

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')

    return render(request, 'productos/cargar_productos_desde_xlsx.html')
