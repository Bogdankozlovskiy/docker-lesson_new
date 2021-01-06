from django.core.management.base import BaseCommand
from manager.models import Book, TMPBook, LikeBookUser, Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()
        arr = [
            TMPBook(
                title=b.title,
                text=b.text,
                date=b.date,
                rate=b.rate,
                count_rated_users=b.count_rated_users,
                count_all_stars=b.count_all_stars,
                slug=b.slug
            )
            for b in books
        ]
        TMPBook.objects.bulk_create(arr)
        print("done")

        query = Book.objects.all().values("slug", "id")
        all_lbu = LikeBookUser.objects.all()
        for book in query:
            new_set = all_lbu.filter(book_id=book['id'])
            for lbu in new_set:
                lbu.tmp_book_id = book['slug']
            LikeBookUser.objects.bulk_update(new_set, ['tmp_book_id'])

        query = Book.objects.all().values("slug", "id")
        all_comments = Comment.objects.all()
        for book in query:
            comments = all_comments.filter(book_id=book['id'])
            for c in comments:
                c.tmp_book_id = book['slug']
            Comment.objects.bulk_update(comments, ['tmp_book_id'])

        books = Book.objects.all()
        tmp_books = TMPBook.objects.all()
        for book in books:
            tmp_book = tmp_books.get(slug=book.slug)
            for author in book.authors.all():
                tmp_book.authors.add(author)
            tmp_book.date = book.date
            tmp_book.save()


