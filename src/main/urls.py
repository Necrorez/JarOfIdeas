from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('profile/',views.profilePage,name='profile'),
    path('categoriesView/',views.ViewCategories,name='categoryView'),
    path('categoriesView/new/',views.CreateNewCategory.as_view(),name='createNewCategory'),
    path('categoriesView/update/<slug:pk>/',views.UpdateCategory.as_view(),name='updateCategory'),
    path('categoriesView/delete/<slug:pk>/',views.DeleteCategory.as_view(),name='deleteCategory'),
    path('messages/',views.ViewMessages,name='messages'),
    path('fund/<pk>/', views.FundingCommentCreate.as_view(),name='fundPost'), 
    path('',views.index,name='country_select'),
    path('<region>/<cat>', views.categoryView,name='category_view'),
    path('<region>/<cat>/create/', views.PostCreateView.as_view(),name='newPost'),
    path('post/<postID>/', views.ViewPost,name='postView'),
    path('delete/<pk>/', views.DeletePost.as_view(),name='deletePost'),
    path('add/<pk>/', views.CommentLoggedCreateView.as_view(),name='addCommentLogged'),
    path('addA/<pk>/', views.CommentNotLoggedCreateView.as_view(),name='addCommentNotLogged'),
    path('add/reply/<pk>/<postID>/', views.ReplyLoggedCreateView.as_view(),name='addReplyLogged'),
    path('addA/reply/<pk>/<postID>/', views.ReplyNotLoggedCreateView.as_view(),name='addReplyNotLogged'),
    path('delete/comment/<pk>/', views.DeleteComment.as_view(),name='deleteComment'),
    path('delete/<postID>/<pk>/', views.DeleteReply.as_view(),name='deleteReply'),
    path('profile/update/<pk>/', views.AccountUpdateForm.as_view(),name='updateProfile'),
    path('profile/update/company/<pk>/', views.CompanyUpdateForm.as_view(),name='updateCompany'),
    path('profile/update/', views.change_password,name='changePassword'),
    path('profile/delete/', views.DeleteAccount.as_view(),name='deleteAccount'),
]
