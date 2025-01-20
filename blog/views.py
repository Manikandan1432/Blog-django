from django.shortcuts import render, redirect
from.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import ContactForm
import logging

def Index(request):
    user = Datas.objects.all().order_by('created_at')
    title = 'Blog'

    paginator = Paginator(user, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'user': user, 'title': title, 'page_obj': page_obj})

def Details(request, slug):
    post = Datas.objects.get(slug=slug)
    related_posts = Datas.objects.filter(categories=post.categories).exclude(pk=post.id)
    return render(request, 'details.html',{'post': post, 'related_posts': related_posts})

def Contact(request):
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger('TESTING')
        if forms.is_valid():
            logger.debug(f'{forms.cleaned_data['name'], forms.cleaned_data['email'], forms.cleaned_data['message']}')
            error_message = 'Message has been sent'
            return render(request, 'contacts.html', {'forms':forms, 'error_message': error_message})
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

