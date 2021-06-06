#django stuff
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
#user auth
from users.forms import *
#my stuff
from .models import Comment, Country,Category,NewUser,Post as Posts, Reply
from .forms import *


def index(request):
    if request.method == 'POST':
        Post = request.POST['name']
        NoneSelected = Country.objects.exclude(code=Post)
        selectedCountry = Country.objects.get(code = Post)
        content={}
        category = Category.objects.all()
        for i in category:
            content[i.name] = Posts.objects.filter(country=selectedCountry).filter(category=i.id).order_by('-date_created')[:5]

        return render(request,"main/main.html",{"countries":NoneSelected,"selected":selectedCountry,"posts":content})
    else:
        All_countries = Country.objects.all()
        return render(request,"main/main.html",{"countries":All_countries})

@login_required
def ViewCategories(request):
    if request.user.is_staff:
        categoryData = Category.objects.all()
        return render(request,"main/categoryPage.html",{"categories":categoryData})
    else:
        return redirect('index')

class UpdateCategory(BSModalUpdateView):
    model = Category
    template_name = 'main/forms/categoryUpdateForm.html'
    form_class = CategoryForm
    success_message = 'Category has been update'
    success_url = reverse_lazy('categoryView')
    @login_required
    def form_valid(self, form):
        if self.request.user.is_staff:
            if not self.request.is_ajax():
                reply = form.save(commit=False)
                reply.save()
                return redirect(self.get_success_url())
            else:
                return redirect(self.get_success_url())
        else:
            return reverse_lazy('index')

class DeleteCategory(BSModalUpdateView):
    template_name ='main/forms/categoryDelete.html'
    model=Category
    form_class = CategoryDeletionForm
    success_message = 'Category has been deleted'
    def get_success_url(self):
            return reverse_lazy('categoryView')
    def form_valid(self, form):
        if self.request.user.is_staff:
            if not self.request.is_ajax():
                category =  Category.objects.get(id=self.kwargs.get('pk'))
                category.delete()
                return redirect(self.get_success_url())
            else:
                return redirect(self.get_success_url())
        else:
            return reverse_lazy('index')
    

class CreateNewCategory(BSModalCreateView):
    template_name = 'main/forms/categoryCreateForm.html'
    form_class = CategoryForm
    success_message = 'Category has been created'
    def get_success_url(self):
        return reverse_lazy('categoryView')
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if not self.request.is_ajax():
                reply = form.save(commit=False)
                reply.save()
                return redirect(self.get_success_url())
            else:
                return redirect(self.get_success_url())
        else:
            return reverse_lazy('index')

def ViewMessages(request):
    if not request.user.is_staff and not request.user.is_investor:
        postData = FundingComment.objects.filter(post__user__id=request.user.id,post__is_funded=True)
        return render(request,"main/messages.html",{'context':postData})
    else:
        return redirect('index')


def ViewPost(request,postID):
    postData = Posts.objects.get(id=postID)
    commentTemp = Comment.objects.filter(post__id=postID)
    commentData = {}
    for i in commentTemp:
        commentData[i.id]={'comment':i,'replies':Reply.objects.filter(comment=i.id)}
    is_validated = False
    if(postData.user == request.user or request.user.is_staff == True):
        is_validated = True
    userData = NewUser.objects.get(id=postData.user.id)
    return render(request,"main/postView.html",{"posts":postData,"auther":userData,"is_valid": is_validated,"comments":commentData})

class FundingCommentCreate(BSModalCreateView):
    template_name = 'main/forms/fundingPost.html'
    form_class = FundingMessageForm
    success_message = 'Post has been funded'
    def get_success_url(self):
        return reverse_lazy('postView', kwargs={'postID': self.kwargs.get('pk')})

    def form_valid(self, form):
        tempPost = Posts.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.is_authenticated and self.request.user.is_investor and not tempPost.is_funded:
            if not self.request.is_ajax():
                comment = form.save(commit=False)
                comment.investor = NewUser.objects.get(id=self.request.user.id)
                comment.post = Posts.objects.get(id=self.kwargs.get('pk'))
                tempPost.is_funded = True
                tempPost.save()
                comment.save()
                return redirect(self.get_success_url())
            else:
                return redirect('index')
        else:
            return redirect(request.META['HTTP_REFERER'])

