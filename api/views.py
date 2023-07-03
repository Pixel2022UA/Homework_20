import json
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from .models import Book, Author


class BookList(View):
    def get(self, request):
        books = Book.objects.all()

        title = request.GET.get("title")
        author = request.GET.get("author")
        genre = request.GET.get("genre")

        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__name__icontains=author)
        if genre:
            books = books.filter(genre__icontains=genre)

        data = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                "publication_date": book.publication_date,
            }
            for book in books
        ]
        return JsonResponse(data, safe=False, status=200)

    def post(self, request):
        data = json.loads(request.body)
        title = data.get("title")
        author_name = data.get("author")
        genre = data.get("genre")
        publication_date = data.get("publication_date")

        if not title or not author_name or not genre or not publication_date:
            return JsonResponse({"error": "Incomplete data"}, status=400)

        try:
            author = Author.objects.get(name=author_name)
        except Author.DoesNotExist:
            author = Author.objects.create(name=author_name)

        try:
            inv_date = datetime.strptime(publication_date, "%Y-%m-%d")
        except ValueError:
            return JsonResponse(
                {"error": "Invalid date format. Use YYYY-MM-DD format."}, status=400
            )

        book = Book.objects.create(
            title=title, author=author, genre=genre, publication_date=inv_date.date()
        )
        data = {
            "id": book.id,
            "title": book.title,
            "author": author.name,
            "genre": book.genre,
            "publication_date": book.publication_date,
        }
        return JsonResponse(data, status=201)


class Books(View):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        data = {
            "id": book.id,
            "title": book.title,
            "author": book.author.name,
            "genre": book.genre,
            "publication_date": book.publication_date,
        }
        return JsonResponse(data, safe=False, status=200)

    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        data = json.loads(request.body)
        title = data.get("title")
        author = data.get("author")
        genre = data.get("genre")
        publication_date = data.get("publication_date")

        if not title and not author and not genre and not publication_date:
            return JsonResponse({"error": "No data to update"}, status=400)

        if title:
            book.title = title
        if author:
            book.author.name = author
            book.author.save()
        if genre:
            book.genre = genre
        if publication_date:
            book.publication_date = publication_date

        book.save()

        data = {
            "id": book.id,
            "title": book.title,
            "author": book.author.name,
            "genre": book.genre,
            "publication_date": book.publication_date,
        }
        return JsonResponse(data, status=200)

    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)
        book.delete()
        return JsonResponse({"message": "Book was deleted"}, status=204)


class AuthorList(View):
    def get(self, request):
        authors = Author.objects.all()
        name = request.GET.get("name")
        if name:
            authors = authors.filter(name__icontains=name)

        data = [{"id": author.id, "name": author.name} for author in authors]
        return JsonResponse(data, safe=False, status=200)


class Authors(View):
    def get(self, request, id):
        try:
            author = Author.objects.get(id=id)
        except Author.DoesNotExist:
            return JsonResponse({"error": "Author not found"}, status=404)

        data = {"id": author.id, "name": author.name}
        return JsonResponse(data, safe=False, status=200)
