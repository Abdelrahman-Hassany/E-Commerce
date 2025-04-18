from django import forms
from .models import Product

class UploadProduct(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','price','image','digital','slug']
        
    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product