from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from manager.models import Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.annotate(
            tmp_all_stars=Sum("liked_user_table__rate"),
            tmp_rated_users=Count("liked_user_table")
        )
        for b in books:
            b.count_rated_users = b.tmp_rated_users
            b.count_all_stars = b.tmp_all_stars
            b.rate = b.tmp_all_stars / b.tmp_rated_users
        Book.objects.bulk_update(
            books,
            ["count_rated_users", "count_all_stars", "rate"],
            batch_size=4
        )

# arr = [1,2,3,4,5,...]
# mas = ["text1", "text2",...]
#
# arr_books = []
# for tit, con in zip(arr, mas):
#     b = Book(title=tit, text=con)
#     arr_books.append(b)

# Book.objects.bulk_create(arr_books)