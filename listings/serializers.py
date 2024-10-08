from rest_framework import serializers
from .models import SolarSolution, Tag, SolutionMedia, SolutionDetails, Service


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class SolutionMediaSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SolutionMedia
        fields = ['image', 'image_url', 'is_display_image']

    def get_image_url(self, obj):
        # Ensure obj is of type SolutionMedia
        if isinstance(obj, SolutionMedia):
            request = self.context.get('request')
            if obj.image and request:
                return request.build_absolute_uri(obj.image.url)
        return None


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
    mediafiles = SolutionMediaSerializer(many=True)
    components = SolutionDetailsSerializer(many=True)
    services = ServiceSerializer(many=True)

    class Meta:
        model = SolarSolution
        fields = ['size', 'price', 'solution_type', 'tags', 'completion_time_days', 'payment_schedule', 'mediafiles',
                  'components', 'services']


class SolarSolutionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'completion_time_days', 'payment_schedule']
