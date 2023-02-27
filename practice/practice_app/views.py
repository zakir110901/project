from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from .models import db, pdf

# Create your views here.
@login_required
def home(request):
    return render(request, 'index.html')

def signupuser(request):
    if request.method=='GET':
        return render(request, 'register.html',{'form':UserCreationForm()})
    else:
        uname = request.POST['username']
        upwd1 = request.POST['password1']
        upwd2 = request.POST['password2']
        if upwd1==upwd2:
            try:
                user = User.objects.create_user(username=uname,password=upwd2)
                user.save()
            except IntegrityError:
                return render(request, 'register.html',{'form':UserCreationForm(),'message':'Username already exists. Choose another one.'})
            else:
                return redirect('loginuser')
        else:
            return render(request, 'register.html',{'form':UserCreationForm(),'message':'Password Mismatch Error'})

def loginuser(request):    
    if request.method=='GET':
        return render(request, 'login.html',{'form':AuthenticationForm()})
    else:
        name = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=name, password=pwd)
        if user is not None:        
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html',{'form':AuthenticationForm(),'message':'User Not Found. Try Again'})

def logoutuser(request):
    logout(request)
    return redirect('loginuser')

@login_required
def pdf(request):
    user=request.user.email
    print(user)
    mydata = db.objects.filter(email=user).values()
    x = mydata[0]['name']
    print(x)  
    template_path = 'certificate.html'
    context = {
        'data': mydata,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename='+ x +'.pdf'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def check(request, user):
    user=user
    print(user)
    mydata = db.objects.filter(email=user).values()
    print(mydata)
    template_path = 'certificate.html'
    context = {
        'data': mydata,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def download_all(request):
    if request.method == 'POST':
        na = request.POST['name']
        mydata = db.objects.filter(name=na).values()
        x = mydata[0]['name']  
        template_path = 'certificate.html'
        context = {
            'data': mydata,
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+ x +'.pdf'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        name = db.objects.all()
        context = {
            'name': name,
        }
        return render(request, 'download.html', context)
    
def download_all1(request):
    
    
    return HttpResponse('dsj')