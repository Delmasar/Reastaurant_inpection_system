from rest_framework import serializers
from accounts.models import Restaurant
from inspections.models import InspectionRequest, Inspection


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'registration_date']


class InspectionRequestSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = InspectionRequest
        fields = ['id', 'restaurant', 'requested_date', 'is_approved', 'created_at']


class InspectionSerializer(serializers.ModelSerializer):
    inspection_request = InspectionRequestSerializer(read_only=True)
    overall_rating = serializers.SerializerMethodField()

    class Meta:
        model = Inspection
        fields = ['id', 'inspection_request', 'inspection_date', 'general_hygiene',
                  'customer_service', 'food_preparation', 'cooking_outcome',
                  'comments', 'overall_rating']

    def get_overall_rating(self, obj):
        return obj.overall_rating