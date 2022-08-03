import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from service.models import Dish, Restaurant, Menu, RestaurantMenu

MENU_URL = reverse("service:menu-list")


class UnauthenticatedMenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(MENU_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user12",
            "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_create_menu(self):
        dish_1 = Dish.objects.create(title="soup 1")
        dish_2 = Dish.objects.create(title="soup 2")
        payload = {
            "dishes": [dish_1.id, dish_2.id],
        }

        response = self.client.post(MENU_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["dishes"], payload["dishes"])

    def test_upload_menu_for_restaurant(self):
        restaurant = Restaurant.objects.create(
            name="test restaurant name",
            address="test address"
        )
        dish = Dish.objects.create(title="soup 1")
        menu = Menu.objects.create()
        menu.dishes.add(dish)
        url = reverse("service:set-current-menu", args=[restaurant.id])
        payload = {
            "date": datetime.datetime.now().date(),
            "menu": menu.id
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_current_restaurant_menu(self):
        restaurant = Restaurant.objects.create(
            name="test restaurant name",
            address="test address"
        )
        dish = Dish.objects.create(title="soup 1")
        menu = Menu.objects.create()
        menu.dishes.add(dish)
        RestaurantMenu.objects.create(
            restaurant=restaurant,
            menu=menu,
            date=datetime.datetime.now().date(),
        )

        url = reverse("service:get-current-menu", args=[restaurant.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

