from rest_framework import generics, permissions
from accounts.models import Restaurant
from inspections.models import InspectionRequest, Inspection
from .serializers import RestaurantSerializer, InspectionRequestSerializer, InspectionSerializer


class RestaurantList(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_restaurant_owner:
            return Restaurant.objects.filter(owner=self.request.user)
        return Restaurant.objects.none()


class InspectionRequestList(generics.ListCreateAPIView):
    serializer_class = InspectionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_restaurant_owner:
            return InspectionRequest.objects.filter(restaurant__owner=self.request.user)
        return InspectionRequest.objects.none()

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=self.request.user)
        serializer.save(restaurant=restaurant)


class InspectionList(generics.ListAPIView):
    serializer_class = InspectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_restaurant_owner:
            return Inspection.objects.filter(inspection_request__restaurant__owner=self.request.user)
        elif self.request.user.is_inspector:
            return Inspection.objects.filter(inspector=self.request.user)
        return Inspection.objects.none()


class InspectionDetail(generics.RetrieveUpdateAPIView):
    serializer_class = InspectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_restaurant_owner:
            return Inspection.objects.filter(inspection_request__restaurant__owner=self.request.user)
        elif self.request.user.is_inspector:
            return Inspection.objects.filter(inspector=self.request.user)
        return Inspection.objects.none()