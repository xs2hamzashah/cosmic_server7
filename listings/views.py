import django_filters
from django.contrib.auth import get_user_model
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile
from accounts.permissions import IsAdmin, IsSeller
from operations.models import Approval
from .models import SolarSolution, Tag, SolutionMedia, SolutionComponent, Service
from .serializers import SolarSolutionListSerializer, SolarSolutionCreateSerializer, SolutionMediaSerializer, \
    SellerReportSerializer, SolarSolutionDetailSerializer, TagSerializer, SolarSolutionUpdateSerializer, \
    SolutionComponentSerializer
from django.db.models import Prefetch, Q


class SolarSolutionViewSet(viewsets.ModelViewSet):
    queryset = SolarSolution.objects.all()
    serializer_class = SolarSolutionListSerializer  # default fallback

    def get_serializer_class(self):
        if self.action == 'list':
            return SolarSolutionListSerializer
        elif self.action == 'create':
            return SolarSolutionCreateSerializer
        elif self.action == 'retrieve':
            return SolarSolutionDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return SolarSolutionUpdateSerializer

    def get_permissions(self):
        """
        Instantiates the appropriate permission instances based on action.
        """
        if self.action == 'create':
            return [AllowAny()]
            # Add other permission classes for other actions as needed.
        return [AllowAny()]

    class SolarSolutionFilter(django_filters.FilterSet):
        CITY_CHOICES = (
            ('ISB', 'Islamabad'),
            ('KAR', 'Karachi'),
            ('LHR', 'Lahore'),
        )

        # SYSTEM_SIZE_CHOICES defines the available options for system sizes.
        # These integers represent the size in kilowatts (KW)
        SYSTEM_SIZE_CHOICES = (
            (5, '5'),
            (10, '10'),
            (15, '15'),
            (20, '20'),
        )
        PRICE_RANGES = (
            ('below_1M', 'Below 1M'),
            ('below_2M', 'Below 2M'),
            ('below_3M', 'Below 3M'),
            ('above_3M', 'Above 3M'),
        )

        city = filters.ChoiceFilter(choices=CITY_CHOICES, field_name='seller__userprofile__company__city',
                                    method='filter_by_city')
        size = filters.ChoiceFilter(choices=SYSTEM_SIZE_CHOICES, field_name='size')
        price = filters.ChoiceFilter(choices=PRICE_RANGES, method='filter_by_price')
        is_seller_page = filters.BooleanFilter(field_name='seller_page', method='filter_by_is_seller_page',
                                            label='Show only seller\'s listing')

        class Meta:
            model = SolarSolution
            fields = ['size', 'price', 'city', 'is_seller_page']

        def filter_by_city(self, queryset, name, value):
            value = value.upper()
            city_map = dict(self.CITY_CHOICES)  # This gives {'ISB': 'Islamabad', 'KAR': 'Karachi', 'LHR': 'Lahore'}
            if value in city_map.keys():
                city_name = city_map[value]

                print(city_name, ' is the city name ')
                # Use Q to filter by the full city name
                return queryset.filter(Q(seller__userprofile__company__city__iexact=city_name))
            return queryset

        def filter_by_price(self, queryset, name, value):
            if value == 'below_1M':
                return queryset.filter(price__lt=1000000)
            elif value == 'below_2M':
                return queryset.filter(price__lt=2000000)
            elif value == 'below_3M':
                return queryset.filter(price__lt=3000000)
            elif value == 'above_3M':
                return queryset.filter(price__gt=3000000)
            return queryset

        def filter_by_is_seller_page(self, queryset, name, value):
            if value and self.request.user.is_authenticated and self.request.user.userprofile.role == 'seller':
                return queryset.filter(seller=self.request.user.userprofile)
            return queryset  # Return the original queryset if conditions are not met

    filter_backends = [DjangoFilterBackend]
    filterset_class = SolarSolutionFilter


    def get_queryset(self):
        if self.action == 'list':
            return SolarSolution.objects.all()
        else:
            # Prefetch related fields for other actions
            return SolarSolution.objects.prefetch_related(
                'tags',
                Prefetch('mediafiles', queryset=SolutionMedia.objects.filter(is_display_image=True)),
                'components'
            ).select_related(
                'seller__userprofile__company',  # Select related to optimize the query for the city filter
                'service'
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        # Validate and save the SolarSolution instance
        serializer = SolarSolutionCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Create the SolarSolution instance
        solar_solution = serializer.save(seller=request.user)

        # Create Approval entry for the newly created SolarSolution
        Approval.objects.create(solution=solar_solution)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tags_data = request.data.pop('tags', [])
        # Handle tags
        tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)

        serializer = SolarSolutionUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_solution = serializer.save()

        # Handle components (SolutionComponent)
        components_data = request.data.get('components', [])
        if components_data:
            updated_solution.components.all().delete()  # Clear existing components
            for component in components_data:
                SolutionComponent.objects.create(solar_solution=updated_solution, **component)

        # Handle service
        service_data = request.data.get('service', None)
        if service_data:
            service_instance = updated_solution.service.first()
            if service_instance:
                for attr, value in service_data.items():
                    setattr(service_instance, attr, value)
                service_instance.save()
            else:
                Service.objects.create(solution=updated_solution, **service_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        print("Partial update called")
        instance = self.get_object()

        # First, handle the tags to avoid unique constraint errors
        tags_data = request.data.pop('tags', None)  # Extract tags from request.data
        if tags_data is not None:
            tags = []
            for tag_data in tags_data:
                tag_name = tag_data.get('name')
                # Check if the tag already exists
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            instance.tags.set(tags)  # Update tags on the instance

        serializer = SolarSolutionUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle components (SolutionComponent)
        components_data = serializer.validated_data.pop('components', None)
        if components_data:
            for component in components_data:
                SolutionComponent.objects.create(solar_solution=instance, **component)

        # Handle service
        service_data = serializer.validated_data.pop('service', None)
        if service_data:
            solar_solution_service = Service.objects.filter(solution=instance).first()  # Get the first match

            if solar_solution_service:
                # Update the existing service
                for attr, value in service_data.items():
                    setattr(solar_solution_service, attr, value)
                solar_solution_service.save()
            else:
                # If no service exists, create a new one
                Service.objects.create(solution=instance, **service_data)

        # Update the main fields
        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Use the filter here
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser, JSONParser])
    def upload_media(self, request, pk=None):
        """
        Upload media for a SolarSolution. Note: Swagger UI does not currently display the image upload field.
        You can use form-data to upload an image (and the is_display_image field) into this API using tools like Postman
        """
        solar_solution = self.get_object()  # Get the specific SolarSolution instance

        # Get the uploaded media file
        media_file = request.FILES.get('media')

        # Get the is_display_image flag
        is_display_image = request.data.get('is_display_image', False)

        # Prepare data for the serializer
        media_data = {
            'image': media_file,
            'is_display_image': is_display_image
        }

        # Use the serializer to validate the data
        serializer = SolutionMediaSerializer(data=media_data)
        serializer.is_valid(raise_exception=True)  # Raises an error if validation fails

        # If the current image is marked as display image, update other images
        if is_display_image:
            SolutionMedia.objects.filter(solution=solar_solution, is_display_image=True).update(is_display_image=False)

        # Create a SolutionMedia instance
        SolutionMedia.objects.create(solution=solar_solution, **serializer.validated_data)
        return Response({'status': 'media file uploaded'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def available_components(self, request):
        components = SolutionComponent.objects.all()  # Get all available components
        serializer = SolutionComponentSerializer(components, many=True)  # Serialize the components
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def admin_analytics(self, request):
        sellers = UserProfile.objects.filter(role='seller')
        report = []

        for seller in sellers:
            solar_products = SolarSolution.objects.filter(seller=seller.user)

            # Do not serialize here, just collect the data
            seller_data = {
                'seller_id': seller.id,
                'seller_name': seller.user.full_name,
                'products': solar_products  # Pass the queryset directly
            }

            report.append(seller_data)

        # Use the SellerReportSerializer to serialize the report data
        serialized_report = SellerReportSerializer(report, many=True)

        return Response({'report': serialized_report.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsSeller])
    def seller_analytics(self, request, pk=None):
        seller = request.user
        solar_products = SolarSolution.objects.filter(seller=seller)

        # Serialize the solar products and their interactions
        serialized_products = SolarSolutionListSerializer(solar_products, many=True).data

        seller_data = {
            'seller_id': seller.id,
            'seller_name': seller.user.full_name,
            'products': serialized_products
        }

        return Response({'report': seller_data}, status=status.HTTP_200_OK)


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

