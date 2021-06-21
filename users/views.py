from .forms import UserRegistrationForm ,UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username} has been created!')
            raw_password=form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if(request.GET.get('next')):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home-home')
    else:
        form=UserRegistrationForm()
    return render(request,'users/register.html',{'form':form,'next':request.GET.get('next')})


@login_required
def profileDisplay(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f' Your Account has been updated')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'users/profile.html',context)

