from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, RestaurantForm
from .models import Restaurant


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set user type based on registration
            if form.cleaned_data.get('is_restaurant_owner'):
                user.is_restaurant_owner = True
            elif form.cleaned_data.get('is_inspector'):
                user.is_inspector = True
            user.save()

            login(request, user)
            messages.success(request, 'Registration successful!')

            if user.is_restaurant_owner:
                return redirect('add_restaurant')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def add_restaurant(request):
    if not request.user.is_authenticated or not request.user.is_restaurant_owner:
        return redirect('home')

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, 'Restaurant added successfully!')
            return redirect('home')
    else:
        form = RestaurantForm()
    return render(request, 'accounts/add_restaurant.html', {'form': form})