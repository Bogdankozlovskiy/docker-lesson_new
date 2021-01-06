from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Prefetch, OuterRef, Exists
from django.shortcuts import render, redirect
from django.views import View
from manager.forms import BookForm, CustomAuthenticationForm, CustomUserCreationForm
from manager.models import Book, Comment, LikeCommentUser
from manager.models import LikeBookUser as RateBookUser
from django.core.paginator import Paginator
from django.http import HttpResponse
from manager.tasks import create_aggregate


class MyPage(View):
    def get(self, request):
        # context = {}
        # books = Book.objects.prefetch_related("authors")
        # if request.user.is_authenticated:
        #     is_owner = Exists(User.objects.filter(books=OuterRef('pk'), id=request.user.id))
        #     books = books.annotate(is_owner=is_owner)
        # paginator = Paginator(books.order_by("-rate", "date"), 2)
        # context['books'] = paginator.get_page(request.GET.get("page", 1))
        # context['range'] = range(1, 6)
        # context['form'] = BookForm()

        # return render(request, "index.html", context)
        create_aggregate.delay(request.user.id)
        return HttpResponse("done")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {'form': CustomAuthenticationForm()})

    def post(self, request):
        user = CustomAuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
            return redirect("the-main-page")
        messages.error(request, user.error_messages)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        messages.error(request, form.error_messages)
        return redirect("register")


def logout_user(request):
    logout(request)
    return redirect("the-main-page")


class AddLike2Comment(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeCommentUser.objects.create(user=request.user, comment_id=id)
        return redirect("the-main-page")


class AddRate2Book(View):
    def get(self, request, slug, rate, location=None):
        if request.user.is_authenticated:
            RateBookUser.objects.create(user=request.user, book_id=slug, rate=rate)
        if location is None:
            return redirect("the-main-page")
        return redirect("book-detail", slug=slug)


class BookDetail(View):
    def get(self, request, slug):
        comment_query = Comment.objects.annotate(count_like=Count("users_like")).select_related("author")
        comments = Prefetch("comments", comment_query)
        book = Book.objects.prefetch_related("authors", comments).get(slug=slug)
        return render(request, "book_detail.html", {"book": book, "rate": 2})


class AddBook(View):
    def post(self, request):
        if request.user.is_authenticated:
            bf = BookForm(data=request.POST)
            book = bf.save(commit=True)
            book.authors.add(request.user)
            book.save()
        return redirect("the-main-page")


def book_delete(request, slug):
    if request.user.is_authenticated:
        book = Book.objects.get(slug=slug)
        if request.user in book.authors.all():
            book.delete()
    return redirect("the-main-page")


class UpdateBook(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                form = BookForm(instance=book)
                return render(request, "update_book.html", {"form": form, "slug": book.slug})
        return redirect("the-main-page")

    def post(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                bf = BookForm(instance=book, data=request.POST)
                if bf.is_valid():
                    bf.save(commit=True)
        return redirect("the-main-page")
