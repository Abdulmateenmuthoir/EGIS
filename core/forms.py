from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Cabinet, Phase, File


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter email address',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter password',
        })
    )


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cabinet Name or Tag',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add Cabinet Description',
                'rows': 3,
            }),
        }


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = ['name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phase name (e.g., Phase 1)',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Order (e.g., 1)',
                'min': 0,
            }),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'cabinet', 'phase', 'file_name', 'file_number',
            'volume', 'comment', 'document_image', 'status', 'custom_status'
        ]
        widgets = {
            'cabinet': forms.Select(attrs={'class': 'form-input'}),
            'phase': forms.Select(attrs={'class': 'form-input'}),
            'file_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'File Name',
            }),
            'file_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'File Number',
                'autocomplete': 'off',
            }),
            'volume': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Volume',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add Comment',
                'rows': 3,
            }),
            'document_image': forms.ClearableFileInput(attrs={
                'class': 'form-input file-input',
                'accept': 'image/*',
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'custom_status': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter custom status...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phase'].required = False
        self.fields['phase'].queryset = Phase.objects.none()
        self.fields['document_image'].required = False
        self.fields['custom_status'].required = False
        self.fields['volume'].required = False
        self.fields['comment'].required = False

        if 'cabinet' in self.data:
            try:
                cabinet_id = int(self.data.get('cabinet'))
                self.fields['phase'].queryset = Phase.objects.filter(
                    cabinet_id=cabinet_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.cabinet_id:
            self.fields['phase'].queryset = Phase.objects.filter(
                cabinet=self.instance.cabinet
            )

    def clean_file_number(self):
        file_number = self.cleaned_data.get('file_number')
        if file_number:
            qs = File.objects.filter(file_number=file_number, is_deleted=False)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('This file number already exists.')
        return file_number


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        }),
        required=True,
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email address',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Last name',
            }),
            'role': forms.Select(attrs={'class': 'form-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
