from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from service.models import Restaurant

RESTAURANT_URL = reverse("service:restaurant-list")


def detail_url(task_id: int):
    return reverse("service:restaurant-detail", args=[task_id])


class UnauthenticatedRestaurantApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRestaurantApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user12",
            "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_create_restaurant(self):
        payload = {
            "name": "test restaurant name",
            "address": "test address"
        }

        response = self.client.post(RESTAURANT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["address"], payload["address"])

    def test_detail_restaurant(self):
        payload = {
            "name": "test restaurant name",
            "address": "test address"
        }
        restaurant = Restaurant.objects.create(**payload)
        url = detail_url(restaurant.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["address"], payload["address"])
