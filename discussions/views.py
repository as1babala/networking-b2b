from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum, Avg
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail

from core.models import *
from .forms import *
from rfi.forms import *


class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee

class ForumListView(LoginRequiredMixin, generic.ListView):
    template_name = "discussions/forum_list.html"
    queryset = Forum.objects.filter(active=True) # for published blogs
    context_object_name = "forums"
    paginate_by = 4
    
class UserForumListView(LoginRequiredMixin, generic.ListView):
    template_name = "discussions/forum_user_list.html"
    context_object_name = "user_forums"
    
    def get_queryset(self):
        return Forum.objects.filter(forum_creator=self.request.user).order_by('-created_on')

class ForumCreateView(LoginRequiredMixin, CreateView):
    template_name = "discussions/forum_create.html"
    form_class = ForumForm
    success_url = reverse_lazy('discussions:forum-list')
    
     
    def form_valid(self, form):
        form.instance.forum_creator = self.request.user
        form.instance.creator_email = self.request.user.email
        messages.success(self.request, f'Your account has been created! You are now able to log in')
            
        return super().form_valid(form)

 
class ForumDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "discussions/forum_detail.html"
    queryset = Forum.objects.all() # not adding context here
    context_object_name = "forums"
    
     
def forum_detail(request, pk):
    forum = Forum.objects.get(pk=pk)
    form = DiscussionForm()
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = Discussion(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["content"],
                forum=forum
            )
            discussion.save()

    discussions = Discussion.objects.filter(forum=forum)
    context = {
        "forum": forum,
        "discussions": discussions,
        "form": form,
 
    }

    return render(request, "discussions/forum_detail.html", context)


class ForumUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "discussions/forum_update.html"
    form_class = ForumForm
    queryset = Forum.objects.all()
    
    def get_success_url(self):
        return reverse("discussions:forum-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ForumUpdateView, self).form_valid(form)
 
class ForumDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "discussions/forum_delete.html"
    queryset = Forum.objects.all()
    context_object_name = "delete_forum"
    
    def get_success_url(self):
        return reverse("discussion:forum-list")


class DiscussionsCreateView( LoginRequiredMixin, CreateView):
    model = Discussion
    fields = [ 'discuss']
    template_name = "discussions/discussion_create.html"
    success_url = reverse_lazy('discussions:forum-list')
     
    def form_valid(self, form):
        form.instance.discussion_creator = self.request.user
        form.instance.discussion_email = self.request.user.email
        form.instance.forum = Forum.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

 

@login_required
def Forum_List_View(request):
    forums=Forum.objects.all()
    
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,"forum/forum_list.html",context)


@login_required
def Create_Discussion_View(request):
    form = DiscussionForm()
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("discussions/forum_list.html")
    context ={'form':form}
    return render(request,"discussions/discussion_create.html",context)

   
    
    
class ForumsSearchView(ListView):
    model = Forum
    template_name = "discussions/forum_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Forum.objects.filter(
            
            #Q(dealer__icontains=query)| 
            Q(forum_creator__icontains=query)  |
            Q(creator_email__icontains=query) |
            Q(topic__icontains=query)|
            Q(active__icontains=query) |
            Q(created_on__icontains=query)
        )
        return object_list   
    
     
    