class ReplyLoggedCreateView(BSModalCreateView):
    template_name = 'main/forms/newReply.html'
    form_class = ReplyLoggedInForm
    success_message = 'Reply has been created'
    def get_success_url(self):
        #return reverse_lazy('index')
        return reverse_lazy('postView',kwargs={'postID': self.kwargs.get('postID')})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if not self.request.is_ajax():
                reply = form.save(commit=False)
                reply.user = NewUser.objects.get(id=self.request.user.id)
                reply.comment = Comment.objects.get(id=self.kwargs.get('pk'))
                reply.save()
                return redirect(self.get_success_url())
            else:
                return redirect('index')
        else:
            return reverse_lazy('postView',kwargs={'postID': self.kwargs.get('postID')})

class ReplyNotLoggedCreateView(BSModalCreateView):
    template_name = 'main/forms/newReply.html'
    form_class = ReplyNotLoggedInForm
    success_message = 'Reply has been created'
    def get_success_url(self):
        #return reverse_lazy('index')
        return reverse_lazy('postView',kwargs={'postID': self.kwargs.get('postID')})

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            if not self.request.is_ajax():
                reply = form.save(commit=False)
                reply.comment = Comment.objects.get(id=self.kwargs.get('pk'))
                reply.save()
                return redirect(self.get_success_url())
            else:
                return redirect('index')
        else:
            return reverse_lazy('postView',kwargs={'postID': self.kwargs.get('postID')})

class CommentLoggedCreateView(BSModalCreateView):
    template_name = 'main/forms/newComment.html'
    form_class = CommentLoggedInForm
    success_message = 'Comment has been created'
    def get_success_url(self):
        return reverse_lazy('postView', kwargs={'postID': self.kwargs.get('pk')})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if not self.request.is_ajax():
                comment = form.save(commit=False)
                comment.user = NewUser.objects.get(id=self.request.user.id)
                comment.post = Posts.objects.get(id=self.kwargs.get('pk'))
                comment.save()
                return redirect(self.get_success_url())
            else:
                return redirect('index')
        else:
            return redirect(request.META['HTTP_REFERER'])

class CommentNotLoggedCreateView(BSModalCreateView):
    template_name = 'main/forms/newComment.html'
    form_class = CommentNotLoggedInForm
    success_message = 'Comment has been created'
    def get_success_url(self):
        #return reverse_lazy('index')
        return reverse_lazy('postView', kwargs={'postID': self.kwargs.get('pk')})

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            if not self.request.is_ajax():
                comment = form.save(commit=False)
                comment.post = Posts.objects.get(id=self.kwargs.get('pk'))
                comment.save()
                return redirect(self.get_success_url())
            else:
                return redirect(self.get_success_url())
        else:
            return redirect(request.META['HTTP_REFERER'])

class DeleteComment(BSModalDeleteView):
    template_name ='main/forms/deleteComment.html'
    model=Comment
    form_class = CommentDeletionForm
    success_message = 'Post has been created'
    def get_success_url(self):
            postData = Comment.objects.get(id=self.kwargs.get('pk'))
            return reverse_lazy('postView', kwargs={'postID': postData.post.id})
    @login_required
    def form_valid(self, form):
        postData = Comment.objects.get(id=self.kwargs.get('pk'))
        if(postData.user == self.request.user or self.request.user.is_staff == True):
            postData.delete()
            return redirect(self.get_success_url())
        else:
            return reverse_lazy(self.get_success_url())

