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


class BaseViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PanelViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_panels(self, request):
        seller = self.request.user.userprofile
        panel_qs = Panel.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(panel_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(panel_qs, many=True)
        return Response(serializer.data)


class MechanicalWorkViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_mechanical_works(self, request):
        seller = self.request.user.userprofile
        mechanical_work_qs = MechanicalWork.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(mechanical_work_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(mechanical_work_qs, many=True)
        return Response(serializer.data)


class AfterSalesServiceViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_after_sales_services(self, request):
        seller = self.request.user.userprofile
        after_sales_service_qs = AfterSalesService.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(after_sales_service_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(after_sales_service_qs, many=True)
        return Response(serializer.data)


class BmsViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_bms(self, request):
        seller = self.request.user.userprofile
        bms_qs = Bms.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(bms_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(bms_qs, many=True)
        return Response(serializer.data)


class CivilWorkViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_civil_works(self, request):
        seller = self.request.user.userprofile
        civil_work_qs = CivilWork.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(civil_work_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(civil_work_qs, many=True)
        return Response(serializer.data)


class DcEarthingViewSet(BaseViewSet):
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
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_dc_earthings(self, request):
        seller = self.request.user.userprofile
        dc_earthing_qs = DcEarthing.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(dc_earthing_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(dc_earthing_qs, many=True)
        return Response(serializer.data)


class ElectricWorkViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_electrical_works(self, request):
        seller = self.request.user.userprofile
        electrical_work_qs = ElectricWork.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(electrical_work_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(electrical_work_qs, many=True)
        return Response(serializer.data)


class HseEquipmentViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_hse_equipments(self, request):
        seller = self.request.user.userprofile
        hse_equipment_qs = HseEquipment.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(hse_equipment_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(hse_equipment_qs, many=True)
        return Response(serializer.data)


class InverterViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_inverters(self, request):
        seller = self.request.user.userprofile
        inverter_qs = Inverter.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(inverter_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(inverter_qs, many=True)
        return Response(serializer.data)


class BatteryViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_batteries(self, request):
        seller = self.request.user.userprofile
        battery_qs = Battery.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(battery_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(battery_qs, many=True)
        return Response(serializer.data)


class NetMeteringViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_net_meterings(self, request):
        seller = self.request.user.userprofile
        net_metering_qs = NetMetering.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(net_metering_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(net_metering_qs, many=True)
        return Response(serializer.data)


class OnlineMonitoringViewSet(BaseViewSet):
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
        serializer.save(seller=seller)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user.userprofile)

    @action(detail=False, methods=['get'])
    def my_online_monitorings(self, request):
        seller = self.request.user.userprofile
        online_monitoring_qs = OnlineMonitoring.objects.filter(seller=seller).order_by('id')

        # Apply pagination to the queryset
        page = self.paginate_queryset(online_monitoring_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, return all objects
        serializer = self.get_serializer(online_monitoring_qs, many=True)
        return Response(serializer.data)
