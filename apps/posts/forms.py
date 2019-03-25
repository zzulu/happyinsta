from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': '',
        'rows': 5,
        'cols': 50,
        'placeholder': 'What are you doing?', }))

    class Meta:
        model = Post
        fields = ['content',]


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form__input',
        'placeholder': 'Write a comment...',
        'autocomplete': 'off', }))

    class Meta:
        model = Comment
        fields = ['content',]
