from django.urls import path, include

from rest_framework import routers

from service.views import RestaurantViewSet


router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)

urlpatterns = [path("", include(router.urls))]


app_name = "service"
