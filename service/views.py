import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.helpers import collect_result_data
from service.models import Restaurant, RestaurantMenu, Menu, Dish
from service.serializers import (
    RestaurantSerializer,
    RestaurantMenuSerializer,
    MenuSerializer,
    MenuListSerializer,
    MenuDetailSerializer,
    DishSerializer,
    VoteSerializer,
    RestaurantCurrentDayResultSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantCurrentMenuRetrieveView(APIView):
    queryset = RestaurantMenu.objects.filter(date=datetime.datetime.now().date())

    def get(self, request, pk):
        restaurant_menu_queryset = self.queryset.filter(restaurant__id=pk)

        if restaurant_menu_queryset.exists():
            menu = restaurant_menu_queryset.first().menu
            serializer = MenuDetailSerializer(menu)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RestaurantCurrentMenuVoteView(APIView):
    """Make vote"""
    queryset = RestaurantMenu.objects.filter(date=datetime.datetime.now().date())
    serializer_class = VoteSerializer

    def post(self, request, pk):
        restaurant_menu_queryset = self.queryset.filter(restaurant__id=pk)
        serializer = VoteSerializer(data=request.data)
        if restaurant_menu_queryset.exists():
            restaurant_menu = restaurant_menu_queryset.first()

            if serializer.is_valid():
                serializer.save(restaurant_menu=restaurant_menu, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantCurrentMenuUploadView(APIView):
    """Set menu for restaurant"""
    queryset = RestaurantMenu.objects.filter(date=datetime.datetime.now().date())
    serializer_class = RestaurantMenuSerializer

    def post(self, request, pk):
        serializer = RestaurantMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer
        elif self.action == "retrieve":
            return MenuDetailSerializer

        return MenuSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RestaurantCurrentDayResultView(APIView):
    queryset = RestaurantMenu.objects.filter(date=datetime.datetime.now().date())

    def get(self, request, pk):
        restaurant_menu_queryset = self.queryset.filter(restaurant__id=pk)
        if restaurant_menu_queryset.exists():
            restaurant_menu = restaurant_menu_queryset.first()
            payload = collect_result_data(restaurant_menu)
            serializer = RestaurantCurrentDayResultSerializer(payload)

            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
