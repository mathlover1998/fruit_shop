from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def get_all_blog_posts(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 4
    offset = (int(page_number) - 1) * items_per_page 
    queryset = Blog.objects.all()[offset:offset + items_per_page]
    has_next_page = len(queryset) == items_per_page
    return render(request, 'blog/blogs.html', {'blog_posts': queryset, 'page_number': page_number, 'has_next_page': has_next_page})


# def get_blog_post(request,id):
#     post = get_object_or_404(Blog,id=id)
#     comments = Comments.objects.filter(blog_post = post,parent_comment__isnull=True)
#     organized_comments = []
#     for comment in comments:
#         organized_comments.append(comment)
#         organized_comments.extend(comment.replies.filter(is_approved=True))
#     return render(request,'blog/post-details.html',{'post':post,'comments':organized_comments})

# def get_posts_by_tag(request,tag_id):
#     posts = Blog.objects.filter(tags__id=tag_id)
#     return render(request,'blog/blog.html',{'blog_posts':posts})

# def get_posts_by_category(request,category_id):
#     posts = Blog.objects.filter(categories__id=category_id)
#     return render(request,'blog/blog.html',{'blog_posts':posts})

# @login_required(login_url="/account/log-in")
# def create_blog_post(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         subtitle = request.POST.get('subtitle')
#         slug = request.POST['slug']
#         tags = request.POST.getlist('tags')
#         content = request.POST['content']
#         image = request.FILES['image']
#         blog = Blog.objects.create(title = title,
#                                  slug = slug,
#                                  subtitle = subtitle,
#                                  content = content,
#                                  author = request.user,
#                                  image = image,
#                                  )
#         for tag_name in tags:
#             tag_name = tag_name.strip()
#             tag, created = Tags.objects.get_or_create(name = tag_name)
#             blog.tags.add(tag)    
#         return redirect('home')
#     return render(request,'blog/create-post.html',{'update':False})


# @login_required
# def get_your_blog_posts(request):
#     author = request.user
#     page_number = request.GET.get('page', 1)
#     items_per_page = 4
#     offset = (int(page_number) - 1) * items_per_page
#     queryset = Blog.objects.filter(author=author)[offset:offset + items_per_page]
#     has_next_page = len(queryset) == items_per_page
#     return render(request,'blog/your-posts.html',{'blog_posts': queryset, 'page_number': page_number, 'has_next_page': has_next_page})

# @login_required
# def update_blog_post(request, id):
#     blog_post = get_object_or_404(Blog, id=id)

#     if request.method == 'POST':
#         blog_post.title = request.POST.get('title')
#         blog_post.slug = request.POST.get('slug')
#         blog_post.subtitle = request.POST.get('subtitle')
#         blog_post.content = request.POST.get('content')
#         tags = request.POST.getlist('tags')
#         if 'image' in request.FILES:
#             blog_post.image = request.FILES['image']
#         for tag_name in tags:
#             tag_name = tag_name.strip()
#             tag, created = Tags.objects.get_or_create(name = tag_name)
#             blog_post.tags.add(tag)    
#         blog_post.save()

#         return redirect('your_blog_posts')

#     return render(request, 'blog/create-post.html', {'blog_post': blog_post, 'update': True})
    
# @login_required
# def delete_blog_post(request,id):
#     blog_post = get_object_or_404(Blog,id=id)
#     blog_post.delete()
#     return redirect('your_blog_posts')


# @login_required
# def create_comment(request,id): 
#     blog_post = get_object_or_404(Blog,id =id)
#     if request.method =='POST':
#         Comments.objects.create(
#             content = request.POST.get('content'),
#             is_approved = True,
#             blog_post = blog_post,
#             author = request.user
#         )
#         return redirect('blog_post',id=id)
#     return render(request,'blog/post-details.html')

# @login_required
# def reply_comment(request):
#     if request.method =='POST':
#         parent_comment_id = request.POST.get('comment_id')
#         post_id = request.POST.get('post_id')
#         parent_comment = get_object_or_404(Comments,id=parent_comment_id)
#         message = request.POST.get('content')
#         Comments.objects.create(
#             blog_post = get_object_or_404(Blog,id=post_id),
#             author = request.user,
#             content = message,
#             is_approved = True,
#             parent_comment = parent_comment
#         )
#         return redirect('blog_post',id=post_id)
#     return render(request, 'blog/post-details.html')

    
        
        
# @login_required
# def edit_comment(request,post_id):
#     blog_post = get_object_or_404(Blog, pk=post_id)
#     if request.method == 'POST':
#         comment_id = request.POST.get('comment_id')
#         comment = get_object_or_404(Comments, pk=comment_id)
#         if request.user != comment.author:
#             return redirect('some_permission_denied_page')
#         else:
#             comment.content = request.POST.get('content')
#             comment.save()
#             return redirect('blog_post', id=post_id)
#     return render(request, 'blog/post-details.html', {'blog_post': blog_post})

# @login_required
# def delete_comment(request,post_id):
#     comment_id = request.GET.get('comment_id')
#     comment = get_object_or_404(Comments, pk=comment_id)
#     comment.delete()
#     return redirect('blog_post', id=post_id)

# def search_results(request):
#     query = request.GET.get('q')
    
#     if query:
#         blogs = Blog.objects.filter(title__icontains=query)
#     else:
#         blogs = Blog.objects.none()
    
#     return render(request, 'blog/search-results.html', {'blog_posts': blogs, 'query': query})


# def like_comment(request):
#     pass

# def unlike_comment(request):
#     pass

# def like_post(request):
#     pass

# def unlike_post(request):
#     pass

# def share_post(request):
#     pass