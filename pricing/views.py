from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import status

from accounts.permissions import IsAdmin
from .models import SubscriptionPlan, SubscriptionPass
from .serializers import SubscriptionPlanSerializer, SubscriptionPassSerializer


class GetOrCreateSubscriptionPlan(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(request_body=SubscriptionPlanSerializer, responses={
        200: openapi.Response(description="Subscription Plan created or retrieved successfully.",
                              schema=SubscriptionPlanSerializer)})
    def post(self, request, *args, **kwargs):
        serializer = SubscriptionPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Automatically handles validation errors

        # Use get_or_create to ensure idempotent plan creation
        subscription_plan, _ = SubscriptionPlan.objects.get_or_create(
            name=serializer.validated_data['name'],
            defaults=serializer.validated_data
        )
        serializer = SubscriptionPlanSerializer(subscription_plan)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionPassListDetail(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = SubscriptionPass.objects.all().select_related('plan', 'seller__user', 'seller__user__userprofile')

    serializer_class = SubscriptionPassSerializer

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

