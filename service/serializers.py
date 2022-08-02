from rest_framework import serializers

from service.models import (
    Restaurant,
    Menu, RestaurantMenu, Dish
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address")
        read_only_fields = ("id", )


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"
        read_only_fields = ("id", )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuDetailSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"


class MenuListSerializer(serializers.ModelSerializer):
    dishes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Menu
        fields = "__all__"


class RestaurantMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ("date", "menu")

