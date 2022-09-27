from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponse

from .models import FollowersCnt, Post, PostLike, Profile


# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html', {
        'user': Profile.objects.get(user=request.user),
        'posts': Post.objects.all(),
    })


@login_required
def profile(request, pk):
    user_obj = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_obj)
    # posts=Post.objects.get(user=user.username)
    posts = Post.objects.filter(user=pk)

    follower = request.user.username
    user = pk

    if FollowersCnt.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCnt.objects.filter(user=pk))
    user_following = len(FollowersCnt.objects.filter(follower=pk))

    params = {
        'user_obj': user_obj,
        'profile': profile,
        'posts': posts,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', params)


@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCnt.objects.filter(follower=follower, user=user).exists():
            delete_follower = FollowersCnt.objects.get(
                follower=follower, user=user)
            delete_follower.delete()
        else:
            new_follower = FollowersCnt.objects.create(
                follower=follower, user=user)
            new_follower.save()

        return redirect('/profile/'+user)

    else:
        return redirect('/')


@login_required
def likePost(request):
    username = request.user.username
    post_id = request.GET['post_id']

    if PostLike.objects.filter(username=username, post_id=post_id).exists():
        post_to_delete = PostLike.objects.get(
            username=username, post_id=post_id)
        post_to_delete.delete()
        original_post = Post.objects.get(id=post_id)
        original_post.likes = original_post.likes-1
        original_post.save()
    else:
        post = PostLike.objects.create(username=username, post_id=post_id)
        post.save()
        original_post = Post.objects.get(id=post_id)
        original_post.likes = original_post.likes+1
        original_post.save()

    return redirect("/")


@login_required
def upload(request):
    if request.method == "POST":
        user = request.user.username
        upload_image = request.FILES.get('upload_image')
        caption = request.POST['my-caption']

        new_post = Post.objects.create(
            user=user, image=upload_image, caption=caption)
        new_post.save()

    return redirect("/")


@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') != None:
            updated_img = request.FILES.get('image')
            user_profile.profile_img = updated_img

        updated_bio = request.POST['bio']
        updated_location = request.POST['location']

        user_profile.bio = updated_bio
        user_profile.location = updated_location
        user_profile.save()

        return redirect('/')

    params = {'bio': user_profile.bio,
              'location': user_profile.location, 'profile_img': user_profile.profile_img}
    return render(request, 'setting.html', params)


def signUp(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if username == "":
            messages.error(request, "Username Can't be Blank")
            return redirect('signUp')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Id Already Exists !!!")
            return redirect('signUp')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username Taken !!!")
            return redirect('signUp')

        else:
            user = User.objects.create(
                username=username, email=email, password=password)
            user.save()

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model, id_user=user_model.id)
            new_profile.save()

            auth.login(request, user)

            return redirect('settings')
    else:
        return render(request, 'signup.html')


def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.password == password:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Wrong Password")
                return redirect("signIn")
        else:
            messages.error(request, "User Doesn't Exists !!!")
            return redirect("signIn")

    else:
        return render(request, 'signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('signIn')
