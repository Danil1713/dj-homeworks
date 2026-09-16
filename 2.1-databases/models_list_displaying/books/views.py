from datetime import date

from django.http import Http404
from django.shortcuts import render

from books.models import Book


def books_view(request, pub_date=None):
    books = Book.objects.all().order_by('pub_date', 'id')
    previous_date = None
    next_date = None

    if pub_date is not None:
        try:
            selected_date = date.fromisoformat(pub_date)
        except ValueError:
            raise Http404('Некорректная дата')

        books = books.filter(pub_date=selected_date)

        previous_date = (
            Book.objects
            .filter(pub_date__lt=selected_date)
            .order_by('-pub_date')
            .values_list('pub_date', flat=True)
            .first()
        )

        next_date = (
            Book.objects
            .filter(pub_date__gt=selected_date)
            .order_by('pub_date')
            .values_list('pub_date', flat=True)
            .first()
        )

    context = {
        'books': books,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_list.html', context)
