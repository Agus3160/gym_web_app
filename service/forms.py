from .models import User, ClientInfo
from django.forms import ModelForm, EmailInput, CharField, PasswordInput, TextInput, Select, Form, EmailField, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

class LoginForm(Form):
  email = EmailField(max_length=255, label='Email', widget=EmailInput(attrs={'placeholder': 'example@example.com', 'class': 'form-control'}))
  password = CharField(label='Password', widget=PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))

class UserSignUpForm(UserCreationForm):
    
    password1 = CharField(label='Password', widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = CharField(label='Confirm Password', widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))
    group = ModelChoiceField(queryset=Group.objects.all(), label='Group', empty_label=None, widget=Select(attrs={'class': 'form-select'}))

    class Meta:
      model = User
      fields = ['email', 'first_name', 'last_name', 'group']
      widgets = {
      'email': TextInput(attrs={'placeholder': 'example@example.com', 'class': 'form-control'}),
      'first_name': TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}),
      'last_name': TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}),
    }

    def clean_group(self):
      group = self.cleaned_data.get('group')
      if not group or group == "":
        raise ValidationError('Please select a valid role.')
      return group

    def clean_password2(self):
      password1 = self.cleaned_data.get("password1")
      password2 = self.cleaned_data.get("password2")
      if not password1 or not password2 or password1 != password2:
        raise ValidationError("Passwords don't match")
      return password2

    def save(self, commit=True):
      user = super().save(commit=False)
      user.set_password(self.cleaned_data["password1"])
      if commit:
        user.save()
      return user
    
class ClientInfoForm(ModelForm):

   # Define widths for each field
  field_widths = {
    'username': 4,
    'email': 4,
    'password': 4,
    'full_name': 6,
    'bio': 6,
  }

  class Meta:
    model = ClientInfo
    fields = ['gender', 'birth_date', 'height', 'ci', 'weight', 'address', 'phone', 'emergency_contact']
    widgets = {
      'gender': Select(attrs={'class': 'form-select'}),
      'birth_date': TextInput(attrs={'class': 'form-control', 'type': 'date'}),
      'height': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height'}),
      'ci': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your CI'}),
      'weight': TextInput(attrs={'min':0,'type': 'number', 'class': 'form-control', 'placeholder': 'Enter your weight'}),
      'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'min': 0}),
      'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone'}),
      'emergency_contact': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your emergency contact'}),
    }
    labels = {
      'weight': 'Weight (kg)',  
      'height': 'Height (cm)',
      'ci': 'CI',
    }

  def clean_height(self):
    height = self.cleaned_data.get('height')
    if height <= 0 or not height:
      raise ValidationError('Height must be greater than 0')
    return height
  
  def clean_weight(self):
    weight = self.cleaned_data.get('weight')
    if weight <= 0 or not weight:
      raise ValidationError('Weight must be greater than 0')
    return weight