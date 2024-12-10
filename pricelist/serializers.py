from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from pricelist.models import (Panel,MechanicalWork, AfterSalesService, Bms, CivilWork, DcEarthing, ElectricWork,
                              HseEquipment, Inverter, Battery, NetMetering, OnlineMonitoring)


class PanelSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Panel
        fields = ["id" ,"seller","brand_name","specification","capacity","unit","price"]


class MechanicalWorkSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = MechanicalWork
        fields = ["id", "seller", "structure_type", "specification", "unit", "price"]


class AfterSalesServiceSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = AfterSalesService
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class BmsSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Bms
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class CivilWorkSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = CivilWork
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class DcEarthingSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = DcEarthing
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class ElectricWorkSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = ElectricWork
        fields = ["id", "seller", "specification", "system_type", "unit", "price"]


class HseEquipmentSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = HseEquipment
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class InverterSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Inverter
        fields = ["id", "seller", "brand_name", "system_type", "specification", "capacity", "unit", "price"]


class BatterySerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Battery
        fields = ["id", "seller", "brand_name", "system_type", "specification", "capacity", "unit", "price"]


class NetMeteringSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = NetMetering
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]


class OnlineMonitoringSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = OnlineMonitoring
        fields = ["id", "seller", "specification", "capacity", "unit", "price"]
