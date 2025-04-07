from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from inspections import views as inspections_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inspections_views.home, name='home'),
    path('register/', accounts_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-restaurant/', accounts_views.add_restaurant, name='add_restaurant'),
    path('request-inspection/<int:restaurant_id>/', inspections_views.request_inspection, name='request_inspection'),
    path('approve-inspection/<int:request_id>/', inspections_views.approve_inspection, name='approve_inspection'),
    path('conduct-inspection/<int:request_id>/', inspections_views.conduct_inspection, name='conduct_inspection'),
    path('analytics/', inspections_views.inspection_analytics, name='analytics'),
    path('api/', include('api.urls')),
    path('admin-dashboard/', inspections_views.admin_dashboard, name='admin_dashboard'),
    path('public-dashboard/', inspections_views.public_dashboard, name='public_dashboard'),
]