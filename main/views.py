from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Project


def home(request):
    projects = Project.objects.only(
        'title',
        'description',
        'image',
        'link',
        'likes',
        'views',
    )

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for reaching out! I will get back to you soon.')
            return redirect('main:home')
    else:
        form = ContactForm()

    return render(request, 'index.html', {'projects': projects, 'form': form})
