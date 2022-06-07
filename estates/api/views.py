from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from account.models import Account
from estates.models import EstatePost
from estates.api.serializers import EstatePostSerializer, EstatePostUpdateSerializer, EstatePostCreateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


# Url: https://<your-domain>/api/estates/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_estate_view(request, slug):
    try:
        estate_post = EstatePost.objects.get(slug=slug)
    except EstatePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EstatePostSerializer(estate_post)
        return Response(serializer.data)


# Url: https://<your-domain>/api/estates/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_estate_view(request, slug):
    try:
        estate_post = EstatePost.objects.get(slug=slug)
    except EstatePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if estate_post.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = EstatePostUpdateSerializer(estate_post, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            data['pk'] = estate_post.pk
            data['post_title'] = estate_post.post_title
            data['price'] = estate_post.price
            data['city'] = estate_post.city
            data['address'] = estate_post.address
            data['square_meters'] = estate_post.square_meters
            data['type'] = estate_post.type
            data['floor'] = estate_post.floor
            data['contracted'] = estate_post.contracted
            data['description'] = estate_post.description
            data['slug'] = estate_post.slug
            data['date_updated'] = estate_post.date_updated
            if estate_post.image:
                image_url = str(request.build_absolute_uri(estate_post.image.url))
                if "?" in image_url:
                    image_url = image_url[:image_url.rfind("?")]
                data['image'] = image_url
            if estate_post.proof_doc:
                data['proof_doc'] = estate_post.proof_doc.url
            data['username'] = estate_post.author.username

            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_is_author_of_estate_post(request, slug):
    try:
        estate_post = EstatePost.objects.get(slug=slug)
    except EstatePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if estate_post.author != user:
        data['response'] = "You don't have permission to edit that."
        return Response(data=data)
    data['response'] = "You have permission to edit that."
    return Response(data=data)


# Url: https://<your-domain>/api/estates/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_estate_view(request, slug):
    try:
        estate_post = EstatePost.objects.get(slug=slug)
    except EstatePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if estate_post.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = estate_post.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


# Url: https://<your-domain>/api/estates/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_estate_view(request):
    if request.method == 'POST':

        request.POST._mutable = True
        data = request.POST
        data['author'] = request.user.pk
        serializer = EstatePostCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            estate_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = estate_post.pk
            data['post_title'] = estate_post.post_title
            data['price'] = estate_post.price
            data['city'] = estate_post.city
            data['address'] = estate_post.address
            data['square_meters'] = estate_post.square_meters
            data['type'] = estate_post.type
            data['floor'] = estate_post.floor
            data['contracted'] = estate_post.contracted
            data['description'] = estate_post.description
            data['slug'] = estate_post.slug
            data['date_updated'] = estate_post.date_updated
            if estate_post.image:
                image_url = str(request.build_absolute_uri(estate_post.image.url))
                if "?" in image_url:
                    image_url = image_url[:image_url.rfind("?")]
                data['image'] = image_url
            if estate_post.proof_doc:
                data['proof_doc'] = estate_post.proof_doc.url
            data['username'] = estate_post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Url: 
    1) list: https://<your-domain>/api/estates/list
    2) pagination: http://<your-domain>/api/estates/list?page=2
    3) search: http://<your-domain>/api/estates/list?search=mitch
    4) ordering: http://<your-domain>/api/estates/list?ordering=-date_updated
    4) search + pagination + ordering: <your-domain>/api/estates/list?search=mitch&page=2&ordering=-date_updated
Headers: Authorization: Token <token>
"""


class ApiEstatesListView(ListAPIView):
    queryset = EstatePost.objects.all()
    serializer_class = EstatePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('post_title', 'description', 'author__username')
