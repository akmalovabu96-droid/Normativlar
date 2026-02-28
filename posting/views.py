from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, LoginForm, RegisterForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .utils import login_required

def post_list(request):

    query = request.GET.get('q')

    posts = Post.objects.all().order_by('-created_at')

    # Searching
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    # Pagination
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {
        'page_obj': page_obj,
        'query': query
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'create.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'update.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete.html', {'post': post})


def register_view(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        form.save()

        return redirect("login")

    return render(request, "register.html", {
        "form": form
    })

def login_view(request):

    form = LoginForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("post_list")

        else:

            form.add_error(
                None,
                "Username yoki password noto‘g‘ri"
            )


    return render(request, "login.html", {
        "form": form
    })

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


