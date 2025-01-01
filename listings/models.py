from django.core.validators import MaxLengthValidator
from django.db import models

from core.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return 'solution_images/{filename}'.format(filename=filename)


class ComponentType(models.TextChoices):
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


class SolutionComponent(TimeStampedModel):
    component_type = models.CharField(max_length=50, choices=ComponentType.choices)
    subtype = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    warranty = models.DecimalField(max_digits=4, decimal_places=1, default=1)
    details = models.TextField(blank=True, null=True)
    ip_rating = models.CharField(max_length=10, blank=True, null=True, help_text="Enter the IP rating (e.g., IP65, IP67)")
    total_backup_capacity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    mechanical_material = models.CharField(max_length=50, choices=MechanicalMaterial.choices, blank=True, null=True)
    mechanical_structure_type = models.CharField(max_length=50, choices=MechanicalStructureType.choices, blank=True, null=True)

    civil_material = models.CharField(max_length=50, choices=CivilMaterial.choices, blank=True, null=True)
    wire_material = models.CharField(max_length=50, choices=WireMaterial.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.component_type} - {self.subtype}"


class SolutionType(models.TextChoices):
    ON_GRID = 'On-Grid', 'On-Grid'
    HYBRID = 'Hybrid', 'Hybrid'
    OFF_GRID = 'Off-Grid', 'Off-Grid'


class PaymentSchedule(models.TextChoices):
    ADVANCE = '100% Advance', '100% Advance'
    FLEXIBLE = 'Flexible', 'Flexible'


class SolarSolution(TimeStampedModel):
    size = models.PositiveIntegerField(help_text="Solution size in kW (e.g., 5.00 kW)")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price of the solution/package")
    solution_type = models.CharField(max_length=50, choices=SolutionType.choices,
                                     help_text="Select the type of solar solution")
    tags = models.ManyToManyField('Tag', related_name='solar_solutions', blank=True)
    completion_time_days = models.PositiveIntegerField(default=15, help_text="Estimated completion time in days")
    payment_schedule = models.CharField(max_length=50, choices=PaymentSchedule.choices,
                                        default=PaymentSchedule.FLEXIBLE, help_text="Payment schedule for the solution")

    # New seller field added
    seller = models.ForeignKey('accounts.UserProfile', null=True,
                               on_delete=models.CASCADE,
                               related_name='solar_solutions')

    components = models.ManyToManyField(SolutionComponent, blank=True, related_name='solar_solutions')
    seller_note = models.TextField(validators=[MaxLengthValidator(1000)], null=True, blank=True)  # Set max length to 500 characters

    @property
    def display_name(self):
        if self.seller and hasattr(self.seller, 'company') and self.seller.company:
            company_name = self.seller.company.name
        else:
            company_name = ""
        return f"{company_name} {self.solution_type} Solar Solution"


# will use through model for the ManyToMany later
# components = models.ManyToManyField(SolutionComponent, through='SolarSolutionComponent', related_name='solar_solutions')
#
# class SolarSolutionComponent(models.Model):
#     solar_solution = models.ForeignKey(SolarSolution, on_delete=models.CASCADE)
#     solution_component = models.ForeignKey(SolutionComponent, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1, help_text="Quantity of the component")
#     condition = models.CharField(max_length=50, help_text="Condition of the component (e.g., new, used)")
#
#     class Meta:
#         unique_together = ('solar_solution', 'solution_component')  # Ensure unique combinations


class Service(TimeStampedModel):
    solution = models.OneToOneField(SolarSolution, related_name='service', on_delete=models.CASCADE)
    dc_earthing_included = models.BooleanField(default=False, help_text="Is DC Earthing included?")
    afss_included = models.BooleanField(default=False, help_text="Is AFSS included?")
    afss_warranty_years = models.PositiveIntegerField(null=True, blank=True,
                                                      help_text="AFSS warranty in years if included")
    online_monitoring_included = models.BooleanField(default=False, help_text="Is online monitoring included?")
    net_metering_included = models.BooleanField(default=False, help_text="Is net metering included?")
    hse_equipment_included = models.BooleanField(default=False, help_text="Is HSE service included?")
    transportation_included = models.BooleanField(default=True, help_text="Is transportation included?")
    transportation_distance = models.PositiveIntegerField(blank=True, null=True, help_text="Enter the distance if transportation is included.")


class BuyerInteraction(TimeStampedModel):
    solar_solution = models.ForeignKey(SolarSolution, related_name='interactions', on_delete=models.CASCADE)
    whatsapp_number = models.CharField(max_length=15)


class SolutionMedia(TimeStampedModel):
    solution = models.ForeignKey(SolarSolution, related_name='mediafiles', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, help_text="Upload an image of the solution")
    is_display_image = models.BooleanField(default=False,
                                           help_text="Indicates if this image is the display image for the solution")

    def __str__(self):
        return f"Image for {self.solution} (Display: {self.is_display_image})"
