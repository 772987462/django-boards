from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from .forms import NewTopicForm
from .models import Board,Topic,Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Count
from django.views.generic import View
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



#FBV分页
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user=User.objects.first() #TODO get the currently logged in user

    if request.method == 'POST':
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            #topic.starter=user
            topic.starter=request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user)
            return redirect('topic_posts', pk=pk,topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form=NewTopicForm()
    return render(request, 'new_topic.html', {'board': board,'form':form})

def topic_posts(request,pk,topic_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    topic.views +=1
    topic.save()
    return render(request,'topic_posts.html',{'topic':topic})

@login_required
def reply_topic(request,pk,topic_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()
            topic.last_updated=timezone.now()
            topic.save()
            return redirect('topic_posts',pk=pk,topic_pk=topic_pk)
    else:
        form=PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})

#基于函数的视图
def new_post(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        else:
            form=PostForm()
        return render(request,'new_post.html',{'form':form})

class NewPostView(View):
    def render(self, request):
        return render(request, 'new_post.html', {'form': self.form})

    def post(self, request):
        self.form = PostForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            return redirect('post_list')
        return self.render(request)

    def get(self, request):
        self.form = PostForm()
        return self.render(request)

#编辑帖子视图
@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    def form_invalid(self, form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        post.save()
        return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)

