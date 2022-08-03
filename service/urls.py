from django.urls import path, include

from rest_framework import routers

from service.views import (
    RestaurantViewSet,
    RestaurantCurrentMenuRetrieveView,
    MenuViewSet,
    RestaurantCurrentMenuUploadView,
    DishViewSet,
    RestaurantCurrentMenuVoteView, RestaurantCurrentDayResultView,
)

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)
router.register("dishes", DishViewSet)

urlpatterns = [

    path(
        "restaurants/<int:pk>/current_menu/",
        RestaurantCurrentMenuRetrieveView.as_view(),
        name="get-current-menu"
    ),
    path(
        "restaurants/<int:pk>/current_menu/set/",
        RestaurantCurrentMenuUploadView.as_view(),
        name="set-current-menu"
    ),
    path(
        "restaurants/<int:pk>/current_menu/vote/",
        RestaurantCurrentMenuVoteView.as_view(),
        name="vote-current-menu"
    ),
    path(
        "restaurants/<int:pk>/current_day_result",
        RestaurantCurrentDayResultView.as_view(),
        name="current-day-result"
    ),
    path("", include(router.urls)),
]


app_name = "service"
