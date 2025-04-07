from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class InspectionRequest(models.Model):
    restaurant = models.ForeignKey('accounts.Restaurant', on_delete=models.CASCADE, related_name='inspection_requests')
    requested_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inspection for {self.restaurant.name} on {self.requested_date}"


class Inspection(models.Model):
    inspection_request = models.OneToOneField(InspectionRequest, on_delete=models.CASCADE, related_name='inspection')
    inspector = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inspections')
    inspection_date = models.DateField()
    general_hygiene = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage score for general hygiene (0-100)"
    )
    customer_service = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage score for customer service (0-100)"
    )
    food_preparation = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage score for food preparation (0-100)"
    )
    cooking_outcome = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage score for cooking outcome (0-100)"
    )
    comments = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def overall_rating(self):
        if None in [self.general_hygiene, self.customer_service,
                    self.food_preparation, self.cooking_outcome]:
            return None
        average = (self.general_hygiene + self.customer_service +
                   self.food_preparation + self.cooking_outcome) / 4
        return round(average / 20, 1)  # Convert to 5-star scale

    def save(self, *args, **kwargs):
        # Auto-complete when all fields are filled
        if all([
            self.general_hygiene is not None,
            self.customer_service is not None,
            self.food_preparation is not None,
            self.cooking_outcome is not None
        ]):
            self.is_completed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inspection of {self.inspection_request.restaurant.name} on {self.inspection_date}"