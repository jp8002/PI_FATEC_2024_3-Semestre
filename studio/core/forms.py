from django import forms
from core.repositories.PersonalRepository import PersonalRepository
from core.services.ConexaoMongo import ConexaoMongo

class CadastrarAlunoForm(forms.Form):
    def listar_personal():
        serviceM = ConexaoMongo()
        serviceM._colecao = serviceM._mydb["personal"]
        repository = PersonalRepository(serviceM)
        
        personais = repository.listarTodos()
        print(personais)
        return [(str(p['nome']), p['nome']) for p in personais]

    def clean(self):
        cleaned_data = super().clean()
        ignorar = ['email','senha']
        for campo, valor in cleaned_data.items():
            if campo not in ignorar and isinstance(valor, str):
                cleaned_data[campo] = valor.title()

        return cleaned_data

    nome = forms.CharField(
        label='Nome Completo',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
        })
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'xxx.xxx.xxx-xx'
        })
    )

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control p-10'
            }
        )
    )

    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'exemplo@email.com'
        })
    )

    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
            'placeholder': 'xx.xxxxx-xxxx'
        })
    )

    plano = forms.CharField(
        label='Plano',
        widget=forms.TextInput(attrs={
            'class': 'form-control p-10',
        })
    )

    personal = forms.ChoiceField(
        choices=listar_personal,
        label='Personal Responsável',
        widget=forms.Select(attrs={
            'class': 'form-control p-7',
        })
    )

class CadastrarPersonalForm(forms.Form):
        nome = forms.CharField(label='Nome completo',
        max_length=255)

        cpf = forms.CharField(label='cpf',
        max_length=10)

        cref = forms.CharField(label='cref do personal',
        max_length=10)

        email = forms.EmailField(label='Email',
        )

        telefone = forms.CharField(label='telefone',
        max_length=11)

        senha = forms.CharField(label='senha',
        max_length=255)

        salario = forms.FloatField(label='salario')
        
        acesso = forms.ChoiceField(label='acesso', choices=[('adm','adm'),('funcionario','funcionario')])
        
        def clean_cpf(self):
            cpf = self.cleaned_data.get('cpf')
            cpf = cpf.replace('-','')
            cpf = cpf.replace('.','')
            
            return cpf
            

