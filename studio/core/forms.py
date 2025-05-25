from django import forms
from django.core.validators import RegexValidator

class CadastrarAlunoForm(forms.Form):
    nome = forms.CharField(
        label='Nome Completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
        })
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'xxx.xxx.xxx-xx'
        })
    )

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control p-10'
            }
        )
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'exemplo@email.com'
        })
    )

    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'xx.xxxxx-xxxx'
        })
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control p-10',
        })
    )

    plano = forms.CharField(
        label='Plano',
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
        })
    )