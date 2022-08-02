from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


RESTAURANT_URL = reverse("service:restaurant-list")


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test_User",
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
