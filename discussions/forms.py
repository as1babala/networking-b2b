from django.forms import ModelForm
from core.models import *
 
class ForumForm(ModelForm):
    class Meta:
        model= Forum
        exclude = [ 'id','slug', 'forum_creator', 'creator_email', 'active']
 
class DiscussionForm(ModelForm):
    class Meta:
        model= Discussion
        exclude = [ 'id','slug', 'discussion_creator', 'discussion_email', 'forum']