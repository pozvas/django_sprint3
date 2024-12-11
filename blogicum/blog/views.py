from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Post, Category


def index(request):
    posts = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(
        request,
        template_name='blog/index.html',
        context={'post_list': posts}
    )


def post_detail(request, post_id):
    try:
        post = Post.objects.select_related(
            'category',
            'location'
        ).get(pk=post_id)
    except ObjectDoesNotExist:
        raise Http404(f"Пост с id {post_id} не найден.")

    if (post.pub_date > timezone.now()
            or not post.is_published
            or not post.category.is_published):
        raise Http404(f"Пост с id {post_id} не найден.")

    return render(
        request,
        template_name='blog/detail.html',
        context={'post': post}
    )


def category_posts(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
        raise Http404(f"Категория с slug {category_slug} не найдена.")

    if not category.is_published:
        raise Http404(f"Категория с slug {category_slug} не найдена.")

    posts = Post.objects.select_related(
        'category',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__slug=category_slug
    ).order_by('-pub_date')

    return render(
        request,
        template_name='blog/category.html',
        context={'post_list': posts, 'category': category}
    )
