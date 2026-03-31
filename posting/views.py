from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
# from .models import Profile
from .forms import PostForm, LoginForm, RegisterForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .utils import login_required
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import PasswordResetCode
from .forms import ForgotPasswordForm
from django.contrib.auth.hashers import make_password
from .forms import ResetPasswordForm
from django.utils import timezone
from datetime import timedelta



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

@permission_required('posting.add_post', raise_exception=True)
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'create.html', {'form': form})

@permission_required('posting.change_post', raise_exception=True)
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'update.html', {'form': form})


@permission_required('posting.delete_post', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete.html', {'post': post})


# def edit_profile(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # profil page url name
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, 'edit_profile.html', {'form': form})
#
#
# def profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'profile.html', {'profile': profile})


def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            form.add_error("username", "Bunday user yo‘q")
            return render(request, 'forgot_password.html', {'form': form})

        code = PasswordResetCode.generate_code()

        PasswordResetCode.objects.create(
            user=user,
            code=code,
            expired_at=timezone.now() + timedelta(minutes=2)
        )

        # EMAIL YUBORISH
        send_mail(
            "Yangi parol",
            f"Sizning kodingiz: {code}\nMuddati: 2 daqiqa!",
            None,
            [settings.EMAIL_HOST_USER]
        )

        request.session['reset_user'] = user.pk

        return redirect('reset')

    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request):
    form = ResetPasswordForm(request.POST or None)

    user_id = request.session.get('reset_user')

    if not user_id:
        return redirect('forgot')

    if form.is_valid():
        code = form.cleaned_data['code']
        new_password = form.cleaned_data['new_password']

        try:
            record = PasswordResetCode.objects.filter(
                user_id=user_id,
                code=code
            ).latest('created_at')
        except PasswordResetCode.DoesNotExist:
            form.add_error("code", "Noto‘g‘ri kod!")
            return render(request, 'reset_password.html', {'form': form})

        # PAROLNI YANGILASH
        user = record.user
        user.password = make_password(new_password)
        user.save()

        # Kodni o‘chiramiz
        record.delete()

        return redirect('login')

    return render(request, 'reset_password.html', {'form': form})


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


