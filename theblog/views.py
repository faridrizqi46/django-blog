from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, base
from .models import Post, Category, Comment, coba
from .forms import PostForm, UpdatePostForm, CommentForm, cobaform
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin 

# def home(request):
#     return render(request, 'home.html', {})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name ='home.html'
    ordering = ['-post_date','-id']
    
    #ordering = ['-id']
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context
    
    # def get_category(self):
    #     cat_menu_lists = Category.objects.all()
    #     return cat_menu_lists
    #     return render(request, 'home.html', {'cat_menu_lists':cat_menu_lists})

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})

    
def CategoryView(request, cats):
    category_post = Post.objects.filter(category=cats.title().replace('-',' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-',' '), 'category_post':category_post})
    

class ArticleDetailView(FormMixin,DetailView):
    model = Post
    template_name = 'article_details.html'
    form_class = CommentForm
    slug_field = 'slug'
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        new_post = Post.objects.all().order_by('-id')[:5]
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id = self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context['liked'] = liked
        context['new_post'] = new_post
        context['form'] = CommentForm(initial={'post': self.object.pk})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    
    def form_valid(self, form):
        post = self.get_object()
        myform = form.save(commit=False)
        myform.post =  post
        form.save()
        return super(ArticleDetailView, self).form_valid(form)
    
    def get_success_url(self,**kwargs):
        return reverse('article-detail', kwargs={'pk':self.object.pk})
    
    # def new_post(self,request):
    #     new_post = Post.object.all()
    #     return {'newerpost':new_post}
    
class AddPostView(CreateView):
    model = Post
    form_class = PostForm #Ini hampir sama kek yg fields cuma ini dipanggil di forms.py dan dikasih classnya disitu biar langsung ada cssnya
    #Jadi klo udah pake yg ini yg field gk usah dipake
    template_name = 'add_post.html'
    #fields = '__all__' #Ini buat nampilin form apa aja yg muncul , disini all yng berarti semua form dari models.py akan muncul
    #Klo mau nampilin hanya beberapa aja -> fields = ('title','body') -> misalnya begitu
    
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    def get_post_id(self):
        postid = self.kwargs['pk'] 
        return postid
    #fields = '__all__'
    def form_valid(self,form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = "/article/{post_id}"
    #success_url = reverse_lazy('article' ,kwargs={'pk': get_post_id()})

### Area Terlarang ###
# class PostCommentView(base.View):
#     def get(self, request, *args, **kwargs):
#         view = ArticleDetailView.as_view()
#         return view(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs) :
#         view = AddCommentView.as_view()
#         return view(request, *args, **kwargs)


# def postcomentdetail(request, slug):
#     template_name = "article_details.html"
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments
#     new_comment = None
#     # Comment posted
#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():

#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     return render(
#         request,
#         template_name,
#         {
#             "post": post,
#             "comments": comments,
#             "new_comment": new_comment,
#             "comment_form": comment_form,
#         },
#     )
### Area Terlarang ###  

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name ='update_post.html'
    #fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name ='delete_post.html'
    success_url = reverse_lazy('home')

class TestMCEView(CreateView):
    model = coba
    form_class = cobaform
    template_name = 'test_mce.html'
    success_url = reverse_lazy('home')