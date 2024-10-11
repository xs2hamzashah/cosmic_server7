from rest_framework import serializers
from .models import SolarSolution, Tag, SolutionMedia, SolutionDetails, Service, BuyerInteraction


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class SolutionMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = SolutionMedia
        fields = ['image', 'is_display_image']


class SolutionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionDetails
        fields = ['details_type', 'brand', 'capacity', 'quantity', 'warranty',
                  'details', 'mechanical_material', 'mechanical_structure_type',
                  'civil_material', 'wire_material']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['dc_earthing_included', 'afss_included', 'afss_warranty_years', 'online_monitoring_included',
                  'net_metering_included', 'fire_extinguisher_included', 'transportation_included']


class SolarSolutionCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)  # will check if it required or not
    components = SolutionDetailsSerializer(many=True)
    services = ServiceSerializer(many=True)

    class Meta:
        model = SolarSolution
        fields = ['size', 'price', 'solution_type', 'tags', 'completion_time_days', 'payment_schedule',
                  'components', 'services']


class SolarSolutionDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    components = SolutionDetailsSerializer(many=True)
    services = ServiceSerializer(many=True)
    images = SolutionMediaSerializer(many=True, source='mediafiles')  # Use the related name for images

    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'tags', 'completion_time_days',
                  'payment_schedule', 'components', 'services', 'images']


class BuyerInteractionSerializer(serializers.ModelSerializer):
    whatsapp_number = serializers.CharField()

    class Meta:
        model = BuyerInteraction
        fields = ['whatsapp_number']


class SolarSolutionListSerializer(serializers.ModelSerializer):
    buyer_interaction_count = serializers.SerializerMethodField()
    buyer_whatsapp_numbers = BuyerInteractionSerializer(many=True, source='interactions')

    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'completion_time_days', 'payment_schedule',
                  'buyer_interaction_count', 'buyer_whatsapp_numbers']

    def get_buyer_interaction_count(self, obj):
        # Count the number of interactions related to this SolarSolution
        return obj.interactions.count()


class SellerReportSerializer(serializers.Serializer):
    seller_id = serializers.IntegerField()
    seller_name = serializers.CharField()
    products = SolarSolutionListSerializer(many=True)
