from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, Producto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
from .carrito import Carrito
import mercadopago



def home(request):
    productos = Producto.objects.all()
   
    return render(request, 'gallery.html',{'productos': productos})

def signup(request):
    if request.method == 'GET':
        
        return render(request, 'signup.html',{'form': UserCreationForm})
        
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('gallery')
            except IntegrityError:
                return render(request, 'signup.html',{'form': UserCreationForm, "error":'Usuario ya existe'})
            
            
        return render(request, 'signup.html',{'form': UserCreationForm, "error":'La contraseña de verificación no coincide.'})


@login_required 
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render (request, 'tasks.html', {'tasks': tasks})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        if 'submit_get' in request.POST:
            return render(request, 'signin.html', {"form": AuthenticationForm})
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render (request, 'signin.html',{'form': AuthenticationForm, "error":'Usuario o pass incorrecto'})
            else:
                

                login(request, user)
                return redirect('gallery')

@login_required
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 'error':'Por favor ingresos los datos validos'})
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  
        form = TaskForm(instance =task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)       
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form':form, 'error':'Error de actualizacion'})

@login_required        
def complete_task (request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete (request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def taskcomplete (request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 

    return render(request, 'tasks.html', {'tasks': tasks})


def tienda(request):
    productos = Producto.objects.all()
    return render(request, "tienda.html", {'productos': productos})

def agregar_producto(request, producto_id):
    if not request.session["carrito"]:
        carrito = Carrito(request)
        producto = Producto.objects.get(id=producto_id)
        carrito.agregar(producto)
       
        return redirect("cart")
    else:
        carrito = Carrito(request)
        producto = Producto.objects.get(id=producto_id)
        carrito.agregar(producto)
       
        return redirect("PD", producto_id=producto_id)


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    
    carrito.eliminar(producto)
   
    return redirect("cart")
    
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda")

def limpiar_carrito_item(request,producto_id):
    
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.limpiaritem(producto)
    return redirect("cart")

def galeriaprueba(request):
    productos = Producto.objects.all()
   
    return render(request, "gallery.html", {'productos': productos})

def detalleproducto(request,producto_id):
    producto = Producto.objects.get(id=producto_id)
   
    return render(request, "productdetails.html", {'productos': producto})
    
    




def cart(request):
    precioanterior = 0
    cantidad = 0
    desc = 0
    subtotal = 0
    total_aum = 0
    preference_data = { "items": [] }
    for key, value in request.session["carrito"].items():
       
        precioanterior = int(value["precioanterior"])
        cantidad = int(value["cantidad"])
        desc += int(precioanterior * cantidad)
        total_aum += int(precioanterior * cantidad)
        subtotal += int(value["precio"]*value["cantidad"])
        
    
        item = {
                    "title": value["nombre"],
                    "quantity": cantidad,
                    "unit_price": int(value["precio"]),
                }
     
 
        preference_data["items"].append(item)
    desc= int(total_aum - subtotal)   
    
    sdk = mercadopago.SDK("APP_USR-5213772683732349-061323-dc5bd7f2a56c2080735653bb6d1901e7-97277305")
    preference_data["back_urls"] = {
    "success": "https://www.tu-sitio/success",
    "failure": "https://www.tu-sitio/failure",
    "pending": "https://www.tu-sitio/pendings"
}
    preference_data["auto_return"] = "approved"
    
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return render(request, "checkout.html", {'preference_id': preference['id'], 'precioanterior': precioanterior, 'desc': desc, 'subtotal': subtotal,'desc': desc, 'total_aum': total_aum} )


    
