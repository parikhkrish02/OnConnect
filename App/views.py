from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from itertools import chain
import random

from .models import FollowersCnt, Post, Profile


@login_required
def index(request):
    user_following_list = []
    feed = []

    user_following = FollowersCnt.objects.filter(
        follower=request.user)

    for users in user_following:
        user_following_list.append(users.user)

    for user in user_following_list:
        feed_lists = Post.objects.filter(user=user)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_following_all.append(user.user)

    new_suggestions_list = [x for x in list(
        all_users) if (x not in list(user_following_all))]

    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users)

    for user in username_profile:
        profile_lists = Profile.objects.filter(user=user)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {
        'user': Profile.objects.get(user=request.user),
        'posts': feed_list,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
    })


@login_required
def profile(request, pk):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=User.objects.get(username=pk))

    user = User.objects.get(username=pk)
    follower = request.user

    if FollowersCnt.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_following = len(user.followers.all())
    user_followers = len(user.following.all())

    params = {
        'user_obj': user,
        'profile': profile,
        'posts': posts,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', params)


def followers(request, pk):
    user = User.objects.get(username=pk)
    following_list = []
    for u in user.following.all():
        following_list.append(u.follower)

    return render(request, "followers.html", {"followers_list": following_list})


def following(request, pk):
    user = User.objects.get(username=pk)
    followers_list = []

    for u in user.followers.all():
        followers_list.append(u.user)

    return render(request, "following.html", {"following_list": followers_list})


@login_required
def follow(request):
    if request.method == 'POST':
        follower = User.objects.get(username=request.POST['follower'])
        user = User.objects.get(username=request.POST['user'])

        if FollowersCnt.objects.filter(follower=follower, user=user).exists():
            delete_follower = FollowersCnt.objects.get(
                follower=follower, user=user)
            delete_follower.delete()
        else:
            new_follower = FollowersCnt.objects.create(
                follower=follower, user=user)
            new_follower.save()

        return redirect('/profile/'+user.username)

    else:
        return redirect('/')


@login_required
def likePost(request):
    user = request.user
    post_id = request.GET['post_id']

    flag = True
    for u in Post.objects.get(id=post_id).likes.all():
        if user == u:
            Post.objects.get(id=post_id).likes.remove(user)
            original_post = Post.objects.get(id=post_id)
            original_post.save()
            flag = False

    if flag:
        Post.objects.get(id=post_id).likes.add(user)
        original_post = Post.objects.get(id=post_id)
        original_post.save()

    return redirect("/")


@login_required
def upload(request):
    if request.method == "POST":
        user = request.user
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

        if password == "":
            messages.error(request, "Password Can't be Blank")
            return redirect('signUp')

        if email == "":
            messages.error(request, "Email Can't be Blank")
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

            new_profile = Profile.objects.create(user=user)
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
