from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views import (
    Books,
    BookList,
    AuthorList,
    Authors,
    RegisterView,
    OrderView,
    OrderCallbackView,
)

urlpatterns = [
    path("books/", csrf_exempt(BookList.as_view()), name="book-list"),
    path("books/<int:id>/", csrf_exempt(Books.as_view()), name="book-id"),
    path("authors/", csrf_exempt(AuthorList.as_view()), name="author-list"),
    path("authors/<int:id>/", csrf_exempt(Authors.as_view()), name="author-id"),
    path("register/", RegisterView.as_view(), name="register"),
    path("orders/", OrderView.as_view(), name="orders"),
    path("callback/", OrderCallbackView.as_view(), name="callback"),
]
