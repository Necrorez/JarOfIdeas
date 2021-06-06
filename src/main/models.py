from django.db import models
from users.models import NewUser
# Create your models here.

class Category(models.Model):
    name =  models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f"{self.name}"
    
    
class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5)
    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_funded = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} {self.category} {self.country}"

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    anonUser = models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"{self.user} {self.post}"

class FundingComment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    investor = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.investor} {self.post}"

class Reply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(Comment,null=True,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    anonUser = models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"{self.user} {self.comment}"


""" drop table main_category;             
drop table main_comment;              
drop table main_country;              
drop table main_country_category;     
drop table main_post;    """