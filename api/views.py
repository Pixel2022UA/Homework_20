import os
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.urls import reverse
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Author, Order
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    OrderSerializer,
    OrderModelSerializer,
    MonoCallbackSerializer,
)
from .monobank import create_order, verify_signature

load_dotenv()
mono_token = os.getenv("MONOBANK_API_KEY")


class OrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order = OrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        webhook_url = request.build_absolute_uri(reverse("callback"))
        data = create_order(order.validated_data["order"], webhook_url)
        return Response(data)

    def get(self, request):
        orders = Order.objects.all().order_by("id")
        serializer = OrderModelSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mono_token = os.getenv("MONOBANK_API_KEY")
        if not verify_signature(
            mono_token, request.headers.get("X-Sign"), request.body
        ):
            return Response({"status": "signature does not match"})
        serializer = MonoCallbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = Order.objects.get(id=serializer.validated_data["reference"])
        except Order.DoesNotExist:
            return Response({"status": "order not found"}, status=404)
        if order.invoice_id != serializer.validated_data["invoice_id"]:
            return Response({"status": "Invoice ID does not match"}, status=400)
        order.status = serializer.validated_data["status"]
        order.save()
        return Response({"status": "ok"})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            try:
                user = User.objects.create_user(username=username, password=password)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            except IntegrityError:
                raise serializers.ValidationError("Username already exists.")
        else:
            return Response(
                {"error": "Please enter valid username and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BookList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @method_decorator(cache_page(60))
    def get(self, request):
        books = Book.objects.all().order_by("id")
        title = request.GET.get("title")
        author = request.GET.get("author")
        genre = request.GET.get("genre")
        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__name__icontains=author)
        if genre:
            books = books.filter(genre__icontains=genre)
        serializer = BookSerializer(books, many=True)
        # time.sleep(4)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            author_name = serializer.validated_data["author"]
            try:
                author = Author.objects.get(name=author_name["name"])
            except Author.DoesNotExist:
                author = Author.objects.create(name=author_name["name"])
            book = serializer.save(author=author)
            response_data = {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                "publication_date": book.publication_date,
                "quantity": book.quantity,
                "price": book.price,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Books(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404

    # @method_decorator(cache_page(60))
    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            author_name = serializer.validated_data.get("author")
            if author_name:
                try:
                    author = Author.objects.get(name=author_name["name"])
                except Author.DoesNotExist:
                    author = Author.objects.create(name=author_name["name"])
                serializer.validated_data["author"] = author
            book = serializer.save()
            response_data = {
                "id": book.id,
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre,
                "publication_date": book.publication_date,
                "quantity": book.quantity,
                "price": book.price,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(
            {"message": "Book was deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class AuthorList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @method_decorator(cache_page(60))
    def get(self, request):
        name = request.GET.get("name")
        authors = Author.objects.all()
        if name:
            authors = authors.filter(name__icontains=name)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Authors(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Author.objects.get(id=id)
        except Author.DoesNotExist:
            raise Http404

    # @method_decorator(cache_page(60))
    def get(self, request, id):
        author = self.get_object(id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)
