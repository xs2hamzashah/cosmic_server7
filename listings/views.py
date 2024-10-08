import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import IsSeller, IsAdmin
from operations.models import Approval
from .models import SolarSolution, Tag, SolutionMedia, SolutionDetails, Service
from .serializers import SolarSolutionListSerializer, SolarSolutionCreateSerializer
from django.db.models import Prefetch


class SolarSolutionViewSet(viewsets.ModelViewSet):
    queryset = SolarSolution.objects.all()
    serializer_class = SolarSolutionListSerializer # default fallback
    permission_classes = [AllowAny]

    class SolarSolutionFilter(django_filters.FilterSet):
        size = django_filters.NumberFilter(field_name='size')
        price = django_filters.NumberFilter(field_name='price')
        city = django_filters.CharFilter(field_name='seller__userprofile__company__city', lookup_expr='icontains')

        class Meta:
            model = SolarSolution
            fields = ['size', 'price', 'city']

        def filter_by_city(self, queryset, name, value):
            # Replace this with your custom logic for city filtering
            # For example, if you want to filter by city name in a related model:
            return queryset.filter(seller__userprofile__city__icontains=value)

    filter_backends = [DjangoFilterBackend]
    filterset_class = SolarSolutionFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return SolarSolutionListSerializer
        elif self.action == 'create':
            return SolarSolutionCreateSerializer

    def get_queryset(self):
        if self.action == 'list':
            return SolarSolution.objects.all()
        else:
            # Prefetch related fields for other actions
            return SolarSolution.objects.prefetch_related(
                'tags',
                Prefetch('mediafiles', queryset=SolutionMedia.objects.filter(is_display_image=True)),
                'components',
                'services'
            ).select_related(
                'seller__userprofile__company'  # Select related to optimize the query for the city filter
            )

    def create(self, request, *args, **kwargs):
        data = request.data
        if not request.user.is_authenticated:
            return Response({'error': 'User must be authenticated'}, status=403)

        tags_data = data.pop('tags', [])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        media_data = data.pop('mediafiles', [])
        components_data = data.pop('components', [])
        services_data = data.pop('services', [])

        # Create the SolarSolution instance
        solar_solution = SolarSolution.objects.create(
            size=data['size'],
            price=data['price'],
            solution_type=data['solution_type'],
            completion_time_days=data['completion_time_days'],
            payment_schedule=data['payment_schedule'],
            seller=request.user
        )

        # Handle tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            solar_solution.tags.add(tag)

        # Handle mediafiles
        for media in media_data:
            SolutionMedia.objects.create(solution=solar_solution, **media)

        # Handle components (SolutionDetails)
        for component in components_data:
            SolutionDetails.objects.create(solar_solution=solar_solution, **component)

        # Handle services
        for service in services_data:
            Service.objects.create(solution=solar_solution, **service)

        # Create Approval entry for the newly created SolarSolution
        Approval.objects.create(solution=solar_solution)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Use the filter here
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)