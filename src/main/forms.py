from django import forms
from .models import Post, Comment, Reply, Category, FundingComment
from django.contrib.auth.hashers import check_password
from bootstrap_modal_forms.forms import BSModalModelForm

class PostModelForm(BSModalModelForm):
    class Meta:
        model = Post
        fields = ('title','description')
        exclude = ['user','country','category']

class CategoryDeletionForm(BSModalModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= Category
        fields = ('confirm_password',)
    
    def clean(self):
        cleaned_data = super(CategoryDeletionForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.request.user.password):
            self.add_error('confirm_password', 'Password does not match.')

class CategoryForm(BSModalModelForm):
    class Meta:
        model = Category
        fields = ('name','description')

class PostDeletionForm(BSModalModelForm):
    class Meta:
        model = Post
        fields = []

class CommentDeletionForm(BSModalModelForm):
    class Meta:
        model = Comment
        fields = []

class ReplyDeletionForm(BSModalModelForm):
    class Meta:
        model = Reply
        fields = []


class CommentLoggedInForm(BSModalModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        exclude = ['user','post','anonUser']

class FundingMessageForm(BSModalModelForm):
    class Meta:
        model = FundingComment
        fields = ['comment']
        exclude = ['investor','post']


class CommentNotLoggedInForm(BSModalModelForm):
    class Meta:
        model = Comment
        fields = ['anonUser','comment']
        exclude = ['user','post']
    
class ReplyNotLoggedInForm(BSModalModelForm):
    class Meta:
        model = Reply
        fields = ['anonUser','reply']
        exclude = ['user','comment']
    
class ReplyLoggedInForm(BSModalModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
        exclude = ['user','comment','anonUser']
    
    
    