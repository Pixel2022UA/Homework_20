from unittest import TestCase

import requests


class APITestCase(TestCase):
    def setUp(self):
        self.base_url = "https://mylibrary-e460551407b2.herokuapp.com/api/"

    def get_last_book_id(self):
        response = requests.get(f"{self.base_url}books/")
        data = response.json()
        last_book_id = data[-1]["id"]
        return last_book_id

    def test_get_books(self):
        response = requests.get(f"{self.base_url}books/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

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

    def test_create_book(self):
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "publication_date": "2023-05-16",
        }
        response = requests.post(f"{self.base_url}books/", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["genre"], "Test Genre")
        self.assertEqual(data["publication_date"], "2023-05-16")
        self.assertIsInstance(data, dict)

    def test_update_book(self):
        last_book = self.get_last_book_id()
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "genre": "Updated Genre",
            "publication_date": "2023-05-17",
        }
        response = requests.put(f"{self.base_url}books/{last_book}/", json=data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Book")
        self.assertEqual(data["author"], "Updated Author")
        self.assertEqual(data["genre"], "Updated Genre")
        self.assertEqual(data["publication_date"], "2023-05-17")
        self.assertIsInstance(data, dict)

    def test_delete_book(self):
        last_book = self.get_last_book_id()
        response = requests.delete(f"{self.base_url}books/{last_book}/")
        self.assertEqual(response.status_code, 204)

    def test_get_authors(self):
        response = requests.get(f"{self.base_url}authors/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_author(self):
        response = requests.get(f"{self.base_url}authors/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertIsInstance(data, dict)
