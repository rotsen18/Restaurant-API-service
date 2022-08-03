from datetime import datetime

from django.db.models import Count, Avg
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from service.models import Restaurant, Dish, Menu, RestaurantMenu, Vote
from service.tests.test_restaurant import RESTAURANT_URL


def detail_url(task_id: int):
    return reverse("service:restaurant-detail", args=[task_id])


class UnauthenticatedVoteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedVoteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user12",
            "test12345"
        )
        self.client.force_authenticate(self.user)

        self.restaurant = Restaurant.objects.create(
            name="test restaurant name",
            address="test address"
        )
        dish = Dish.objects.create(title="soup 1")
        menu = Menu.objects.create()
        menu.dishes.add(dish)
        self.restaurant_menu = RestaurantMenu.objects.create(
            restaurant=self.restaurant,
            menu=menu,
            date=datetime.now().date(),
        )

    def test_make_vote(self):
        url = reverse("service:vote-current-menu", args=[self.restaurant.id])
        payload = {"rate": 2}
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_summary_day_information(self):
        another_user = get_user_model().objects.create_user(
            "user13",
            "test12345"
        )
        Vote.objects.create(
            restaurant_menu=self.restaurant_menu,
            user=self.user,
            rate=3
        )
        Vote.objects.create(
            restaurant_menu=self.restaurant_menu,
            user=another_user,
            rate=1
        )

        url = reverse("service:current-day-result", args=[self.restaurant.id])
        response = self.client.get(url)

        rate_data = Vote.objects.aggregate(
            amount=Count("id"),
            average=Avg("rate")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["restaurant"], self.restaurant.name)
        self.assertEqual(response.data["rate_amount"], rate_data["amount"])
        self.assertEqual(response.data["average_rate"], rate_data["average"])
        self.assertEqual(
            response.data["menu"]["id"],
            self.restaurant_menu.menu.id
        )
