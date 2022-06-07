from django.urls import path
from estates.views import (
	create_estate_view,
	detail_estate_view,
	edit_estate_view,
)

app_name = 'estates'

urlpatterns = [
	path('create/', create_estate_view, name="create"),
	path('<slug>/', detail_estate_view, name="detail"),
	path('<slug>/edit', edit_estate_view, name="edit"),
]