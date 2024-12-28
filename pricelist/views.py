from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.decorators import action

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
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Panel.objects.filter(seller=self.request.user.userprofile)
        return Panel.objects.all()



    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        # Check if a panel already exists for this seller
        if Panel.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A panel for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_panel(self, request):
        seller = self.request.user.userprofile
        try:
            panel = Panel.objects.get(seller=seller)
        except Panel.DoesNotExist:
            raise NotFound({"detail": "No panel found for this seller."})

        serializer = self.get_serializer(panel)
        return Response(serializer.data)


class MechanicalWorkViewSet(viewsets.ModelViewSet):
    queryset = MechanicalWork.objects.all()
    serializer_class = MechanicalWorkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MechanicalWork.objects.filter(seller=self.request.user.userprofile)
        return MechanicalWork.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if MechanicalWork.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A mechanical work for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_mechanical_work(self, request):
        seller = self.request.user.userprofile
        try:
            mechanical_work = MechanicalWork.objects.get(seller=seller)
        except MechanicalWork.DoesNotExist:
            raise NotFound({"detail": "No mechanical work found for this seller."})

        serializer = self.get_serializer(mechanical_work)
        return Response(serializer.data)


class AfterSalesServiceViewSet(viewsets.ModelViewSet):
    queryset = AfterSalesService.objects.all()
    serializer_class = AfterSalesServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AfterSalesService.objects.filter(seller=self.request.user.userprofile)
        return AfterSalesService.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if AfterSalesService.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "An after sales service for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_after_sales_service(self, request):
        seller = self.request.user.userprofile
        try:
            after_sales_service = AfterSalesService.objects.get(seller=seller)
        except AfterSalesService.DoesNotExist:
            raise NotFound({"detail": "No after-sales service found for this seller."})

        serializer = self.get_serializer(after_sales_service)
        return Response(serializer.data)


class BmsViewSet(viewsets.ModelViewSet):
    queryset = Bms.objects.all()
    serializer_class = BmsSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Bms.objects.filter(seller=self.request.user.userprofile)
        return Bms.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if Bms.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A BMS for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_bms(self, request):
        seller = self.request.user.userprofile
        try:
            bms = Bms.objects.get(seller=seller)
        except Bms.DoesNotExist:
            raise NotFound({"detail": "No BMS found for this seller."})

        serializer = self.get_serializer(bms)
        return Response(serializer.data)


class CivilWorkViewSet(viewsets.ModelViewSet):
    queryset = CivilWork.objects.all()
    serializer_class = CivilWorkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CivilWork.objects.filter(seller=self.request.user.userprofile)
        return CivilWork.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if CivilWork.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A civil work for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_civil_work(self, request):
        seller = self.request.user.userprofile
        try:
            civil_work = CivilWork.objects.get(seller=seller)
        except CivilWork.DoesNotExist:
            raise NotFound({"detail": "No civil work found for this seller."})

        serializer = self.get_serializer(civil_work)
        return Response(serializer.data)


class DcEarthingViewSet(viewsets.ModelViewSet):
    queryset = DcEarthing.objects.all()
    serializer_class = DcEarthingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return DcEarthing.objects.filter(seller=self.request.user.userprofile)
        return DcEarthing.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if DcEarthing.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A DC earthing for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)\

    @action(detail=False, methods=['get'])
    def my_dc_earthing(self, request):
        seller = self.request.user.userprofile
        try:
            dc_earthing = DcEarthing.objects.get(seller=seller)
        except DcEarthing.DoesNotExist:
            raise NotFound({"detail": "No DC Earthing found for this seller."})

        serializer = self.get_serializer(dc_earthing)
        return Response(serializer.data)


class ElectricWorkViewSet(viewsets.ModelViewSet):
    queryset = ElectricWork.objects.all()
    serializer_class = ElectricWorkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ElectricWork.objects.filter(seller=self.request.user.userprofile)
        return ElectricWork.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if ElectricWork.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "An electric work for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_electrical_work(self, request):
        seller = self.request.user.userprofile
        try:
            electrical_work = ElectricWork.objects.get(seller=seller)
        except ElectricWork.DoesNotExist:
            raise NotFound({"detail": "No Electrical work found for this seller."})

        serializer = self.get_serializer(electrical_work)
        return Response(serializer.data)

class HseEquipmentViewSet(viewsets.ModelViewSet):
    queryset = HseEquipment.objects.all()
    serializer_class = HseEquipmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return HseEquipment.objects.filter(seller=self.request.user.userprofile)
        return HseEquipment.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if HseEquipment.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "An HSE equipment for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_hse_equipment(self, request):
        seller = self.request.user.userprofile
        try:
            hse_equipment = HseEquipment.objects.get(seller=seller)
        except HseEquipment.DoesNotExist:
            raise NotFound({"detail": "No HSE Equipment found for this seller."})

        serializer = self.get_serializer(hse_equipment)
        return Response(serializer.data)


class InverterViewSet(viewsets.ModelViewSet):
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Inverter.objects.filter(seller=self.request.user.userprofile)
        return Inverter.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if Inverter.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "An inverter for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_inverter(self, request):
        seller = self.request.user.userprofile
        try:
            inverter = Inverter.objects.get(seller=seller)
        except Inverter.DoesNotExist:
            raise NotFound({"detail": "No inverter found for this seller."})

        serializer = self.get_serializer(inverter)
        return Response(serializer.data)


class BatteryViewSet(viewsets.ModelViewSet):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Battery.objects.filter(seller=self.request.user.userprofile)
        return Battery.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if Battery.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A battery for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_battery(self, request):
        seller = self.request.user.userprofile
        try:
            battery = Battery.objects.get(seller=seller)
        except Battery.DoesNotExist:
            raise NotFound({"detail": "No battery found for this seller."})

        serializer = self.get_serializer(battery)
        return Response(serializer.data)


class NetMeteringViewSet(viewsets.ModelViewSet):
    queryset = NetMetering.objects.all()
    serializer_class = NetMeteringSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return NetMetering.objects.filter(seller=self.request.user.userprofile)
        return NetMetering.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if NetMetering.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "A net metering for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_net_metering(self, request):
        seller = self.request.user.userprofile
        try:
            net_metering = NetMetering.objects.get(seller=seller)
        except NetMetering.DoesNotExist:
            raise NotFound({"detail": "No net metering found for this seller."})

        serializer = self.get_serializer(net_metering)
        return Response(serializer.data)


class OnlineMonitoringViewSet(viewsets.ModelViewSet):
    queryset = OnlineMonitoring.objects.all()
    serializer_class = OnlineMonitoringSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return OnlineMonitoring.objects.filter(seller=self.request.user.userprofile)
        return OnlineMonitoring.objects.all()

    def perform_create(self, serializer):
        seller = self.request.user.userprofile
        if OnlineMonitoring.objects.filter(seller=seller).exists():
            raise ValidationError({"detail": "An online monitoring for this seller already exists."})
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_online_monitoring(self, request):
        seller = self.request.user.userprofile
        try:
            online_monitoring = OnlineMonitoring.objects.get(seller=seller)
        except OnlineMonitoring.DoesNotExist:
            raise NotFound({"detail": "No battery found for this seller."})

        serializer = self.get_serializer(online_monitoring)
        return Response(serializer.data)
