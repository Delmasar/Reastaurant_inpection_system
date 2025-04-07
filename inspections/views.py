from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InspectionRequest, Inspection
from .forms import InspectionRequestForm, InspectionForm
from accounts.models import CustomUser, Restaurant
from django.db.models import Max, Avg, Case, When, FloatField
from django.db.models import Count, Q


@login_required
def home(request):
    if request.user.is_customer:
        return redirect('public_dashboard')

    context = {}

    if request.user.is_restaurant_owner:
        restaurants = Restaurant.objects.filter(owner=request.user)
        inspection_requests = InspectionRequest.objects.filter(restaurant__in=restaurants)
        inspections = Inspection.objects.filter(
            inspection_request__in=inspection_requests,
            is_completed=True
        )
        context.update({
            'restaurants': restaurants,
            'inspection_requests': inspection_requests,
            'inspections': inspections,
        })
    elif request.user.is_inspector:
        pending_requests = InspectionRequest.objects.filter(is_approved=False)
        upcoming_inspections = InspectionRequest.objects.filter(
            is_approved=True,
            inspection__isnull=True
        )
        completed_inspections = Inspection.objects.filter(
            inspector=request.user,
            is_completed=True
        )
        context.update({
            'pending_requests': pending_requests,
            'upcoming_inspections': upcoming_inspections,
            'completed_inspections': completed_inspections,
        })
    elif request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'inspections/home.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Statistics
    total_inspectors = CustomUser.objects.filter(is_inspector=True).count()
    total_restaurants = Restaurant.objects.count()
    pending_requests = InspectionRequest.objects.filter(is_approved=False).count()
    approved_requests = InspectionRequest.objects.filter(is_approved=True, inspection__isnull=True).count()
    completed_inspections = Inspection.objects.filter(is_completed=True).count()

    # Get detailed inspection data
    inspections = Inspection.objects.filter(
        is_completed=True
    ).select_related(
        'inspection_request__restaurant',
        'inspector'
    ).order_by('-inspection_date')

    context = {
        'total_inspectors': total_inspectors,
        'total_restaurants': total_restaurants,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'completed_inspections': completed_inspections,
        'inspections': inspections,
    }
    return render(request, 'inspections/admin_dashboard.html', context)

@login_required
def request_inspection(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)

    if request.method == 'POST':
        form = InspectionRequestForm(request.POST)
        if form.is_valid():
            inspection_request = form.save(commit=False)
            inspection_request.restaurant = restaurant
            inspection_request.save()
            messages.success(request, 'Inspection request submitted successfully!')
            return redirect('home')
    else:
        form = InspectionRequestForm()

    return render(request, 'inspections/request_inspection.html', {
        'form': form,
        'restaurant': restaurant,
    })


@login_required
def approve_inspection(request, request_id):
    if not request.user.is_inspector:
        return redirect('home')

    inspection_request = get_object_or_404(InspectionRequest, pk=request_id)
    inspection_request.is_approved = True
    inspection_request.save()
    messages.success(request, 'Inspection request approved!')
    return redirect('home')

@login_required
def conduct_inspection(request, request_id):
    if not request.user.is_inspector:
        return redirect('home')

    inspection_request = get_object_or_404(InspectionRequest, pk=request_id, is_approved=True)

    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.inspection_request = inspection_request
            inspection.inspector = request.user
            inspection.save()
            messages.success(request, 'Inspection completed successfully!')
            return redirect('home')
    else:
        form = InspectionForm(initial={'inspection_date': inspection_request.requested_date})

    return render(request, 'inspections/conduct_inspection.html', {
        'form': form,
        'inspection_request': inspection_request,
    })


@login_required
def inspection_analytics(request):
    if not request.user.is_restaurant_owner:
        return redirect('home')

    restaurants = Restaurant.objects.filter(owner=request.user)
    inspections = Inspection.objects.filter(inspection_request__restaurant__in=restaurants)

    return render(request, 'inspections/analytics.html', {
        'inspections': inspections,
    })


def public_dashboard(request):
    # Get all restaurants with completed inspections
    restaurants = Restaurant.objects.filter(
        inspection_requests__inspection__is_completed=True
    ).annotate(
        latest_date=Max('inspection_requests__inspection__inspection_date')
    ).distinct().order_by('-latest_date')

    restaurant_data = []
    for restaurant in restaurants:
        avg_rating = restaurant.average_rating()
        if avg_rating is not None:  # Only include restaurants with ratings
            restaurant_data.append({
                'restaurant': restaurant,
                'avg_rating': avg_rating,
                'latest_date': restaurant.latest_inspection_date(),
                'inspections': restaurant.inspection_requests.filter(
                    inspection__is_completed=True
                ).select_related('inspection')
            })

    return render(request, 'inspections/public_dashboard.html', {
        'restaurant_data': restaurant_data
    })