from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, PostView, Catagory, Tag, SavedPost
from marketing.models import Signup
from django.db.models import Count, Q
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def get_catagory_count():
    queryset = Post.objects.values(
        'catagories__title').annotate(Count('catagories__title'))
    return queryset


def get_tag_count():
    queryset = Post.objects.values(
        'tags__title').annotate(Count('tags__title'))
    return queryset


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)


def filterbycat(request, query):
    cats = Catagory.objects.all()
    cats = cats.filter(title__icontains=query)
    queryset = Post.objects.filter(catagories__in=cats)
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)


def filterbytag(request, query):
    tags = Tag.objects.all()
    tags = tags.filter(title__icontains=query)
    queryset = Post.objects.filter(tags__in=tags)
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)


def index(request):
    featured = Post.objects.filter(featured=True)
    letest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list': featured,
        'letest': letest
    }
    return render(request, 'index.html', context)


def blog(request):
    posts = Post.objects.all().order_by('id')
    catagory_count = get_catagory_count()
    tag_count = get_tag_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]

    paginator = Paginator(posts, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'catagory_count': catagory_count,
        'page_request_var': page_request_var,
        'tag_count': tag_count,
    }
    return render(request, 'blog.html', context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    tag_count = get_tag_count()
    data = False
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
        try:
            data = get_object_or_404(SavedPost, user=request.user, post=post)
        except:
            data = False
    print(data)
    catagory_count = get_catagory_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'slug': post.slug
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'catagory_count': catagory_count,
        'form': form,
        'tag_count': tag_count,
        'saved': data
    }
    return render(request, 'post.html', context)


@login_required
def save(request, id):
    post = get_object_or_404(Post, id=id)
    SavedPost.objects.get_or_create(user=request.user, post=post)
    return redirect(reverse('post_detail', kwargs={
        'id': id
    }))


@login_required
def savedlist(request):
    queryset = SavedPost.objects.filter(user=request.user)
    context = {
        'queryset': queryset
    }
    print(queryset)
    return render(request, 'savedpost.html', context)
