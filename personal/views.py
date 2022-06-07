from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from estates.views import get_estate_queryset
from estates.models import EstatePost

ESTATE_POSTS_PER_PAGE = 10


def home_screen_view(request):
	context = {}

	query = ""
	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	estate_posts = sorted(get_estate_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	estate_posts_paginator = Paginator(estate_posts, ESTATE_POSTS_PER_PAGE)

	try:
		estate_posts = estate_posts_paginator.page(page)
	except PageNotAnInteger:
		estate_posts = estate_posts_paginator.page(ESTATE_POSTS_PER_PAGE)
	except EmptyPage:
		estate_posts = estate_posts_paginator.page(estate_posts_paginator.num_pages)

	context['estate_posts'] = estate_posts

	return render(request, "personal/home.html", context)
