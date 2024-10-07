from django.db import models

from core.models import TimeStampedModel
from listings.models import SolarSolution


class Approval(TimeStampedModel):
    solution = models.ForeignKey(SolarSolution, related_name='approvals', on_delete=models.CASCADE)
    admin_verified = models.BooleanField(default=False, help_text="Has the admin verified the listing?")
    discrepancy = models.TextField(null=True, blank=True, help_text="Details of any discrepancy found during review")
    discrepancy_resolved = models.BooleanField(default=False, help_text="Has the discrepancy been resolved?")
    email_notification_sent = models.BooleanField(default=False,
                                                  help_text="Has the approval notification been sent to the seller?")
