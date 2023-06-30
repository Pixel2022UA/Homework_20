import json
from django.test import TestCase
from django.urls import reverse
from .models import Book, Author


class BookAPITest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Oliver')
        self.book = Book.objects.create(title='First book', author=self.author, genre='Mystic', publication_date='2023-01-01')

    def test_get_all_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_book_by_id(self):
        response = self.client.get(reverse('book-id', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'First book')

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'genre': 'Mystery',
            'publication_date': '2023-01-01'
        }
        response = self.client.post(reverse('book-list'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {
            'title': 'Updated Book',
            'genre': 'Thriller'
        }
        response = self.client.put(reverse('book-id', args=[self.book.id]), data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Book')
        self.assertEqual(response.json()['genre'], 'Thriller')
    #
    def test_delete_book(self):
        response = self.client.delete(reverse('book-id', args=[self.book.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)


class AuthorAPITest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='Eshton')
        self.author2 = Author.objects.create(name='Jane')
#
    def test_get_all_authors(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_author_by_id(self):
        response = self.client.get(reverse('author-id', args=[self.author1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Eshton')
