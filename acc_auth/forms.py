from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from acc_auth.models import MyUser
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
from django.urls import reverse
from crispy_forms.bootstrap import InlineField

class Date_input(forms.DateInput):
    input_type= 'date'

     
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')


# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'date_of_birth')
#         widgets={
#             "date_of_birth": Date_input(attrs={"class":'border-success border-opacity-25',}),
#         }

class LoginForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('email','password')
        widgets={
            "email": forms.EmailInput(attrs={"class":'border-success border-opacity-25',}),
            "password":forms.PasswordInput(attrs={"class":'border-success border-opacity-25',}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_class = 'd-flex form-inline bg-light mb-3 px-3 gap-4 justify-content-center flex-nowrap bg-primary'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('create_room')
        # self.helper.add_input(Submit('create', 'Submit'))
        self.helper.layout = Layout(
            InlineField('email'),
            InlineField('password'),
        )

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email,password=password):
                raise forms.ValidationError('invalid credentials')


"""
class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_class = 'd-flex form-inline bg-light mb-3 px-3 gap-4 justify-content-center flex-nowrap'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('create_room')
        self.helper.add_input(Submit('create', 'Submit'))
        self.helper.layout = Layout(
            InlineField('name'),
        )
"""