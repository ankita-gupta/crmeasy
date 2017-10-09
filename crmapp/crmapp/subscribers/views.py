from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Subscriber
from .forms import SubscriberForm

def subsciber_new(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            address_one = form.cleaned_data['address_one']
            address_two = form.cleaned_data['address_two']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            sub = Subscriber(address_one=address_one, address_two=address_two, city=city, state=state, user_rec=user)
            sub.save()
            return HttpResponseRedirect('/success/')
    else:
        form = SubscriberForm()
    return render(request, 'subscribers/subscriber_new.html', {'form':form})

