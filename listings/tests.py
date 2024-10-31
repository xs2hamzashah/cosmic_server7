from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from accounts.tests import BaseTestCase
from .models import SolarSolution, Tag, SolutionComponent, Service, ComponentType, SolutionType


class SolarSolutionViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create some tags
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')

        # Create a SolarSolution instance
        self.solar_solution = SolarSolution.objects.create(
            size=5.00,
            price=10000,
            solution_type=SolutionType.HYBRID,
            seller=self.user
        )

        # Create SolutionComponent instances
        self.component1 = SolutionComponent.objects.create(
            component_type=ComponentType.PV_MODULE,
            brand='Brand A',
            capacity=3.00,
            quantity=2
        )
        self.component2 = SolutionComponent.objects.create(
            component_type=ComponentType.BATTERY,
            brand='Brand B',
            capacity=300.00,
            quantity=10
        )

        # Associate components with the solar solution
        self.solar_solution.components.add(self.component1, self.component2)

        self.url = reverse('solar-solution-detail', args=[self.solar_solution.id])


    def test_retrieve_solar_solution(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['size']), self.solar_solution.size)

    def test_create_solar_solution(self):
        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            'size': 12,
            'price': 60000,
            'solution_type': SolutionType.HYBRID,
        }

        response = self.client.post(reverse('solar-solution-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_solution = SolarSolution.objects.last()
        self.assertEqual(new_solution.size, 12)
        self.assertEqual(new_solution.price, 60000)
        self.assertEqual(new_solution.solution_type, SolutionType.HYBRID)

    def test_update_solar_solution_with_existing_components_and_tags(self):
        data = {
            'size': 15,
            'price': 70000,
            'solution_type': SolutionType.HYBRID,
            'tag_ids': [self.tag1.id, self.tag2.id],  # Update tags
            'component_ids': [self.component1.id, self.component2.id],  # Attach existing component
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.solar_solution.refresh_from_db()
        self.assertEqual(self.solar_solution.size, 15)
        self.assertEqual(self.solar_solution.price, 70000)
        self.assertEqual(self.solar_solution.solution_type, SolutionType.HYBRID)
        self.assertEqual(self.solar_solution.tags.count(), 2)
        self.assertEqual(self.solar_solution.components.count(), 2)

    def test_delete_solar_solution(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SolarSolution.objects.filter(id=self.solar_solution.id).exists())

    def test_update_with_invalid_component_id(self):
        data = {
            'component_ids': [99999],
        }
        response = self.client.patch(reverse('solar-solution-detail', args=[self.solar_solution.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message
        self.assertTrue(any('Invalid component IDs' in str(error) for error in response.data['component_ids']))


class ComponentListCreateTestCase(BaseTestCase):
    def setUp(self):
        self.authenticate_user(role='seller')

        self.valid_component_data = {
            'component_type': 'Battery',
            'brand': 'Brand A',
            'capacity': 100,
            'quantity': 2,
        }

    def test_list_components(self):
        SolutionComponent.objects.create(**self.valid_component_data)

        response = self.client.get(reverse('component-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_component(self):
        response = self.client.post(reverse('component-list'), self.valid_component_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        component = SolutionComponent.objects.get(id=response.data['id'])
        self.assertEqual(component.component_type, self.valid_component_data['component_type'])
        self.assertEqual(component.brand, self.valid_component_data['brand'])


class TagListCreateTestCase(BaseTestCase):
    def setUp(self):
        self.authenticate_user(role='seller')

        self.valid_tag_data = {
            'name': 'NewTag',
        }

    def test_list_tags(self):
        Tag.objects.create(**self.valid_tag_data)

        response = self.client.get(reverse('tag-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_tag(self):
        response = self.client.post(reverse('tag-list-create'), self.valid_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tag = Tag.objects.get(id=response.data['id'])
        self.assertEqual(tag.name, self.valid_tag_data['name'])