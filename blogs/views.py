from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from django.core.mail import send_mail
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField
from core.models import *
from .forms import *
from django.db.models import Count, Avg, Sum
from django.shortcuts import render, redirect
from common.utils import send_notification_email

class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee

class BlogListView(LoginRequiredMixin, generic.ListView):
    template_name = "blogs/blog_list.html"
    queryset = Blog.objects.all().filter(status="PUBLISHED") # for published blogs
    #queryset = Blog.objects.all().filter(status=2)
    #queryset = Blog.objects.all()
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "blogs"
    paginate_by = 4

class BlogDraftListView(admin, generic.ListView):
    template_name = "blogs/blog_list_draft.html"
    queryset = Blog.objects.all().filter(status="DRAFT") # for published blogs
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "drafts"
    paginate_by = 4

class BlogArchivedListView(admin, employee, generic.ListView):
    template_name = "blogs/blog_list_archived.html"
    queryset = Blog.objects.all().filter(status="ARCHIVED") # for published blogs
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "archived"
    paginate_by = 4
    
        
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "blogs/category_list.html"
    queryset = Category.objects.all() # not adding context here
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "category"
    paginate_by = 4

#creating permission, the below will be used for view the admin only could manage


#@user_passes_test(is_admin)
class BlogCreateViewAlert(admin, employee,  CreateView):
    template_name = "blogs/blog_create.html"
    form_class = BlogForm
    success_url = reverse_lazy('blogs:blog-list')
    
    
    def form_valid( self, form):
        form.instance.author = self.request.user
        form.instance.email = self.request.user.email
        if form.instance.status =='DRAFT':
            subject = 'New Blog Created' if form.instance.status=='PUBLISHED' else 'Blog Published'
            message = 'A new blog post has been created' if form.instance.status=='PUBLISHED' else 'A blog post has been published'
            recipient_list = ['babala.assih@gmail.com', 'user2@example.com']  # List of recipients
            send_notification_email(subject, message, recipient_list)
            
        return super().form_valid(form)
    
 
class BlogCreateView(admin, employee,  CreateView):
    template_name = "blogs/blog_create.html"
    form_class = BlogForm
    success_url = reverse_lazy('blogs:blog-list')
    
    
    def form_valid( self, form):
        form.instance.author = self.request.user
        form.instance.email = self.request.user.email
        return super().form_valid(form)
       
class CategoryCreateView(admin, employee, CreateView):
    template_name = "blogs/category_create.html"
    form_class = CategoryForm
    
    def get_success_url(self):
        return reverse("blogs:category-list")
    