class DeleteReply(BSModalDeleteView):
    template_name ='main/forms/deleteComment.html'
    model=Reply
    form_class = ReplyDeletionForm
    success_message = 'Post has been created'
    def get_success_url(self):
            return reverse_lazy('postView', kwargs={'postID': self.kwargs.get('postID')})
    @login_required
    def form_valid(self, form):
        postData = Reply.objects.get(id=self.kwargs.get('pk'))
        if(postData.user == self.request.user or self.request.user.is_staff == True):
            postData.delete()
            return redirect(self.get_success_url())
        else:
            return reverse_lazy(self.get_success_url())

class DeletePost(BSModalDeleteView):
    model = Posts
    template_name ='main/forms/deletionQuestion.html'
    form_class = PostDeletionForm
    success_message = 'Post has been created'
    def get_success_url(self):
            return reverse_lazy('index')
    
    @login_required
    def form_valid(self, form):
        postData = Posts.objects.get(id=self.kwargs.get('pk'))
        if(postData.user == self.request.user or self.request.user.is_staff == True):
            postData.delete()
            return redirect(self.get_success_url())
        else:
            return reverse_lazy(self.get_success_url())

def categoryView(request,region,cat):
    if request.method == 'GET':
        selectedPosts = Posts.objects.filter(category__name=cat).filter(country__name=region).order_by('-date_created')
        paginator = Paginator(selectedPosts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"main/categories.html",{"movies":page_obj,"test":{'region':region,'category':cat}})
    else:
        return redirect('/')

class PostCreateView(BSModalCreateView):
    template_name = 'main/forms/newPost.html'
    form_class = PostModelForm
    success_message = 'Post has been created'
    def get_success_url(self):
        return reverse_lazy('category_view', kwargs={'region': self.kwargs.get('region'),'cat': self.kwargs.get('cat')})
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if not self.request.is_ajax():
                posts = form.save(commit=False)
                posts.user = NewUser.objects.get(id=self.request.user.id)
                posts.country = Country.objects.get(name=self.kwargs.get('region'))
                posts.category = Category.objects.get(name=self.kwargs.get('cat')) 
                posts.save()
                return redirect(self.get_success_url())
            else:
                return redirect(self.get_success_url())
        else:
            return redirect(self.get_success_url())


#Account stuff
def registerPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password1')
            
            account = authenticate(email=email,user_name=user_name,password=password)
            login(request,account)
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'main/register.html',context)

def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method =='POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect(request.META['HTTP_REFERER'])
        else:
            context['login_form'] = form
            return render(request,'main/login.html',context)
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request,'main/login.html',context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            if not request.is_ajax():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/forms/passwordUpdateForm.html', {
        'form': form
    })

class AccountUpdateForm(BSModalUpdateView):
    model = NewUser
    template_name = 'main/forms/profileUpdateForm.html'
    form_class = AccountUpdateForm
    success_message = 'Success: Account was updated.'
    success_url = reverse_lazy('profile')

class CompanyUpdateForm(BSModalUpdateView):
    model = NewUser
    template_name = 'main/forms/profileUpdateForm.html'
    form_class = CompanyUpdateForm
    success_message = 'Success: Company information was updated.'
    success_url = reverse_lazy('profile')


class DeleteAccount(BSModalUpdateView):
    template_name = 'main/forms/accountDelete.html'
    form_class = PasswordConfirmationForm
    model = NewUser
    success_url = reverse_lazy('/')

    def get_object(self, queryset=None):
        '''This loads the profile of the currently logged in user'''
        return NewUser.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        if not self.request.is_ajax():
            account =  NewUser.objects.get(id=self.request.user.id)
            account.delete()
            logout(self.request)
            return redirect('index')
        else:
            return redirect('index')
        

@login_required
def profilePage(request):
    content = {'user':request.user}
    return render(request,'main/profile.html',content)

def logoutPage(request):
    if request.user.is_authenticated == False:
        return redirect(request.META['HTTP_REFERER'])
    logout(request)
    return redirect('index')