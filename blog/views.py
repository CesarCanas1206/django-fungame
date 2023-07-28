from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .filters import PostFilter

# Create your views here.


def archive(request):
    title = "VirtGold Blog"
    description = "Virtgold is one of the best websites to Buy ingame virtual gold. With multiple payment options, you can either buy or sell osrs or rs3 gold."
    tags = ["virtgold", "virt gold", "blog", "buy ingame currencies", "sell currency"]
    ogtype = "object"
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs
    page = request.GET.get("page")
    paginator = Paginator(posts, 12)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "myFilter": myFilter,
        "title": title,
        "description": description,
        "tags": tags,
        "ogtype": ogtype,
    }
    return render(request, "blog/posts_archive.html", context=context)


def post(request, slug):
    ogtype = "article"
    post = Post.objects.get(slug=slug)
    context = {"post": post, "ogtype": ogtype}
    return render(request, "blog/single_post.html", context)
