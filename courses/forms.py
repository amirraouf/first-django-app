from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.utils.translation import ugettext_lazy as _


class Course(forms.ModelForm):
    class Meta:
        model = Course_dir
        fields = ['name', 'no_hours', 'no_seats', 'description','price',
                  'certification', 'type_of_degree', 'date', 'time', 'availability',
                  'instructor']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class login_form(forms.Form):
    class Meta:
        model = Person
        fields = ['username','password']


class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label="Username", error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")
        })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      max_length=30,
                                                                      render_value=False)),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      max_length=30,
                                                                      render_value=False)),
                                label=_("Password (again)"))

    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True,
                                                                       max_length=30,
                                                                       render_value=False
                                                                       )
                                                            ),
                                 label=_("First Name")
                                 )
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True,
                                                                      max_length=30,
                                                                      render_value=False)),
                                label=_("Last Name"))

    def clean_username(self):
        try:
            user = Person.objects.get(username__iexact=self.cleaned_data['username'])
        except Person.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

#
# class UserForm(UserCreationForm):
#     age = forms.IntegerField()
#     mobile = forms.CharField()
#     avatar = forms.ImageField()
#     is_training_center = forms.BooleanField()
#     is_instructor = forms.BooleanField()
#
#     def save(self, commit=True):
#         user = super(UserForm, self).save(commit=False)
#
#         if commit:
#             user.save()
#
#             if self.cleaned_data.get('is_training_center'):
#                 Training_Center.objects.create(Person=Person)
#
#             if self.cleaned_data.get('is_instructor'):
#                 Instructor.objects.create(Person=Person)
#
#         return user





class Instructor_profile(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['age', 'mobile', 'img']


class User_profile(forms.ModelForm):
    class Meta:
        model = Go_User
        fields = ['age', 'mobile', 'img']


class Training_center_profile(forms.ModelForm):
    class Meta:
        model = Training_Center
        fields = ['training_center_name', 'address', 'logo']


class courses(forms.ModelForm):
    class Meta:
        model = Course_dir
        fields = '__all__'