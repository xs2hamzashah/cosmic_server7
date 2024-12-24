import django_filters
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile
from accounts.permissions import IsAdmin, IsSeller, IsAdminOrSeller
from operations.models import Approval
from .models import SolarSolution, Tag, SolutionMedia, SolutionComponent, Service, BuyerInteraction
from .serializers import SolarSolutionListSerializer, SolarSolutionCreateSerializer, SolutionMediaSerializer, \
    SellerReportSerializer, SolarSolutionDetailSerializer, TagSerializer, SolarSolutionUpdateSerializer, \
    SolutionComponentSerializer, AdminAnalyticsSerializer, UpdateMediaSerializer
from django.db.models import Prefetch, Q, Count, F


class SolarSolutionViewSet(viewsets.ModelViewSet):
    queryset = SolarSolution.objects.all()
    serializer_class = SolarSolutionListSerializer  # default fallback
    # ordering fields
    # search fields

    def get_serializer_class(self):
        if self.action == 'list':
            return SolarSolutionListSerializer
        elif self.action == 'create':
            return SolarSolutionCreateSerializer
        elif self.action == 'retrieve':
            return SolarSolutionDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return SolarSolutionUpdateSerializer

        # Add a fallback to prevent returning None
        return self.serializer_class

    def get_permissions(self):
        """
        Instantiates the appropriate permission instances based on action.
        """
        if self.action in ['create', 'update', 'partial_update', 'upload_media']:
            return [IsAdminOrSeller()]
        elif self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminOrSeller()]

    class SolarSolutionFilter(django_filters.FilterSet):
        CITY_CHOICES = (
            ('ISB', 'Islamabad'),
            ('KAR', 'Karachi'),
            ('LHR', 'Lahore'),
        )

        PRICE_RANGES = (
            ('below_1M', 'Below 1M'),
            ('below_2M', 'Below 2M'),
            ('below_3M', 'Below 3M'),
            ('above_3M', 'Above 3M'),
        )

        city = filters.ChoiceFilter(choices=CITY_CHOICES, field_name='seller__company__city',
                                    method='filter_by_city')
        size = django_filters.NumberFilter(field_name='size', method='filter_by_size')
        price = filters.ChoiceFilter(choices=PRICE_RANGES, method='filter_by_price')
        is_seller_page = filters.BooleanFilter(field_name='seller_page', method='filter_by_is_seller_page',
                                            label='Show only seller\'s listing')
        approved = filters.BooleanFilter(field_name='approved', method='filter_by_approved')

        class Meta:
            model = SolarSolution
            fields = ['size', 'price', 'city', 'is_seller_page', 'seller']

        def filter_by_city(self, queryset, name, value):
            value = value.upper()
            city_map = dict(self.CITY_CHOICES)  # This gives {'ISB': 'Islamabad', 'KAR': 'Karachi', 'LHR': 'Lahore'}
            if value in city_map.keys():
                city_name = city_map[value]

                # Use Q to filter by the full city name
                return queryset.filter(Q(seller__company__city__iexact=city_name))
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

        def filter_by_size(self, queryset, name, value):
            if value is not None and 0 < value <= 200:
                return queryset.filter(size=value)
            return queryset

        def filter_by_is_seller_page(self, queryset, name, value):
            if (value and self.request.user.is_authenticated and
                    self.request.user.userprofile.role == UserProfile.role.SELLER):
                return queryset.filter(seller=self.request.user.userprofile)
            return queryset

        def filter_by_approved(self, queryset, name, value):
            if value:
                return queryset.filter(approval__is_approved=value)
            return queryset

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SolarSolutionFilter


    def get_queryset(self):
        solar_solution_qs = SolarSolution.objects.select_related(
            'seller', 'service',
            'seller__user',
            'seller__company'
        ).prefetch_related(
            'interactions',
            Prefetch('mediafiles', queryset=SolutionMedia.objects.filter(is_display_image=True)),
        )

        if self.action == 'list':
            return solar_solution_qs
        else:
            return solar_solution_qs.select_related(
                'service',
                'approval'
            ).prefetch_related(
                'tags',
                'components'
            ).order_by('id')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        existing_pass = user_profile.subscriptions.exists()
        # TODO: will come to this after we implement the payment
        # if not existing_pass:
        #     raise ValidationError("Please purchase a plan first before creating a solar solution.")

        solar_solution = serializer.save(seller=user_profile)
        Approval.objects.create(solution=solar_solution)

    def perform_update(self, serializer):
        instance = serializer.save()  # Save the instance first

        # Handle existing components
        component_ids = serializer.validated_data.get('component_ids', [])
        if component_ids:
            existing_components = SolutionComponent.objects.filter(id__in=component_ids)
            instance.components.set(existing_components)

        # Handle tags
        tag_ids = serializer.validated_data.get('tag_ids', [])
        if tag_ids:
            existing_tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(existing_tags)

        # Handle media files
        # need to handle like either they want to delete the image, update the image is_display_field,
        media_files = serializer.validated_data.get('media_files', [])
        if media_files:
            existing_media_files = SolutionMedia.objects.filter(id__in=media_files)
            instance.mediafiles.set(existing_media_files)

        # Handle service
        service_data = serializer.validated_data.get('service', None)
        if service_data:
            services_qs = Service.objects.filter(solution=instance)
            if services_qs:
                service_instance = services_qs.first()
                for attr, value in service_data.items():
                    setattr(service_instance, attr, value)
                service_instance.save()
            else:
                Service.objects.create(solution=instance, **service_data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # handle service in here
        service_data = serializer.validated_data.pop('service', None)
        if service_data:
            services_qs = Service.objects.filter(solution=instance)
            if services_qs:
                service_instance = services_qs.first()
                for attr, value in service_data.items():
                    setattr(service_instance, attr, value)
                service_instance.save()
            else:
                Service.objects.create(solution=instance, **service_data)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Use the filter here
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Upload a media file for a SolarSolution.",
        request_body=SolutionMediaSerializer,
        responses={201: "Media uploaded", 400: "Invalid input"}
    )
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_media(self, request, pk=None):
        """
        Upload a single media file for a SolarSolution.
        """
        solar_solution = self.get_object()  # Get the specific SolarSolution instance
        if not solar_solution.seller == request.user.userprofile:
            raise ValidationError("You are not allowed to upload media for this solution.")

        # Use the serializer to validate the data
        serializer = SolutionMediaSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the current image is marked as display image
            if serializer.validated_data.get('is_display_image'):
                # Set all other images as not display image
                SolutionMedia.objects.filter(solution=solar_solution, is_display_image=True).update(
                    is_display_image=False)

            # Create a SolutionMedia instance
            serializer.save(solution=solar_solution)  # Save with the related solution
            return Response({'status': 'media file uploaded'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(methods=['put', 'patch', 'delete'], request_body=UpdateMediaSerializer,
                         responses={
                             200: openapi.Response(description='Media file updated'),
                             400: openapi.Response(description='Invalid request'),
                             404: openapi.Response(description='Media file not found')
                         })
    @action(detail=True, methods=['put', 'patch', 'delete'], parser_classes=[MultiPartParser, FormParser])
    def update_media(self, request, pk=None):
        solar_solution = self.get_object()  # Get the specific SolarSolution instance

        if not (solar_solution.seller == request.user.userprofile or
                request.user.userprofile.role == UserProfile.Role.ADMIN):
            raise ValidationError("You are not allowed to update media for this solution.")

        serializer = UpdateMediaSerializer(data=request.data)
        if serializer.is_valid():
            image_id = serializer.validated_data['image_id']
            is_display_image = serializer.validated_data.get('is_display_image', False)

            try:
                media = SolutionMedia.objects.get(id=image_id, solution=solar_solution)
            except SolutionMedia.DoesNotExist:
                raise ValidationError("Media not found")

            if request.method == 'PUT' or request.method == 'PATCH':
                if is_display_image:
                    SolutionMedia.objects.filter(solution=solar_solution, is_display_image=True).exclude(
                        id=image_id).update(
                        is_display_image=False)
                    media.is_display_image = True
                else:
                    display_image_exists = SolutionMedia.objects.filter(is_display_image=True).exclude(id=image_id).exists()
                    if display_image_exists:
                        media.is_display_image = False
                    raise ValidationError(
                        "You can't modify this image. You need to set another image as display image first.")

                media.save()  # Save the updated media
                return Response({'status': 'media file updated'}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                media.delete()
                return Response({'status': 'media file deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    @swagger_auto_schema(
        operation_description="Simplified Admin Analytics",
        manual_parameters=[
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="Filter analytics by city (e.g., Islamabad, Karachi, Lahore)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: AdminAnalyticsSerializer()}
    )
    def admin_analytics(self, request):
        city = request.query_params.get('city')

        seller_filter = Q(role='seller')
        solution_filter = Q()
        buyer_filter = Q()
        if city:
            seller_filter &= Q(company__city__exact=city)
            solution_filter &= Q(seller__company__city__exact=city)
            buyer_filter &= Q(solar_solution__seller__company__city__exact=city)

        # Seller counts
        total_sellers = UserProfile.objects.filter(seller_filter).count()
        sellers_by_city = (
            UserProfile.objects.filter(seller_filter)
            .values('company__city')
            .annotate(city_sellers=Count('id'))
        )

        # Solar Solution counts
        total_solutions = SolarSolution.objects.filter(solution_filter).count()
        approved_solutions = SolarSolution.objects.filter(solution_filter, approval__admin_verified=True).count()
        unapproved_solutions = SolarSolution.objects.filter(solution_filter, approval__admin_verified=False).count()

        # Buyer counts
        total_buyers = BuyerInteraction.objects.filter(buyer_filter).count()
        buyers_by_city = (
            BuyerInteraction.objects.filter(buyer_filter)
            .values(company__city=F('solar_solution__seller__company__city'))
            .annotate(city_buyers=Count('id'))
        )

        # Prepare response data
        response_data = {
            "sellers": {
                "total": total_sellers,
                "seller_by_city_count": sellers_by_city
            },
            "solar_solutions": {
                "total": total_solutions,
                "approved": approved_solutions,
                "unapproved": unapproved_solutions,
            },
            "buyers": {
                "total": total_buyers,
                "buyer_by_city_count": buyers_by_city
            }
        }

        # Serialize and return response
        serializer = AdminAnalyticsSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrSeller])
    @swagger_auto_schema(
        operation_description="Seller Analytics",
        responses={200: SellerReportSerializer()}
    )
    def seller_analytics(self, request, pk=None):
        seller = request.user
        seller_profile = seller.userprofile
        solar_solutions = (SolarSolution.objects.select_related('seller', 'seller__user',
                                                               'seller__company')
                          .prefetch_related('interactions', 'mediafiles', 'components').filter(seller=seller_profile))

        seller_data = {
            'seller_id': seller.id,
            'seller_name': seller.full_name,
            'products': solar_solutions
        }
        # Use the SellerReportSerializer to serialize the seller data
        serializer = SellerReportSerializer(seller_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = SolutionComponent.objects.all()
    serializer_class = SolutionComponentSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['component_type', 'subtype']
    search_fields = ['component_type', 'subtype']
    ordering_fields = ['component_type']
    ordering = ['component_type']

    def get_queryset(self):
        return SolutionComponent.objects.all().order_by('component_type')

    def perform_create(self, serializer):
        serializer.save()


class TagAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        return Tag.objects.all().order_by('name')

    def perform_create(self, serializer):
        serializer.save()