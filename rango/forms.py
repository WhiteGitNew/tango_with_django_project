from django import forms, views
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User
from rango.models import UserProfile

class CategoryForm(forms.ModelForm):
    # name = forms.CharField(max_length=128,
    #                        help_text="Please enter the category name.")
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # 给form提供额外信息的内部类
    class Meta:
        #提供ModelForm和Model之间的关联
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    # title = forms.CharField(max_length=128,
    #                         help_text="Please enter the title of the page.")
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        
        #可以选择在form中包含的fields，用exclude去除某个filed,他允许NULL值
        exclude = ('category',)
        #或者include某个filed
        #fields = ('title', 'url', 'views')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email','password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)