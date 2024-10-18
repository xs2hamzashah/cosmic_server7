from rest_framework import serializers
from .models import SolarSolution, Tag, SolutionMedia, SolutionComponent, Service, BuyerInteraction


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name']


class SolutionMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = SolutionMedia
        fields = ['image', 'is_display_image']


class SolutionComponentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SolutionComponent
        fields = ['id', 'component_type', 'brand', 'capacity', 'quantity', 'warranty',
                  'details', 'mechanical_material', 'mechanical_structure_type',
                  'civil_material', 'wire_material']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['dc_earthing_included', 'afss_included', 'afss_warranty_years', 'online_monitoring_included',
                  'net_metering_included', 'fire_extinguisher_included', 'transportation_included']


class SolarSolutionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SolarSolution
        fields = ['id' ,'size', 'price', 'solution_type']


class SolarSolutionUpdateSerializer(serializers.ModelSerializer):
    component_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True,
                                          required=False)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True,
                                    required=False)
    service = ServiceSerializer(required=False)

    class Meta:
        model = SolarSolution
        fields = ['size', 'price', 'solution_type', 'tag_ids', 'completion_time_days',
                  'payment_schedule', 'component_ids', 'service']

    def validate_component_ids(self, value):
        # Check if all component IDs are valid
        invalid_ids = []
        for component_id in value:
            if not SolutionComponent.objects.filter(id=component_id).exists():
                invalid_ids.append(component_id)
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid component IDs: {', '.join(map(str, invalid_ids))}")
        return value

    def validate_tag_ids(self, value):
        # Check if all tag IDs are valid
        invalid_ids = []
        for tag_id in value:
            if not Tag.objects.filter(id=tag_id).exists():
                invalid_ids.append(tag_id)
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid tag IDs: {', '.join(map(str, invalid_ids))}")
        return value

class SolarSolutionDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    components = SolutionComponentSerializer(many=True)
    service = ServiceSerializer()
    images = SolutionMediaSerializer(many=True, source='mediafiles')  # Use the related name for images

    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'tags', 'completion_time_days',
                  'payment_schedule', 'components', 'service', 'images']


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
