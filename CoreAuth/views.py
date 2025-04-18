from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .form import RegistrationForm

# Create your views here.

def registration_view(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('store')
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request,'accounts/registration.html',context)


def login_view(request):
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            error_message = "invalid credentials"
    return render(request, 'accounts/login.html', {'error': error_message})
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('store')