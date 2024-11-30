from django.urls import path
from .views import GetOrCreateSubscriptionPlan, SubscriptionPassListDetail

urlpatterns = [
    path('subscription-plan/', GetOrCreateSubscriptionPlan.as_view(), name='get_or_create_subscription_plan'),
    path('subscription-passes/', SubscriptionPassListDetail.as_view(), name='subscription_pass_list'),
    path('subscription-passes/<int:id>/', SubscriptionPassListDetail.as_view(), name='subscription_pass_detail')
]
