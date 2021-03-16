from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import *
from django.core import serializers

from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def create_review(request):
    if request.method == 'POST':
        obtained_contents = request.POST.get('contents')
        obtained_user = request.user
        obtained_book_serial_no = request.POST.get('book_serial_no')
        obtained_book = Book.objects.get(serial_no=obtained_book_serial_no)
        contents = Review(contents=obtained_contents, 
                            user=obtained_user,
                            book=obtained_book
                            )
        contents.save()
        messages.success(request, "Review was posted successfully!")

def book_details(request, book_id):
    book = Book.objects.get(serial_no=book_id)
    # print(book)
    review_list = Review.objects.filter(book=book)
    review_tree = []
    for each_review in review_list:
        if not each_review.parent:
            comments = Review.objects.filter(parent=each_review)
            comment_list = []
            for each_comment in comments:
                comment_list.append(each_comment.as_json())
            review_tree.append({
                'review': each_review.as_json(),
                'comments': comment_list
            })
    print(review_tree)
    return JsonResponse(review_tree, safe=False)


    