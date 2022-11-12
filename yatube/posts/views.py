from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post, User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .utils import get_paginator

POST_QTY = 10


def index(request):
    post_list = Post.objects.all()
    paginat = get_paginator(post_list, request)
    context = {
        'page_obj': paginat['page_obj'],
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginat = get_paginator(posts, request)
    context = {
        'group': group,
        'page_obj': paginat['page_obj'],
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = author.posts.count()
    paginat = get_paginator(posts, request)
    context = {
        'author': author,
        'posts': posts,
        'count': count,
        'page_obj': paginat['page_obj'],
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    count = author.posts.count()
    context = {
        'post': post,
        'author': author,
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', request.user)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'is_edit': True,
        }
    return render(request, 'posts/create_post.html', context)
