
from django.http.request import HttpRequest as HttpRequest
from django.views.generic.list import ListView #TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
#from .forms import LoginForm
from django.contrib.auth.models import User,Group
from .forms import UserForm, FormDatosPersonales
from django.contrib.messages.views import SuccessMessageMixin
from .models import DatosPersonales
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader  import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .token import token_activacion
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect

from django.views.generic import TemplateView

    #template_name=''

class LoginView(LoginView):
    template_name= 'login.html'
    form_class= AuthenticationForm
    #form_class= LoginForm

#class BienvenidaView(LoginRequiredMixin,TemplateView):
   # name='bienvenida.html'

class RegistrarView(SuccessMessageMixin, CreateView):
    model=User
    form_class=UserForm
    success_url=reverse_lazy('login')
    success_message="%(username)s se registró de manera exitosa"


    def form_valid(self,form):
        user =form.save(commit=False)
        user.is_active=False
        user.save()

        sitio= get_current_site(self.request)

        uid=urlsafe_base64_encode(force_bytes(user.id))
        token= token_activacion.make_token(user)

        mensaje= render_to_string(
            'confirmar_cuenta.html',
            {
            'user':user,
            'sitio':sitio,
            'uid':uid,
            'token':token
            }
            
        )
        asunto='Activar cuenta'
        para= user.email
        email=EmailMessage(
            asunto,
            mensaje,
            to=[para]
        )
        email.content_subtype= 'html'
        email.send()
        return super().form_valid(form)
    
class ActivarCuentaView(TemplateView):
    def get(self, request, *args, **kwargs) :
        try:
            uid= urlsafe_base64_decode(kwargs['uidb64'])
            token =kwargs['token']
            user = User.objects.get(pk=uid)
        except(TypeError,ValueError,User.DoesNotExist):
            user=None
        if user is not None and token_activacion.check_token(user, token):
            user.is_active=True
            user.save()

            messages.success(request,'Cuenta activada, ingresa datos')
        else:
            messages.error(request,'Token inválido, contacta al administrador')
            

        return redirect('login')

class CrearPerfilView(SuccessMessageMixin, CreateView):
    model = DatosPersonales
    form_class = FormDatosPersonales
    template_name = 'datos/datospersonales_form.html'
    success_url = reverse_lazy('bienvenida')
    success_message = "Se guardaron tus datos personales"


    def form_valid(self, form):
        datos_personales = form.save(commit=False)
        datos_personales.user=self.request.user
        datos_personales.save()
        
        return super().form_valid(form)
    

class ListaUsuariosView(ListView):
    model=User
    template_name='lista_usuarios.html'

    def get_context_data(self, **kwargs):
        context=super(ListaUsuariosView,self).get_context_data(**kwargs)
        context['grupos']=Group.objects.all()
        return context
    
def asignar_grupos(request):
    id_usuario=request.POST.get('usuario', None)
    usuario=User.objects.get(id=id_usuario)
    usuario.groups.clear()
    for item in request.POST:
        if request.POST[item]=='on':
            grupo=Group.objects.get(id=int(item))
            usuario.groups.add(grupo)
    
    messages.success(request, 'Se agregaron los grupos al usuario')
    return redirect('lista_usuarios')