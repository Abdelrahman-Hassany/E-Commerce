from django import forms
from django.contrib.auth import get_user_model
from .models import Customer,Seller

User = get_user_model()
class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        label="Enter Your name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    user_type = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('seller', 'Seller')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password', 'password_confirm']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    # To ensure that the password matches 
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError('Your Password Does Not Match!')
        return cleaned_data
    
    # To ensure hashing password and choice account type
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        user_type = self.cleaned_data['user_type']
        
        if user_type == 'customer':
            user.is_customer = True
        elif user_type == 'seller':
            user.is_seller = True

        if commit:
            user.save()
            if user.is_customer:
                Customer.objects.create(user=user,
                                        name =self.cleaned_data['name'])
            if user.is_seller:
                Seller.objects.create(user=user,
                                      name =self.cleaned_data['name'])
        return user

    
    
        
