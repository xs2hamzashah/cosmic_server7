from rest_framework import serializers

from pricelist.models import (Panel,MechanicalWork, AfterSalesService, Bms, CivilWork, DcEarthing, ElectricWork,
                              HseEquipment, Inverter, Battery, NetMetering, OnlineMonitoring)


class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ["id", "brand_name","specification","capacity","unit","price"]


class MechanicalWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicalWork
        fields = ["id", "structure_type", "specification", "unit", "price"]


class AfterSalesServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfterSalesService
        fields = ["id", "specification", "capacity", "unit", "price"]


class BmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bms
        fields = ["id", "brand_name", "specification", "capacity", "unit", "price"]


class CivilWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilWork
        fields = ["id", "specification", "capacity", "unit", "price"]


class DcEarthingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcEarthing
        fields = ["id", "specification", "capacity", "unit", "price"]


class ElectricWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricWork
        fields = ["id", "specification", "system_type", "unit", "price"]


class HseEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HseEquipment
        fields = ["id", "specification", "capacity", "unit", "price"]


class InverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inverter
        fields = ["id", "brand_name", "system_type", "specification", "capacity", "unit", "price"]


class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = ["id", "brand_name", "system_type", "specification", "capacity", "unit", "price"]


class NetMeteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetMetering
        fields = ["id", "specification", "capacity", "unit", "price"]


class OnlineMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineMonitoring
        fields = ["id", "specification", "capacity", "unit", "price"]
