from django.http import HttpResponseRedirect
from blog.forms import CommentForm

from django.shortcuts import render

from blog.models import Post, Comment

# Create your views here.

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts":posts,
    }
    return render(request, "blog/index.html",context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains = category).order_by("-created_on")

    context = {
        "category": category,
        "posts": posts,
    }
    return render(request,"blog/category.html",context)

def blog_details(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = Comment(

                author=form.cleaned_data["author"],

                body=form.cleaned_data["body"],

                post=post,

            )

            comment.save()

            return HttpResponseRedirect(request.path_info)
    Comments = Comment.objects.filter(post=post)
    context = {
        "post":post,
        "comments": Comments,
        "form": CommentForm(),
    }
    return render(request, "blog/details.html",context)