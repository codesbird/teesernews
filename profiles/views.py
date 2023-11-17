from typing import Any, Dict, Optional, Type
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from news.models import *
# Create your views here.
########################### moduls form django library for project  #####################################################
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import json,uuid
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.views.generic import UpdateView

def Dashboard(request):
    return render(request,'dashboard.html')


class EditProfile(UpdateView):
    
    model = User

    fields = ["username","first_name","last_name","email","gender","dob","phone","city","state","country","bio","private","profile"]
    
    success_url = '/profile/'

    template_name = 'edit_profile.html'

   
        
def ChangePassword(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/dashboard/')

    else:
        form = PasswordChangeForm(request.user)

    return render(request,'changepassword.html',{'forms':form})
