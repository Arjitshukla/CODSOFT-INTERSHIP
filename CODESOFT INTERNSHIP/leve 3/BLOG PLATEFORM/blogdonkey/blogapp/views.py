from django.shortcuts import redirect,render
from blogapp.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

# ===========================>>BLOG pages <<=====================================

def bloghome(request):
    allPosts = Post.objects.all()
    context ={'allposts':allPosts}
    return render (request,'blog/blog.html',context)

def blogpost(request,slug):
    post = Post.objects.filter(slug =slug)[0]
    comments= BlogComment.objects.filter(post=post)
    context ={"post":post, 'comments': comments, 'user': request.user}
    return render (request,'blog/blogpost.html',context)
   

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        comment=BlogComment(comment= comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")