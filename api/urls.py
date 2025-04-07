from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantList.as_view(), name='restaurant-list'),
    path('inspection-requests/', views.InspectionRequestList.as_view(), name='inspection-request-list'),
    path('inspections/', views.InspectionList.as_view(), name='inspection-list'),
    path('inspections/<int:pk>/', views.InspectionDetail.as_view(), name='inspection-detail'),
]