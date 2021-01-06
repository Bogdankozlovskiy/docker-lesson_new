from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


class Book(models.Model):
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    title = models.CharField(
        max_length=50,
        verbose_name="название",
        help_text="ну это типо погоняло книги",
        db_index=True
    )
    date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    authors = models.ManyToManyField(User, related_name="books")
    rate = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    count_rated_users = models.PositiveIntegerField(default=0)
    count_all_stars = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(User, through="manager.LikeBookUser", related_name="liked_books")
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return f"{self.title}-{self.slug}"

    def save(self, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.title)
        try:
            super().save(**kwargs)
        except:
            self.slug += str(self.date)
            super().save(**kwargs)


class LikeBookUser(models.Model):
    class Meta:
        unique_together = ("user", "book")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_book_table")
    book: Book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="liked_user_table", null=True)
    rate = models.PositiveIntegerField(default=5)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            lbu = LikeBookUser.objects.get(user=self.user, book=self.book)
            self.book.count_all_stars -= lbu.rate
            lbu.rate = self.rate
            lbu.save()
        else:
            self.book.count_rated_users += 1
        self.book.count_all_stars += self.rate
        self.book.rate = self.book.count_all_stars / self.book.count_rated_users
        self.book.save()


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    users_like = models.ManyToManyField(
        User,
        through="manager.LikeCommentUser",
        related_name="liked_comment"
    )


class LikeCommentUser(models.Model):
    class Meta:
        unique_together = ("user", "comment")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comment_table")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeCommentUser.objects.get(user=self.user, comment=self.comment).delete()

# CRUD
# create + ;
# read   + ;
# update + ;
# delete + ;

class TableAggregate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_aggregate')
    result = models.PositiveIntegerField(default=0)