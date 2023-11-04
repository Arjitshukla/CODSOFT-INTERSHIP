from django.shortcuts import render, redirect
from django.http import HttpResponse
from homeapp.models import Contact
from django.contrib import messages
from blogapp.models import Post
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate, login, logout 

# Create your views here.
# ==========================>>HTML Pages  <<=======================================

def home(request):
    return render (request,'home/home.html')
    
def about(request):
        return render (request,'home/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        Email=request.POST['email']
        phone=request.POST['phone']
        Content =request.POST['content']

        if len(name)<2 or len(Email)<3 or len(phone)<10 or len(Content)<4:
             messages.error(request, "fill the form correctly")
        else:
            contact=Contact(name=name, Email=Email, phone=phone, Content=Content)
            contact.save()
            messages.success(request, "succefully")
    return render(request, "home/contact.html")

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        # allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(Content__icontains=query)
        allPosts =allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params ={"allposts":allPosts,'query': query}
    return render (request,'home/search.html',params)

# ==========================>>Authentication Apis  <<=======================================

# sign up----------->>
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('/')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Blogdonkey has been successfully created")
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")

# login------------->>
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")

# logout ----------->>
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out :thanks you! ")
    return redirect('/')
