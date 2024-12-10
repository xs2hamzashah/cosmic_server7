from rest_framework.routers import DefaultRouter
from .views import (
    PanelViewSet,
    MechanicalWorkViewSet,
    AfterSalesServiceViewSet,
    BmsViewSet,
    CivilWorkViewSet,
    DcEarthingViewSet,
    ElectricWorkViewSet,
    HseEquipmentViewSet,
    InverterViewSet,
    BatteryViewSet,
    NetMeteringViewSet,
    OnlineMonitoringViewSet
)

router = DefaultRouter()
router.register(r'panel', PanelViewSet, basename='panel')
router.register(r'mechanical-work', MechanicalWorkViewSet, basename='mechanical-work')
router.register(r'after-sales-service', AfterSalesServiceViewSet, basename='after-sales-service')
router.register(r'bms', BmsViewSet, basename='bms')
router.register(r'civil-work', CivilWorkViewSet, basename='civil-work')
router.register(r'dc-earthing', DcEarthingViewSet, basename='dc-earthing')
router.register(r'electric-work', ElectricWorkViewSet, basename='electric-work')
router.register(r'hse-equipment', HseEquipmentViewSet, basename='hse-equipment')
router.register(r'inverter', InverterViewSet, basename='inverter')
router.register(r'battery', BatteryViewSet, basename='battery')
router.register(r'net-metering', NetMeteringViewSet, basename='net-metering')
router.register(r'online-monitoring', OnlineMonitoringViewSet, basename='online-monitoring')

urlpatterns = router.urls
