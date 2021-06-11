from django import forms
from .models import Post, Category, Comment,coba

#choice = [('Machine Learning', 'Machine Learning'),('Sport', 'Sport'),('Data Science', 'Data Science'),('Other', 'Other')]
choice = Category.objects.all().values_list('name', 'name')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','title_tag','author','category','header_image','body','snippet')
        
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title Here'}),
            'title_tag' : forms.TextInput(attrs={'class': 'form-control'}),
            'author' : forms.TextInput(attrs={'class': 'form-control','value':'','id':'user','type':'hidden'}),
            #'author' : forms.Select(attrs={'class': 'form-control'}),
            'category' : forms.Select(choices=choice,attrs={'class': 'form-control'}),
            'body' : forms.Textarea(attrs={'id':'full-featured-non-premium'}),
            'snippet' : forms.Textarea(attrs={'class': 'form-control'}),
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','title_tag','category','body','snippet')
        
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title Here'}),
            'title_tag' : forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(choices=choice,attrs={'class': 'form-control'}),
            'body' : forms.Textarea(attrs={'id':'full-featured-non-premium'}),
            'snippet' : forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','body')
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your Name Here'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
        }

class cobaform(forms.ModelForm):
    class Meta:
        model = coba
        fields = ('testmce',)
        
        widgets = {
            'testmce' : forms.Textarea(attrs={'id':'full-featured-non-premium'})
        }