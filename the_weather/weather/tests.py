"""
Unit tests for the weather app.

This module contains unit tests for the weather app, including tests
for adding cities, fetching weather data, and deleting cities.

Classes:
    CityModelTest: Unit tests for the City model.
    CityFormTest: Unit tests for the City form.
    WeatherViewTest: Unit tests for the index view.
    DeleteCityViewTest: Unit tests for the delete_city view.
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import City
from .forms import CityForm


class CityModelTest(TestCase):

    def setUp(self):
        self.city = City.objects.create(name='Las Vegas')

    def test_city_creation(self):
        self.assertEqual(self.city.name, 'Las Vegas')
        self.assertEqual(City.objects.count(), 1)

    def test_city_deletion(self):
        self.city.delete()
        self.assertEqual(City.objects.count(), 0)


class CityFormTest(TestCase):
    def test_city_form_valid(self):
        form = CityForm(data={'name': 'New York'})
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())


class WeatherViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(name='Las Vegas')
        self.url = reverse('index')

    def test_index_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_index_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('weather_data', response.context)

    def test_city_addition(self):
        response = self.client.post(self.url, {'name': 'New York'})
        self.assertEqual(City.objects.count(), 2)


class DeleteCityViewTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Las Vegas')
        self.client = Client()

    def test_delete_city(self):
        response = self.client.post(reverse('delete_city', args=['Las Vegas']))
        self.assertEqual(City.objects.count(), 0)
        self.assertRedirects(response, reverse('index'))
