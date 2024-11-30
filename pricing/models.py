from django.db import models

from core.models import TimeStampedModel


class SubscriptionPlan(TimeStampedModel):
    class Package(models.TextChoices):
        BASIC = 'basic', 'Basic Package'

    name = models.CharField(max_length=100, choices=Package.choices, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_name_display()} (${self.price})"


class SubscriptionPass(TimeStampedModel):
    seller = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seller', 'plan')
        verbose_name = 'Subscription Pass'

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"