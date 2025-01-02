from django.core.validators import MaxLengthValidator
from rest_framework import serializers

from accounts.models import UserProfile
from accounts.serializers import CompanySerializer
from operations.models import Approval
from operations.serializers import ApprovalSerializer
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
        fields = ['id', 'image', 'is_display_image']


class UpdateMediaSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(required=True)
    is_display_image = serializers.BooleanField(required=False)


class SolutionComponentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SolutionComponent
        fields = ['id', 'component_type', 'subtype', 'brand', 'capacity', 'quantity', 'warranty', 'ip_rating',
                  'details', 'mechanical_material', 'mechanical_structure_type', 'total_backup_capacity',
                  'civil_material', 'wire_material']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['dc_earthing_included', 'afss_included', 'afss_warranty_years', 'online_monitoring_included',
                  'net_metering_included', 'hse_equipment_included', 'transportation_included', 'transportation_distance']


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
    seller_note = serializers.CharField(validators=[MaxLengthValidator(500)], required=False, allow_blank=True)


    class Meta:
        model = SolarSolution
        fields = ['size', 'price', 'solution_type', 'tag_ids', 'completion_time_days',
                  'payment_schedule', 'component_ids', 'service', 'seller_note']

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


class SolarSolutionApprovalSerializer(ApprovalSerializer):
    class Meta:
        model = Approval
        fields = ['admin_verified']

class SolarSolutionDetailSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    components = SolutionComponentSerializer(many=True)
    service = ServiceSerializer()
    images = SolutionMediaSerializer(many=True, source='mediafiles')  # Use the related name for images
    approval = SolarSolutionApprovalSerializer()
    seller_note = serializers.CharField(validators=[MaxLengthValidator(500)], required=False, allow_blank=True)
    company = CompanySerializer(source='seller.company')

    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'tags', 'completion_time_days',
                  'payment_schedule', 'components', 'service', 'images', 'approval', 'seller_note',
                  'display_name', 'city', 'company']

    def get_city(self, obj):
        company = getattr(obj.seller, 'company', None)
        return company.city


class BuyerInteractionSerializer(serializers.ModelSerializer):
    whatsapp_number = serializers.CharField()

    class Meta:
        model = BuyerInteraction
        fields = ['whatsapp_number']


class SolarSolutionListSerializer(serializers.ModelSerializer):
    # buyer_interaction_count, buyer_whatsapp_count, these fields will be be included on the Seller Page
    # we'll make enhancement for this in Future.
    # or we create another Seperate Api for seller page
    buyer_interaction_count = serializers.SerializerMethodField()
    buyer_whatsapp_numbers = BuyerInteractionSerializer(many=True, source='interactions')
    images = SolutionMediaSerializer(many=True, source='mediafiles')  # Use the related name for images
    seller_note = serializers.CharField(validators=[MaxLengthValidator(500)], required=False, allow_blank=True)
    city = serializers.SerializerMethodField()
    is_approved = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = SolarSolution
        fields = ['id', 'size', 'price', 'solution_type', 'completion_time_days', 'payment_schedule',
                  'buyer_interaction_count', 'buyer_whatsapp_numbers', 'images', 'seller_note',
                  'display_name', 'city', 'is_approved', 'company']

    def get_buyer_interaction_count(self, obj):
        # Count the number of interactions related to this SolarSolution
        return obj.interactions.count()


    def get_city(self, obj):
        seller = getattr(obj.seller, 'userprofile', None)
        if seller and seller.role == UserProfile.Role.SELLER:
            company = getattr(seller, 'company', None)
            return getattr(company, 'city', None) if company else None
        return None

    def get_is_approved(self, obj):
        approval = getattr(obj, 'approval', None)
        return approval.admin_verified if approval else False

    def get_company(self, obj):
        seller = obj.seller
        if seller and seller.role == UserProfile.Role.SELLER:
            company = getattr(seller, 'company', None)
            return company.name
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Check if request and user exist
        if request and hasattr(request, 'user'):
            user = request.user

            # Handle anonymous users
            if user.is_anonymous or not hasattr(user, 'userprofile'):
                representation.pop('is_approved', None)
                representation.pop('buyer_interaction_count', None)
                representation.pop('buyer_whatsapp_numbers', None)

            else:
                # If the user is not an admin or a seller, remove sensitive fields
                if user.userprofile.role not in [UserProfile.Role.ADMIN, UserProfile.Role.SELLER]:
                    representation.pop('is_approved', None)
                    representation.pop('buyer_interaction_count', None)
                    representation.pop('buyer_whatsapp_numbers', None)

        return representation


class BuyerPerPackageSerializer(serializers.Serializer):
    solar_solution_id = serializers.IntegerField(source='solar_solution__id')
    package_buyers = serializers.IntegerField()


class SellerReportSerializer(serializers.Serializer):
    seller_id = serializers.IntegerField()
    seller_name = serializers.CharField()
    total_buyers = serializers.IntegerField()
    buyers_per_package = BuyerPerPackageSerializer(many=True)
    products = SolarSolutionListSerializer(many=True)


class SellerCityCountSerializer(serializers.Serializer):
    city = serializers.CharField(source='company__city')
    count = serializers.IntegerField(source='city_sellers', required=False)


class BuyerCityCountSerializer(serializers.Serializer):
    city = serializers.CharField(source='company__city')
    count = serializers.IntegerField(source='city_buyers', required=False)


class SellerAnalyticsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    seller_by_city_count = SellerCityCountSerializer(many=True)


class BuyerAnalyticsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    buyer_by_city_count = BuyerCityCountSerializer(many=True)


class SolutionAnalyticsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    approved = serializers.IntegerField()
    unapproved = serializers.IntegerField()


class AdminAnalyticsSerializer(serializers.Serializer):
    sellers = SellerAnalyticsSerializer()
    solar_solutions = SolutionAnalyticsSerializer()
    buyers = BuyerAnalyticsSerializer()
