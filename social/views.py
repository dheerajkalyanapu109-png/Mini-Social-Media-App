from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Profile, Post, Comment, Follow

def _posts(request, qs):
    qs = qs.select_related("author").annotate(n_likes=Count("likes", distinct=True), n_comments=Count("comments", distinct=True))
    posts = list(qs)
    liked = set(request.user.liked_posts.values_list("id", flat=True)) if request.user.is_authenticated else set()
    for p in posts: p.liked = p.id in liked
    return posts

def feed(request):
    qs, mode = Post.objects.all(), "all"
    if request.user.is_authenticated and not request.GET.get("all"):
        ids = list(request.user.following_set.values_list("following_id", flat=True)) + [request.user.id]
        qs, mode = qs.filter(author_id__in=ids), "following"
    return render(request, "feed.html", {"posts": _posts(request, qs), "mode": mode})

@require_POST
@login_required
def post_create(request):
    text = request.POST.get("text", "").strip()[:280]
    if text: Post.objects.create(author=request.user, text=text)
    else: messages.error(request, "Write something first.")
    return redirect("feed")

def post_detail(request, pk):
    post = _posts(request, Post.objects.filter(pk=pk))
    if not post: return redirect("feed")
    return render(request, "post_detail.html", {"p": post[0], "comments": Comment.objects.filter(post_id=pk).select_related("author")})

@require_POST
@login_required
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    text = request.POST.get("text", "").strip()[:280]
    if text: Comment.objects.create(post=post, author=request.user, text=text)
    return redirect("post_detail", pk=pk)

@require_POST
@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists(): post.likes.remove(request.user); liked = False
    else: post.likes.add(request.user); liked = True
    if request.headers.get("x-requested-with") == "fetch":
        return JsonResponse({"liked": liked, "count": post.likes.count()})
    return redirect("post_detail", pk=pk)

def profile(request, username):
    u = get_object_or_404(User, username=username)
    Profile.objects.get_or_create(user=u)
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=u).exists()
    return render(request, "profile.html", {"u": u, "posts": _posts(request, u.posts.all()), "is_following": is_following,
        "followers": u.follower_set.count(), "following": u.following_set.count()})

@require_POST
@login_required
def follow_toggle(request, username):
    u = get_object_or_404(User, username=username)
    if u != request.user:
        f, created = Follow.objects.get_or_create(follower=request.user, following=u)
        if not created: f.delete()
    return redirect("profile", username=username)

@login_required
def edit_profile(request):
    prof, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        prof.bio = request.POST.get("bio", "").strip()[:160]; prof.save()
        return redirect("profile", username=request.user.username)
    return render(request, "edit_profile.html", {"prof": prof})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(); Profile.objects.create(user=user); login(request, user); return redirect("feed")
    return render(request, "registration/register.html", {"form": form})
