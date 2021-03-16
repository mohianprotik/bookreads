from django.http import JsonResponse
from django.shortcuts import render
from review_system.models import Book, Tag

# Create your views here.
def autocomplete(request):
    if 'term' in request.GET:
        qs1 = Book.objects.filter(title__icontains=request.GET.get('term'))
        qs1_data = []
        for i in qs1:
            qs1_data.append(i.title)
        qs2 = Book.objects.filter(author__icontains=request.GET.get('term'))
        qs2_data = []
        for i in qs2:
            qs2_data.append(i.author)
        # qs3 = Book.objects.filter(tags__istartswith=request.GET.get('term'))

        retrieved_list = qs1_data + qs2_data

        titles = list()
        for each in retrieved_list:
            titles.append(each)
        
        return JsonResponse(titles, safe=False)

    return render(request, 'search/home.html')

def search_by_name(request):
    if request.method == 'POST':
        term = request.POST.get('book')
        qs1 = Book.objects.filter(title__icontains=term)
        qs2 = Book.objects.filter(author__icontains=term)
        
        qs = qs1.union(qs2)
        book_list = []
        for each_book in qs:
            book_list.append(each_book.as_json())

        return JsonResponse(book_list, safe=False)