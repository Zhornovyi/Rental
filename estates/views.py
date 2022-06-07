from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from estates.models import EstatePost
from estates.forms import CreateEstatePostForm, UpdateEstatePostForm

from account.models import Account


def create_estate_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    form = CreateEstatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateEstatePostForm()
    context['form'] = form
    return render(request, "estate/estate_create.html", context)


def detail_estate_view(request, slug):
    context = {}
    estate_post = get_object_or_404(EstatePost, slug=slug)
    context['estate_post'] = estate_post
    return render(request, 'estate/estate_details.html', context)


def edit_estate_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    estate_post = get_object_or_404(EstatePost, slug=slug)
    if estate_post.author != user:
        return HttpResponse("You are not the author of that post.")
    if request.POST:
        form = UpdateEstatePostForm(request.POST or None, request.FILES or None, instance=estate_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            estate_post = obj
    form = UpdateEstatePostForm(
        initial={
            "post_title": estate_post.post_title,
            "description": estate_post.description,
            "image": estate_post.image,
        }
    )

    context['form'] = form
    return render(request, 'estate/estate_edit.html', context)


def get_estate_queryset(query=None):
    queryset = []
    queries = query.split(" ")  # python install 2019 = [python, install, 2019]
    for q in queries:
        posts = EstatePost.objects.filter(
            Q(post_title__icontains=q) |
            Q(description__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))
