from rest_framework import serializers
from .models import Book, Author, Order


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.name")

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "publication_date",
            "quantity",
            "price",
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class OrderContentSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    order = OrderContentSerializer(many=True, allow_empty=False)


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_price", "create", "invoice_id", "books", "status"]


class MonoCallbackSerializer(serializers.Serializer):
    invoiceId = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.IntegerField()
    ccy = serializers.IntegerField()
    reference = serializers.CharField()
