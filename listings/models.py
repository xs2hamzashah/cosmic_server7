from django.db import models

from core.models import TimeStampedModel


class SolutionType(models.TextChoices):
    ON_GRID = 'On-Grid', 'On-Grid'
    HYBRID = 'Hybrid', 'Hybrid'
    OFF_GRID = 'Off-Grid', 'Off-Grid'


class PaymentSchedule(models.TextChoices):
    ADVANCE = '100% Advance', '100% Advance'
    FLEXIBLE = 'Flexible', 'Flexible'


class SolarSolution(TimeStampedModel):
    size = models.DecimalField(max_digits=5, decimal_places=2, help_text="Solution size in kW (e.g., 5.00 kW)")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price of the solution/package")
    solution_type = models.CharField(max_length=50, choices=SolutionType.choices,
                                     help_text="Select the type of solar solution")
    tags = models.ManyToManyField('Tag', related_name='solar_solutions', blank=True)
    completion_time_days = models.PositiveIntegerField(default=15, help_text="Estimated completion time in days")
    payment_schedule = models.CharField(max_length=50, choices=PaymentSchedule.choices,
                                        default=PaymentSchedule.FLEXIBLE, help_text="Payment schedule for the solution")

    # New seller field added
    seller = models.ForeignKey('accounts.CustomUser', null=True,
                               on_delete=models.CASCADE,
                               related_name='solar_solutions')


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return 'solution_images/{filename}'.format(filename=filename)


class SolutionMedia(TimeStampedModel):
    solution = models.ForeignKey(SolarSolution, related_name='mediafiles', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, help_text="Upload an image of the solution")
    is_display_image = models.BooleanField(default=False,
                                           help_text="Indicates if this image is the display image for the solution")

    def __str__(self):
        return f"Image for {self.solution} (Display: {self.is_display_image})"


class DetailsType(models.TextChoices):
    PV_MODULE = 'PV Module', 'PV Module'
    INVERTER = 'Inverter', 'Inverter'
    BATTERY = 'Battery', 'Battery'
    ELECTRICAL_WORK = 'Electrical Work', 'Electrical Work'
    MECHANICAL_WORK = 'Mechanical Work', 'Mechanical Work'
    CIVIL_WORK = 'Civil Work', 'Civil Work'


class WireMaterial(models.TextChoices):
    COPPER = 'Copper', 'Copper'
    SILVER = 'Silver', 'Silver'
    OTHER = 'Other', 'Other'


class MechanicalMaterial(models.TextChoices):
    IRON = 'Iron', 'Iron'
    ALUMINIUM = 'Aluminium', 'Aluminium'
    GI = 'GI', 'GI'
    PVC = 'PVC', 'PVC'
    OTHER = 'Other', 'Other'


class MechanicalStructureType(models.TextChoices):
    L2 = 'L2', 'L2'
    L3 = 'L3', 'L3'
    SPECIAL = 'Special', 'Special'
    SAWTOOTH = 'Sawtooth', 'Sawtooth'
    OTHER = 'Other', 'Other'


class CivilMaterial(models.TextChoices):
    CONCRETE = 'Concrete', 'Concrete'
    CURBSTONE = 'Curbstone', 'Curbstone'
    BRICK = 'Brick', 'Brick'
    OTHER = 'Other', 'Other'


class SolutionDetails(TimeStampedModel):
    solar_solution = models.ForeignKey(SolarSolution, on_delete=models.CASCADE, related_name='components')
    details_type = models.CharField(max_length=50,
                                    choices=DetailsType.choices)  # Identifies the type of solar solution details
    brand = models.CharField(max_length=100, blank=True, null=True)  # Optional, not always applicable
    capacity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional
    quantity = models.PositiveIntegerField(default=1)  # Can be used for counts or multiples of work done
    warranty = models.DecimalField(max_digits=4, decimal_places=1, default=1)  # Default 1 year warranty
    details = models.TextField(blank=True, null=True)  # Additional details (specific to the work type)

    mechanical_material = models.CharField(max_length=50, choices=MechanicalMaterial.choices, blank=True,
                                           null=True)  # Mechanical work
    mechanical_structure_type = models.CharField(max_length=50, choices=MechanicalStructureType.choices, blank=True,
                                                 null=True)  # Structure type in mechanical work

    civil_material = models.CharField(max_length=50, choices=CivilMaterial.choices, blank=True,
                                      null=True)  # Civil work
    wire_material = models.CharField(max_length=50, choices=WireMaterial.choices, blank=True,
                                     null=True)  # Wire work

    def __str__(self):
        return f"{self.details_type} for {self.solar_solution}"


class Service(TimeStampedModel):
    solution = models.ForeignKey(SolarSolution, related_name='services', on_delete=models.CASCADE)
    dc_earthing_included = models.BooleanField(default=False, help_text="Is DC Earthing included?")
    afss_included = models.BooleanField(default=False, help_text="Is AFSS included?")
    afss_warranty_years = models.PositiveIntegerField(null=True, blank=True,
                                                      help_text="AFSS warranty in years if included")
    online_monitoring_included = models.BooleanField(default=False, help_text="Is online monitoring included?")
    net_metering_included = models.BooleanField(default=False, help_text="Is net metering included?")
    fire_extinguisher_included = models.BooleanField(default=False, help_text="Is HSE service included?")
    transportation_included = models.BooleanField(default=True, help_text="Is transportation included?")


class BuyerInteraction(TimeStampedModel):
    solar_solution = models.ForeignKey(SolarSolution, related_name='interactions', on_delete=models.CASCADE)
    whatsapp_number = models.CharField(max_length=15)