@login_required  
def blog_detail(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    # Check if the user has already read this blog post
    if not BlogRead.objects.filter(reader=user, blog_post=blog).exists():
        BlogRead.objects.create(reader=user, blog_post=blog)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviews = Review(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["content"],
                blog=blog
            )
            reviews.save()

    reviews = Review.objects.filter(blog=blog)
    #reply = Review.objects.filter(blog=blog).get(pk=pk)
    review_count = Review.objects.filter(blog=blog).annotate(num_reviews=Count("rating")).count()
    sum_rating = Review.objects.filter(blog=blog).aggregate(Sum("rating"))
    if Review.objects.filter(blog=blog).count() == 0:
        average_rating = 0
    else:
        #average_rating = Review.objects.filter(blog=blog).aggregate(Avg("rating"))
    #replies = ReplyToReview.objects.filter(blog=blog, review=reviews)
    
        average_rating = Review.objects.filter(blog=blog).aggregate(Avg("rating"))
    average_rating = average_rating.get('rating__avg')# format the average rating
    average_rating = round((average_rating),0)# the whole number
    blogs = Blog.objects.all()
    #blog_user = CustomUser.objects.filter(user=request.user)
   
    context = {
        "blog": blog,
        "reviews": reviews,
        #"replies": replies,
        "form": form,
        "review_count": review_count,
        "average_rating": average_rating,
        "sum_rating": sum_rating,
        "blogs": blogs,
        #"blog_user": blog_user
        
    }

    return render(request, "blogs/blog_detail.html", context)


def read_history(request):
    # Assuming you have the user object available
    return render(request, 'blogs/read_history.html', {'reader': request.user})

class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "blogs/blog_detail.html"
    queryset = Blog.objects.all() # not adding context here
    context_object_name = "blogs"

class BlogUpdateView(admin, employee, generic.UpdateView):
    template_name = "blogs/blog_update.html"
    form_class = BlogFormUpdate
    queryset = Blog.objects.all()
    
    def get_success_url(self):
        return reverse("blogs:blog-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(BlogUpdateView, self).form_valid(form)
    
   
class BlogDeleteView1(admin, generic.DeleteView):
    template_name = "blogs/blog_delete.html"
    queryset = Blog.objects.all()
    
    def get_success_url(self):
        return reverse("blogs:blog-list")


class BlogDeleteView(admin, generic.DeleteView):
    template_name = "blogs/blog_delete.html"
    queryset = Blog.objects.all()
    context_object_name = "delete_blogs"
    
    def get_success_url(self):
        return reverse("blogs:blog-list")

@login_required
def add_review(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            
            review.blog = blog
            review.user = request.user
            
            review.save()
            return redirect('blogs/blog_detail.html', pk=blog.pk)
    else:
        form = ReviewForm()
    return render(request, 'blogs/review_create.html', {'form': form, ' blog': blog})


   
class ReviewCreateView( LoginRequiredMixin, CreateView):
    model = Review
    fields = [ 'comment', 'rating']
    template_name = "blogs/review_create.html"
    success_url = reverse_lazy('blogs:blog-list')
     
    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        #form.instance.email = self.request.user.email
        form.instance.blog = Blog.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class ReplyToReviewCreateView(LoginRequiredMixin, CreateView):
    model = ReplyToReview
    #form_class = ReplyToReviewForm
    fields = [ 'comment']
    template_name = 'blogs/reply_create.html'
    success_url = reverse_lazy('blogs:blog-detail')

    def form_valid(self, form):
        form.instance.replier = self.request.user
        form.instance.review_id = Review.objects.get(pk=self.kwargs['review_id'])
        #form.instance.review = self.kwargs['review_id']
        
        return super().form_valid(form)

    #def get_success_url(self):
        #return reverse_lazy('blogs:review-detail', kwargs={'pk': self.kwargs['review_id']})
@login_required
def send_reply( request, review_id):
    review = get_object_or_404(Review, id=review_id)
    form = ReplyToReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replier= request.user
            reply.review = review
            reply.save()
            return redirect('blogs:blog-list')

    return render(request, 'blogs/reply_create.html', {'form': form, 'review': review})

class ReplyToReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = ReplyToReview
    form_class = ReplyToReviewForm
    template_name = 'blogs/reply_create.html'

    def get_success_url(self):
        return reverse_lazy('blogs:review-detail', kwargs={'pk': self.object.review_id})


class ReplyToReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = ReplyToReview
    template_name = 'replies/reply_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.review_id})
   

class BlogsSearchView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "blogs/blog_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Blog.objects.filter(
            
            Q(title__icontains=query)| 
            Q(email__icontains=query)|
            Q(author__icontains=query)|
            Q(categories__icontains=query)|
            Q(status__icontains=query) |
            Q(created_on__icontains=query)
        )
        return object_list   

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blogs/blog_categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_with_count'] = Category.objects.annotate(post_count=Count('blog')).filter(post_count__gt=0) 
        return context
@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    blogs = Blog.objects.filter(categories=category)
    return render(request, 'blogs/category_detail.html', {'category': category, 'blogs': blogs})



@login_required
def category_list(request):
    categories = Category.objects.all()
    #categories = Category.objects.annotate(num_blogs=Count('blog')).all().order_by('-num_blogs') 
    return render(request, 'blogs/blog_categories.html', {'categories': categories})

#### sending email upon blog creation #####
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Blog)  # assuming 'Blog' is your model
def send_email(sender, instance, **kwargs):
    # Define the recipient's email address
    recipient_email = "babala.assih@gmail.com"  # replace this with the actual recipient's email address

    # Create and send the email message
    email = EmailMessage(
        'New Blog Created',
        'Please check the creation of a new blog; it needs your approval',
        to=[recipient_email]  # Use the recipient's email address here
    )
    email.send()