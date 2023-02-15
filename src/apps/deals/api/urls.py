from django.urls import path

from src.apps.deals.api.views import DealListCreateView


urlpatterns = [
    path("", DealListCreateView.as_view(), name="deal-list"),
]
