from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import ContactForm, RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, NewPost
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


#from django.contrib.auth.decorators import login_required
def Index(request):
    post = Datas.objects.filter(is_published=True).order_by('created_at')
    title = 'Blog'

    paginator = Paginator(post, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'post': post, 'title': title, 'page_obj': page_obj})


def Details(request, slug):
    if request.user and not request.user.has_perm('blog.view_datas'):
        messages.error(request, 'you have no permissions to view the post')
        return redirect('/')
    post = Datas.objects.get(slug=slug)
    related_posts = Datas.objects.filter(categories=post.categories).exclude(pk=post.id)
    return render(request, 'details.html', {'post': post, 'related_posts': related_posts})


def Contact(request):
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger('TESTING')
        if forms.is_valid():
            logger.debug(forms.cleaned_data['name'], forms.cleaned_data['email'], forms.cleaned_data['message'])
            messages.success(request, 'message has been sent')
        else:
            logger.debug('form submission failure')
        return render(request, 'contacts.html', {'forms': forms, 'name': name, 'email': email, 'message': message})
    return render(request, 'contacts.html')


def About(request):
    desc = AboutUs.objects.first()
    if desc is None or not desc.content:
        desc = 'Default content goes Here...'
    else:
        desc = desc.content
    return render(request, 'about.html', {'desc': desc})


def Register(request):
    forms = RegisterForm()
    if request.method == 'POST':
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data['password'])
            user.save()
            readers_group, created = Group.objects.get_or_create(name='Readers')
            user.groups.add(readers_group)
            messages.success(request, 'registration success Log in Now')
            return redirect('login')
    return render(request, 'register.html', {'forms': forms})


def login(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'login successful')
                return redirect('/dashboard')
    return render(request, 'login.html', {'forms': forms})


# @login_required
def dashboard(request):
    all_posts = Datas.objects.filter(user=request.user)
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {'page_obj': page_obj})


def logout(request):
    auth_logout(request)
    return redirect('/')


def forgot_password(request):
    forms = ForgotPasswordForm()
    if request.method == 'POST':
        forms = ForgotPasswordForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = 'email sent request'
            message = render_to_string('reset_password_view.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@gmail.com', [email])
            messages.success(request, 'Email sent successfully')

    return render(request, 'forgot_password.html', {'forms': forms})


def reset_password(request, uidb64, token):
    forms = ResetPasswordForm()
    if request.method == 'POST':
        forms = ResetPasswordForm(request.POST)
        if forms.is_valid():
            new_password = forms.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError):
                user = None

            if user is not None and default_token_generator.check_token(user, token):

                user.set_password(new_password)
                user.save()
                messages.success(request, 'password reset successfully')
                return redirect('login')

            else:
                messages.error(request, 'The password reset link is invalid or expired')

    return render(request, 'reset_password.html', {'forms': forms})

@login_required
@permission_required('blog.add_datas', raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    forms = NewPost()
    if request.method == 'POST':
        forms = NewPost(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('dashboard')

    return render(request, 'new_post.html', {'categories': categories, 'forms': forms})

@login_required
@permission_required('blog.change_datas', raise_exception=True)
def edit_post(request, slug):
    categories = Category.objects.all()
    post = get_object_or_404(Datas, slug=slug)
    forms = NewPost()
    if request.method == 'POST':
        forms = NewPost(request.POST, request.FILES, instance=post)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'Post updated successfully')
            return redirect('dashboard')

    return render(request, 'edit_post.html', {'categories': categories, 'post': post, 'forms': forms})

@login_required
@permission_required('blog.delete_datas', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Datas, id=post_id)
    post.delete()
    messages.success(request, 'post deleted successfully')
    return redirect('dashboard')
@login_required
@permission_required('blog.can_publish', raise_exception=True)
def publish_post(request, post_id):
    post = get_object_or_404(Datas, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, 'post published successfully')
    return redirect('dashboard')

