from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_restaurant_owner = models.BooleanField(default=False)
    is_inspector = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Restaurant(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        from inspections.models import Inspection  # Local import to avoid circular import
        inspections = Inspection.objects.filter(
            inspection_request__restaurant=self,
            is_completed=True
        )
        if inspections.exists():
            return round(sum(i.overall_rating for i in inspections) / inspections.count(), 1)
        return None

    def latest_inspection_date(self):
        from inspections.models import Inspection  # Local import to avoid circular import
        latest = Inspection.objects.filter(
            inspection_request__restaurant=self,
            is_completed=True
        ).order_by('-inspection_date').first()
        return latest.inspection_date if latest else None