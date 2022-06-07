import os
from rest_framework import serializers
from estates.models import EstatePost
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from estates.utils import is_image_aspect_ratio_valid, is_image_size_valid

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 20


class EstatePostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')
    proof_doc = serializers.SerializerMethodField('validate_proof_doc')

    class Meta:
        model = EstatePost
        fields = ['pk', 'slug', 'post_title',
                  'city', 'address', 'price', 'square_meters', 'type', 'floor',
                  'description', 'image', 'proof_doc', 'date_updated', 'username', 'contracted']

    def get_username_from_author(self, estate_post):
        username = estate_post.author.username
        return username

    def validate_image_url(self, estate_post):
        image = estate_post.image
        if image:
            new_url = image.url
            if "?" in new_url:
                new_url = image.url[:image.url.rfind("?")]
            return new_url
        else:
            return ""

    def validate_proof_doc(self, estate_post):
        try:
            return estate_post.proof_doc.url
        except:
            return ""


class EstatePostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatePost
        fields = ['post_title', 'description', 'image', 'contracted',
                  'city', 'address', 'price', 'square_meters', 'type', 'floor']

    def validate(self, estate_post):
        try:
            title = estate_post['post_title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = estate_post['description']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = estate_post['image'] if 'image' in estate_post else None

            if image:
                url = os.path.join(settings.TEMP, str(image))
                storage = FileSystemStorage(location=url)

                with storage.open('', 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()

                # Check image size
                if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                    os.remove(url)
                    raise serializers.ValidationError(
                        {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

                # Check image aspect ratio
                if not is_image_aspect_ratio_valid(url):
                    os.remove(url)
                    raise serializers.ValidationError(
                        {"response": "Image height must not exceed image width. Try a different image."})

                os.remove(url)
        except KeyError:
            pass
        return estate_post


class EstatePostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatePost
        fields = ['post_title', 'description', 'image', 'date_updated', 'author', 'slug',
                  'city', 'address', 'price', 'square_meters', 'type', 'floor', 'proof_doc']

    def save(self):
        try:
            post_title = self.validated_data['post_title']
            if len(post_title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            description = self.validated_data['description']
            if len(description) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a description longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = self.validated_data['image'] if 'image' in self.validated_data else None
            proof_doc = self.validated_data['proof_doc'] if 'proof_doc' in self.validated_data else None

            estate_post = EstatePost(
                author=self.validated_data['author'],
                post_title=post_title,
                description=description,
                image=image,
                proof_doc=proof_doc,
                city=self.validated_data['city'],
                price=self.validated_data['price'],
                address=self.validated_data['address'],
                square_meters=self.validated_data['square_meters'],
                type=self.validated_data['type'],
                floor=self.validated_data['floor'],
                slug=self.validated_data['slug']
            )
            if image:
                url = os.path.join(settings.TEMP, str(image))
                storage = FileSystemStorage(location=url)

                with storage.open('', 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()

                # Check image size
                if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                    os.remove(url)
                    raise serializers.ValidationError(
                        {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

                # Check image aspect ratio
                if not is_image_aspect_ratio_valid(url):
                    os.remove(url)
                    raise serializers.ValidationError(
                        {"response": "Image height must not exceed image width. Try a different image."})

                os.remove(url)
            estate_post.save()
            return estate_post
        except KeyError:
            raise serializers.ValidationError(
                {"response": f"request must contain the following fields: {self.Meta.fields}."})
