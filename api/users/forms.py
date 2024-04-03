from django import forms

print(dir(forms))

class UpdateProfileForm(forms.Form):
  #  name = forms.IntegerField(validators=[validate_even])
 #   username = forms.IntegerField(validators=[validate_even])
    email = forms.EmailField()
  #  avatar = forms.IntegerField(validators=[validate_even])
    