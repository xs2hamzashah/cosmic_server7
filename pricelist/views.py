from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.models import UserProfile
from accounts.permissions import IsAdminOrSeller
from .serializers import (
    PanelSerializer,
    MechanicalWorkSerializer,
    AfterSalesServiceSerializer,
    BmsSerializer,
    CivilWorkSerializer,
    DcEarthingSerializer,
    ElectricWorkSerializer,
    HseEquipmentSerializer,
    InverterSerializer,
    BatterySerializer,
    NetMeteringSerializer,
    OnlineMonitoringSerializer
)
from .models import (
    Panel,
    MechanicalWork,
    AfterSalesService,
    Bms,
    CivilWork,
    DcEarthing,
    ElectricWork,
    HseEquipment,
    Inverter,
    Battery,
    NetMetering,
    OnlineMonitoring
)


class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return Panel.objects.filter(seller=self.request.user.userprofile)
        return Panel.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class MechanicalWorkViewSet(viewsets.ModelViewSet):
    queryset = MechanicalWork.objects.all()
    serializer_class = MechanicalWorkSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return MechanicalWork.objects.filter(seller=self.request.user.userprofile)
        return MechanicalWork.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class AfterSalesServiceViewSet(viewsets.ModelViewSet):
    queryset = AfterSalesService.objects.all()
    serializer_class = AfterSalesServiceSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return AfterSalesService.objects.filter(seller=self.request.user.userprofile)
        return AfterSalesService.objects.all()

    def perform_create(self, serializer):
        # Automatically set the seller to the current user's seller
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class BmsViewSet(viewsets.ModelViewSet):
    queryset = Bms.objects.all()
    serializer_class = BmsSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return Bms.objects.filter(seller=self.request.user.userprofile)
        return Bms.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class CivilWorkViewSet(viewsets.ModelViewSet):
    queryset = CivilWork.objects.all()
    serializer_class = CivilWorkSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return CivilWork.objects.filter(seller=self.request.user.userprofile)
        return CivilWork.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class DcEarthingViewSet(viewsets.ModelViewSet):
    queryset = DcEarthing.objects.all()
    serializer_class = DcEarthingSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return DcEarthing.objects.filter(seller=self.request.user.userprofile)
        return DcEarthing.objects.all()

    def perform_create(self, serializer):
        # Automatically set the seller to the current user's seller
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class ElectricWorkViewSet(viewsets.ModelViewSet):
    queryset = ElectricWork.objects.all()
    serializer_class = ElectricWorkSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return ElectricWork.objects.filter(seller=self.request.user.userprofile)
        return ElectricWork.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class HseEquipmentViewSet(viewsets.ModelViewSet):
    queryset = HseEquipment.objects.all()
    serializer_class = HseEquipmentSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return HseEquipment.objects.filter(seller=self.request.user.userprofile)
        return HseEquipment.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class InverterViewSet(viewsets.ModelViewSet):
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return Inverter.objects.filter(seller=self.request.user.userprofile)
        return Inverter.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class BatteryViewSet(viewsets.ModelViewSet):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return Battery.objects.filter(seller=self.request.user.userprofile)
        return Battery.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class NetMeteringViewSet(viewsets.ModelViewSet):
    queryset = NetMetering.objects.all()
    serializer_class = NetMeteringSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return NetMetering.objects.filter(seller=self.request.user.userprofile)
        return NetMetering.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)


class OnlineMonitoringViewSet(viewsets.ModelViewSet):
    queryset = OnlineMonitoring.objects.all()
    serializer_class = OnlineMonitoringSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if (self.request.user.is_authenticated and
                not self.request.user.userprofile.role in [UserProfile.role.ADMIN, UserProfile.role.SELLER]):
            return OnlineMonitoring.objects.filter(seller=self.request.user.userprofile)
        return OnlineMonitoring.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)
