from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import TemplateView
from netmiko import Netmiko
from netmiko import redispatch, exceptions
import time


# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password ==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exists!")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "User Name Already Exists!")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Password Mismatch!")
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
         
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "User does not exist!")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def counter(request):
    text = request.POST['text']
    amount_of_words=len(text.split())
    amount_of_chars=len(text)
    return render(request, 'counter.html', {'amount':amount_of_words,'chars':amount_of_chars})

def output(request):
    if request.method=='POST':
        ipadd=request.POST['ipadd']
        cmds=request.POST['cmds']
    linux_jump_host_ip = '10.255.127.67'
    linux_jump_host_user = 'srj026'
    linux_jump_host_password = 'J@1mahalaxmi'
    router_ip = ipadd
    router_user = 'maek_sjagnade'
    router_password = '_SzO<IH6'
    net_connect = Netmiko(device_type='cisco_ios',
						  host = linux_jump_host_ip,
						  username = linux_jump_host_user,
						  password = linux_jump_host_password)
    net_connect.write_channel(f'ssh -l {router_user} -p 3002 {router_ip}\n')
    time.sleep(2)
    output = net_connect.read_channel()
    if 'Password' in output:
     net_connect.write_channel(router_password+'\n')
     time.sleep(2)
    redispatch(net_connect,device_type='cisco_ios')
    for cmd in cmds:
	    router_output = net_connect.send_command(cmd)
    return render(request, 'output.html',{'ipad':ipadd, 'cmdss':cmds,'router_output':router_output})

  
def nconnect(request):
    return render(request, 'nconnect.html')
#class NConnect(TemplateView):
#    template_name="nconnect.html"

