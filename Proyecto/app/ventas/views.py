from django.shortcuts import render, redirect
from .models import Cliente, Producto
from .forms import AddClienteForm,EditarClienteForm, AddProductoForm,EditarProductoForm
from django.contrib import messages
from .models import Cliente, Egreso, Producto, Egreso, ProductosEgreso
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
import json
# Create your views here.
def ventas_view(request):
    ventas=Egreso.objects.all()
    num_ventas=len(ventas)
    context={
        'ventas':ventas,
        'num_ventas':num_ventas
    }

    num_ventas = 156
    context = {
        'num_ventas': num_ventas
    }
    return render (request, 'ventas.html', context)

def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar =EditarClienteForm()
    context = {
    'clientes': clientes,
    'form_personal': form_personal,
    'form_editar':form_editar
    }
    return render (request, 'clientes.html', context)

def add_cliente_view(request):
    # print ("Guardar cliente")
    if request.POST:
        form= AddClienteForm(request.POST, request.FILES)
        try:
            form.save()
        except:
            messages(request, "Error al guardar el cliente")
            return redirect('Clientes')
    return redirect('Clientes')

def edit_cliente_view(request):
    if request.POST:
        cliente=Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form=EditarClienteForm(
            request.POST, request.FILES, instance=cliente
        )
        if form.is_valid:
            form.save()
    return redirect('Clientes')

def delete_cliente_view(request):
    if request.POST:
        cliente=Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
    return redirect('Clientes')

def delete_venta_view(request):
    if request.POST:
        cliente=Egreso.objects.get(pk=request.POST.get('id_producto_eliminar'))
        cliente.delete()
    return redirect('Ventas')



#Productos

def productos_view(request):
    """
    clientes = Cliente.objects.all()
    
    form_editar =EditarClienteForm()
    """
    productos=Producto.objects.all()
    form_add = AddProductoForm()
    form_editar=EditarProductoForm()
    context = {
        'productos': productos,
        'form_add': form_add,
        'form_editar':form_editar
      
    }

    return render (request, 'productos.html', context)

def add_productos_view(request):
    # print ("Guardar productos")
    if request.POST:
        form= AddProductoForm(request.POST, request.FILES)
        try:
            form.save()
        except:
            messages(request, "Error al guardar el producto")
            return redirect('Productos')
    return redirect('Productos')


class add_ventas(ListView):
    template_name = 'add_ventas.html'
    model = Egreso

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {'success': False}  # Default response
        try:
            action = request.POST.get('action', '')
            print(f"Action: {action}")

            if action == 'autocomplete':
                data = []
                term = request.POST.get("term", "")
                for i in Producto.objects.filter(descripcion__icontains=term)[:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
                print(f"Autocomplete data: {data}")

            elif action == 'save':
                total_pagado = sum(float(request.POST.get(method, 0)) for method in ["efectivo", "tarjeta", "transferencia", "vales", "otro"])
                fecha = request.POST.get("fecha", "")
                id_cliente = int(request.POST.get("id_cliente", 0))
                cliente_obj = Cliente.objects.get(pk=id_cliente)
                datos = json.loads(request.POST.get("verts", "{}"))
                total_venta = float(datos.get("total", 0))
                ticket_num = int(request.POST.get("ticket", 0))
                ticket = ticket_num == 1
                desglosar_iva_num = int(request.POST.get("desglosar", 0))
                desglosar_iva = desglosar_iva_num == 1
                comentarios = request.POST.get("comentarios", "")

                nueva_venta = Egreso(
                    fecha_pedido=fecha,
                    cliente=cliente_obj,
                    total=total_venta,
                    pagado=total_pagado,
                    comentarios=comentarios,
                    ticket=ticket,
                    desglosar=desglosar_iva
                )
                nueva_venta.save()
                data['success'] = True
                data['venta_id'] = nueva_venta.id
                print(f"Nueva venta guardada: {nueva_venta}")

            else:
                data['error'] = "Acción no reconocida"

        except Exception as e:
            data['error'] = str(e)
            print(f"Error: {e}")

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos_lista"] = Producto.objects.all()
        context["clientes_lista"] = Cliente.objects.all()
        return context


def export_pdf_view(request):
    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    
    return html_template


def edit_productos_view(request):
    if request.POST:
        producto=Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form=EditarProductoForm(
            request.POST, request.FILES, instance=producto
        )
        if form.is_valid:
            form.save()
    return redirect('Productos')


def delete_producto_view(request):
    if request.POST:
        producto=Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        producto.delete()
    return redirect('Productos')


