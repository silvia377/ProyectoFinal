from django.urls import path, include
from. import views
urlpatterns = [
    path('', views.ventas_view, name= 'Ventas'),
    path('clientes/', views.clientes_view, name= 'Clientes'),
    path('add_cliente/', views.add_cliente_view, name= 'AddCliente'), #Añadir cliente
    path('edit_cliente/', views .edit_cliente_view, name= 'EditCliente'), #Editar cliente
    path('delete_cliente/', views.delete_cliente_view, name= 'DeleteCliente'), #Eliminar cliente


    path('productos/', views.productos_view, name= 'Productos'),
    path('add_producto/', views.add_productos_view, name= 'AddProducto'), #Añadir productos
    path('edit_producto/', views.edit_productos_view, name= 'EditProducto'), #Editar producto
    path('delete_producto/', views.delete_producto_view, name= 'DeleteProducto'), #Eliminar producto

    
    path('add_venta/',views.add_ventas.as_view(), name='AddVenta'),
    path('export/', views.export_pdf_view, name="ExportPDF" ),
    path('delete_venta/', views.delete_venta_view, name= 'DeleteVenta'), #Eliminar venta
    





]

