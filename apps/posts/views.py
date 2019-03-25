from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from .models import Post, Comment
from .forms import CommentForm


@login_required
def list(request):
    posts = Post.objects.filter(user__in=request.user.followings.all()).select_related('user').prefetch_related('like_users').all()
    comment_form = CommentForm()
    return render(request, 'posts/post_list.html', {'posts': posts, 'comment_form': comment_form})


@require_POST
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_id = post_id
        comment.user = request.user
        comment.save()    
        status = 200
        data = {'pk': comment.pk, 'post_id': comment.post_id, 'username': comment.user.username, 'content': comment.content}
    else:
        status = 422
        data = {}
           
    return JsonResponse(data, status=status)


@require_POST
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user != request.user:
        status = 422
        data = {}
    else:
        status = 200
        data = {'pk': comment.pk}
        comment.delete()
        
    return JsonResponse(data, status=status)


@require_POST
def post_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        data = {'liked': False}
    else:
        post.like_users.add(request.user)
        data = {'liked': True}

    return JsonResponse(data)
