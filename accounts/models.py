from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_restaurant_owner = models.BooleanField(default=False)
    is_inspector = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Restaurant(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        inspections = Inspection.objects.filter(inspection_request__restaurant=self)
        if inspections.exists():
            total = sum(inspection.overall_rating for inspection in inspections)
            return total / inspections.count()
        return None

    def get_last_inspection(self):
        return Inspection.objects.filter(inspection_request__restaurant=self).order_by('-inspection_date').first()