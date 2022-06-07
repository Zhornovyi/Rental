from django.urls import path
from estates.api.views import (
	api_detail_estate_view,
	api_update_estate_view,
	api_delete_estate_view,
	api_create_estate_view,
	api_is_author_of_estate_post,
	ApiEstatesListView
)
# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'estates'

urlpatterns = [
	path('<slug>/', api_detail_estate_view, name="detail"),
	path('<slug>/update', api_update_estate_view, name="update"),
	path('<slug>/delete', api_delete_estate_view, name="delete"),
	path('create', api_create_estate_view, name="create"),
	path('list', ApiEstatesListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_estate_post, name="is_author"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)