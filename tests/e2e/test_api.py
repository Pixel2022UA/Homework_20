from unittest import TestCase

import pytest
import requests
from faker import Faker
from rest_framework import status

fake = Faker()


class APITestCase(TestCase):
    def setUp(self):
        self.base_url = "https://mylibrary-e460551407b2.herokuapp.com/api/"

    @pytest.mark.run(order=1)
    def test_user_registration(self):
        username = fake.user_name()
        password = fake.password()
        data = {
            "username": username,
            "password": password,
        }
        response = requests.post(f"{self.base_url}register/", json=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("token", response_data)
        self.assertTrue(response_data["token"])
        self.__class__.token = response_data["token"]

    @pytest.mark.run(order=2)
    def test_create_book(self):
        headers = {"Authorization": f"Token {self.token}"}
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "publication_date": "2023-05-16",
        }
        response = requests.post(f"{self.base_url}books/", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["genre"], "Test Genre")
        self.assertEqual(data["publication_date"], "2023-05-16")
        self.assertIsInstance(data, dict)

    def get_last_book_id(self):
        response = requests.get(f"{self.base_url}books/")
        data = response.json()
        last_book_id = data[-1]["id"]
        return last_book_id

    @pytest.mark.run(order=3)
    def test_get_books(self):
        response = requests.get(f"{self.base_url}books/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    @pytest.mark.run(order=4)
    def test_get_book(self):
        last_book = self.get_last_book_id()
        response = requests.get(f"{self.base_url}books/{last_book}/")
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, dict)
            self.assertTrue("title" in data)
            self.assertTrue("author" in data)
            self.assertTrue("genre" in data)
            self.assertTrue("publication_date" in data)
        elif response.status_code == 404:
            pass

    @pytest.mark.run(order=5)
    def test_update_book(self):
        headers = {"Authorization": f"Token {self.token}"}
        last_book = self.get_last_book_id()
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "genre": "Updated Genre",
            "publication_date": "2023-05-17",
        }
        response = requests.put(
            f"{self.base_url}books/{last_book}/", headers=headers, json=data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Book")
        self.assertEqual(data["author"], "Updated Author")
        self.assertEqual(data["genre"], "Updated Genre")
        self.assertEqual(data["publication_date"], "2023-05-17")
        self.assertIsInstance(data, dict)

    @pytest.mark.run(order=6)
    def test_delete_book(self):
        headers = {"Authorization": f"Token {self.token}"}
        last_book = self.get_last_book_id()
        response = requests.delete(
            f"{self.base_url}books/{last_book}/", headers=headers
        )
        self.assertEqual(response.status_code, 204)

    @pytest.mark.run(order=7)
    def test_get_authors(self):
        response = requests.get(f"{self.base_url}authors/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    @pytest.mark.run(order=8)
    def test_get_author(self):
        response = requests.get(f"{self.base_url}authors/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertIsInstance(data, dict)
