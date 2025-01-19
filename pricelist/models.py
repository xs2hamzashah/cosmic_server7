from django.db import models

from accounts.models import Company, UserProfile
from core.models import TimeStampedModel


class PriceListUnitType(models.TextChoices):
    watt = 'watt', 'watt'
    kw = "kw", "kw"


class SystemType(models.TextChoices):
    onGrid = "on_grid","on_grid"
    hybrid = "hybrid","hybrid"
    vfd = "vfd","vfd"


class BatteryType(models.TextChoices):
    tubular = "tubular","tubular"
    lithium = "lithium","lithium"


class StructureType(models.TextChoices):
    iron_standard = "iron_standard","iron_standard"
    aluminum_standard = "aluminum_standard","aluminum_standard"
    ms_iron_standard = "ms_iron_standard", "ms_iron_standard"


# panel/
class Panel(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='panels', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)


# /mechanical-work
class MechanicalWork(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='mechanical_works', on_delete=models.CASCADE)
    structure_type = models.CharField(max_length=20, choices=StructureType.choices)
    specification = models.CharField(max_length=200)
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# after-sales-service
class AfterSalesService(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='after_sales_services', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)


# /bms
class Bms(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='bms', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /civil-work
class CivilWork(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='civil_works', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /dc-earthing
class DcEarthing(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='dc_earthings', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# electric-work
class ElectricWork(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='electrical_works', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=SystemType.choices)
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /hse-equipment
class HseEquipment(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='hse_equipments', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /inverter
class Inverter(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='inverters', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=SystemType.choices)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /battery
class Battery(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='batteries', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=BatteryType.choices)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /net-marketing
class NetMetering(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='net_meterings', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()


# /online-marketing
class OnlineMonitoring(TimeStampedModel):
    seller = models.ForeignKey(UserProfile, related_name='online_monitorings', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType.choices)
    price = models.IntegerField()
