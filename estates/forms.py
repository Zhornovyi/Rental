from django import forms

from estates.models import EstatePost


class CreateEstatePostForm(forms.ModelForm):

	class Meta:
		model = EstatePost
		fields = '__all__'
		exclude = ['slug', 'author', 'date_updated', 'date_published', 'contracted']


class UpdateEstatePostForm(forms.ModelForm):

	class Meta:
		fields = '__all__'
		exclude = ['slug', 'author', 'date_updated', 'date_published', 'contracted']

	def save(self, commit=True):
		estate_post = self.instance
		estate_post.post_title = self.cleaned_data['post_title']
		estate_post.description = self.cleaned_data['description']

		if self.cleaned_data['image']:
			estate_post.image = self.cleaned_data['image']

		if commit:
			estate_post.save()
		return estate_post
