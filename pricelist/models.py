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
    seller = models.OneToOneField(UserProfile, related_name='panel', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /mechanical-work
class MechanicalWork(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='mechanical_work', on_delete=models.CASCADE)
    structure_type = models.CharField(max_length=20,choices=StructureType)
    specification = models.CharField(max_length=200)
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# after-sales-service
class AfterSalesService(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='after_sales_service', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /bms
class Bms(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='bms', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /civil-work
class CivilWork(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='civil_work', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /dc-earthing
class DcEarthing(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='dc_earthing', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# electric-work
class ElectricWork(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='electrical_work', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=SystemType)
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /hse-equipment
class HseEquipment(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='hse_equipment', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()



# /inverter
class Inverter(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='inverter', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=SystemType)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /battery
class Battery(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='battery', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20, choices=BatteryType)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /net-marketing
class NetMetering(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='net_metering', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


# /online-marketing
class OnlineMonitoring(TimeStampedModel):
    seller = models.OneToOneField(UserProfile, related_name='online_monitoring', on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    capacity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=PriceListUnitType)
    price = models.IntegerField()


