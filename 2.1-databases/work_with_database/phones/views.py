from django.shortcuts import render, redirect, get_object_or_404

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_fields = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }

    sort = request.GET.get('sort')
    sort_field = sort_fields.get(sort, 'id')
    phones = Phone.objects.all().order_by(sort_field)

    context = {
        'phones': phones,
    }
    return render(request, 'catalog.html', context)


def show_product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)

    context = {
        'phone': phone,
    }
    return render(request, 'product.html', context)
