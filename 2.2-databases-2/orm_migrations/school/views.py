from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    students = (
        Student.objects
        .order_by('group', 'name')
        .prefetch_related('teachers')
    )

    context = {
        'object_list': students,
    }
    return render(request, 'school/students_list.html', context)
