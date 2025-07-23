# Guia Completo: Django CRUD com Class-Based Views

## Introdução: O que é CRUD?

CRUD significa **C**reate, **R**ead, **U**pdate, **D**elete - as quatro operações básicas que qualquer sistema precisa fazer com dados. É como um canivete suíço para manipular informações no banco de dados.

**Analogia**: Imagine um caderno de contatos:
- **Create**: Adicionar um novo contato
- **Read**: Consultar/listar contatos existentes  
- **Update**: Editar informações de um contato
- **Delete**: Remover um contato

## Por que usar Class-Based Views (CBVs)?

As CBVs são como "moldes pré-fabricados" que o Django oferece. Em vez de escrever todo o código do zero, você usa estruturas prontas e apenas personaliza o que precisa.

**Vantagens**:
- **Menos código**: Django já implementou a lógica básica
- **Reutilização**: Um template pode servir para Create e Update
- **Padronização**: Estrutura consistente em todo o projeto
- **Manutenibilidade**: Mais fácil de manter e expandir

## Estrutura do Projeto

### 1. Models (models.py) - A Fundação

```python
from django.db import models
from django.urls import reverse

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="Email")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    ativo = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('pessoa_list')
```

**Por que usar `get_absolute_url()`?**
- Define para onde redirecionar após operações de Create/Update
- Centraliza a lógica de redirecionamento
- Facilita manutenção (se mudar a URL, muda só aqui)

### 2. Forms (forms.py) - A Validação

```python
from django import forms
from .models import Pessoa

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'email', 'data_nascimento', 'ativo', 'observacoes']
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre a pessoa'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Validação personalizada para email único
        if self.instance.pk:  # Editando registro existente
            if Pessoa.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError("Este email já está em uso!")
        else:  # Criando novo registro
            if Pessoa.objects.filter(email=email).exists():
                raise forms.ValidationError("Este email já está em uso!")
        
        return email
```

**Por que usar ModelForm?**
- Gera campos automaticamente baseado no modelo
- Validações automáticas (email válido, campos obrigatórios)
- Integração perfeita com CBVs

### 3. Views (views.py) - A Lógica de Negócio

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pessoa
from .forms import PessoaForm

class PessoaListView(ListView):
    model = Pessoa
    template_name = 'myapp/pessoa_list.html'
    context_object_name = 'pessoas'

class PessoaCreateView(CreateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'myapp/base_form.html'
    success_url = reverse_lazy('pessoa_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nova Pessoa'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Pessoa criada com sucesso!')
        return super().form_valid(form)

class PessoaUpdateView(UpdateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'myapp/base_form.html'  # MESMO template que Create!
    success_url = reverse_lazy('pessoa_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar: {self.object.nome}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Pessoa atualizada com sucesso!')
        return super().form_valid(form)

class PessoaDeleteView(DeleteView):
    model = Pessoa
    template_name = 'myapp/pessoa_confirm_delete.html'
    success_url = reverse_lazy('pessoa_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pessoa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
```

**Pontos Importantes**:
- **CreateView e UpdateView usam o MESMO template** (`base_form.html`)
- **reverse_lazy**: Usado porque as URLs ainda não foram carregadas quando a classe é definida
- **get_context_data**: Adiciona dados extras para o template
- **form_valid**: Executado quando o formulário é válido

### 4. URLs (urls.py) - As Rotas

```python
from django.urls import path
from . import views

urlpatterns = [
    path('pessoas/', views.PessoaListView.as_view(), name='pessoa_list'),
    path('pessoas/nova/', views.PessoaCreateView.as_view(), name='pessoa_create'),
    path('pessoas/<int:pk>/editar/', views.PessoaUpdateView.as_view(), name='pessoa_update'),
    path('pessoas/<int:pk>/excluir/', views.PessoaDeleteView.as_view(), name='pessoa_delete'),
]
```

**Padrão de URLs**:
- Lista: `/pessoas/`
- Criar: `/pessoas/nova/`
- Editar: `/pessoas/{id}/editar/`
- Excluir: `/pessoas/{id}/excluir/`

## O Segredo: base_form.html Reutilizável

Este é o template **inteligente** que serve tanto para Create quanto Update:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            
            <h1 class="text-center mb-4">{{ titulo }}</h1>
            
            {% if form.errors %}
                <div class="alert alert-danger">
                    <h5>Corrija os erros abaixo:</h5>
                    {% for field, errors in form.errors.items %}
                        <p><strong>{{ field }}:</strong> {{ errors.0 }}</p>
                    {% endfor %}
                </div>
            {% endif %}
            
            <form method="post">
                {% csrf_token %}
                
                <div class="row g-4">
                    
                    <div class="col-12">
                        <div class="form-floating">
                            {{ form.nome }}
                            <label for="{{ form.nome.id_for_label }}">{{ form.nome.label }}</label>
                        </div>
                    </div>
                    
                    <div class="col-12">
                        <div class="form-floating">
                            {{ form.email }}
                            <label for="{{ form.email.id_for_label }}">{{ form.email.label }}</label>
                        </div>
                    </div>
                    
                    <div class="col-12">
                        <div class="form-floating">
                            {{ form.data_nascimento }}
                            <label for="{{ form.data_nascimento.id_for_label }}">{{ form.data_nascimento.label }}</label>
                        </div>
                    </div>
                    
                    <div class="col-12">
                        <div class="form-check">
                            {{ form.ativo }}
                            <label class="form-check-label" for="{{ form.ativo.id_for_label }}">
                                {{ form.ativo.label }}
                            </label>
                        </div>
                    </div>
                    
                    <div class="col-12">
                        <div class="form-floating">
                            {{ form.observacoes }}
                            <label for="{{ form.observacoes.id_for_label }}">{{ form.observacoes.label }}</label>
                        </div>
                    </div>
                    
                    <div class="col-12 text-center">
                        <button type="submit" class="btn btn-primary px-5">
                            {% if object %}Atualizar{% else %}Criar{% endif %}
                        </button>
                        <a href="{% url 'pessoa_list' %}" class="btn btn-secondary px-5 ms-2">
                            Cancelar
                        </a>
                    </div>
                    
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### Como o Template Diferencia Create vs Update?

**A Mágica está na variável `object`**:

```html
{% if object %}Atualizar{% else %}Criar{% endif %}
```

**Quando é Create**:
- `object` = None (não existe ainda)
- Título: "Nova Pessoa"
- Botão: "Criar"
- Campos vazios

**Quando é Update**:
- `object` = instância da Pessoa existente
- Título: "Editar: João Silva"
- Botão: "Atualizar"
- Campos preenchidos com dados atuais

## Templates Complementares

### Lista (pessoa_list.html)

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Lista de Pessoas</h1>
        <a href="{% url 'pessoa_create' %}" class="btn btn-primary">Nova Pessoa</a>
    </div>
    
    <div class="row">
        {% for pessoa in pessoas %}
        <div class="col-md-6 col-lg-4 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ pessoa.nome }}</h5>
                    <p class="card-text">{{ pessoa.email }}</p>
                    <div class="btn-group" role="group">
                        <a href="{% url 'pessoa_update' pessoa.pk %}" class="btn btn-sm btn-warning">Editar</a>
                        <a href="{% url 'pessoa_delete' pessoa.pk %}" class="btn btn-sm btn-danger">Excluir</a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### Confirmação de Exclusão (pessoa_confirm_delete.html)

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h3>Confirmar Exclusão</h3>
                    <p>Tem certeza que deseja excluir <strong>{{ object.nome }}</strong>?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-danger me-2">Sim, Excluir</button>
                        <a href="{% url 'pessoa_list' %}" class="btn btn-secondary">Cancelar</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Implementação Passo a Passo

### 1. Preparar o Ambiente

```bash
# Criar e aplicar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser
```

### 2. Estrutura de Arquivos

```
myapp/
├── models.py
├── forms.py
├── views.py
├── urls.py
└── templates/
    └── myapp/
        ├── base_form.html
        ├── pessoa_list.html
        └── pessoa_confirm_delete.html
```

### 3. URLs Principais Disponíveis

- **`/pessoas/`** → Lista todas as pessoas
- **`/pessoas/nova/`** → Formulário para criar nova pessoa
- **`/pessoas/1/editar/`** → Formulário para editar pessoa com ID 1
- **`/pessoas/1/excluir/`** → Confirmação para excluir pessoa com ID 1

## Vantagens desta Abordagem

### 1. **DRY (Don't Repeat Yourself)**
- Um template serve para Create e Update
- Código reutilizável e maintível

### 2. **Consistência**
- Mesma aparência para criar e editar
- Padrão uniforme em todo o sistema

### 3. **Facilidade de Manutenção**
- Alterar o layout? Só um arquivo
- Adicionar campo? Só no form e template

### 4. **Escalabilidade**
- Fácil adicionar novos modelos
- Padrão replicável

## Dicas Avançadas

### 1. Adicionando Validação Ajax
```javascript
// No template base_form.html
<script>
$('#id_email').on('blur', function() {
    // Validar email via Ajax
});
</script>
```

### 2. Campos Condicionais
```html
{% if user.is_staff %}
    <div class="col-12">
        {{ form.campo_admin }}
    </div>
{% endif %}
```

### 3. Formulários com Múltiplos Modelos
```python
class PessoaUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['endereco_form'] = EnderecoForm(instance=self.object.endereco)
        return context
```

## Conclusão

O `base_form.html` é uma solução elegante que:

- **Reduz duplicação** de código
- **Padroniza** a interface
- **Facilita manutenção**
- **Acelera desenvolvimento**

Esta abordagem demonstra o poder do Django em criar sistemas robustos com menos código, seguindo princípios de engenharia de software como DRY e separação de responsabilidades.

**Lembre-se**: A chave está em entender que CreateView e UpdateView são diferentes operações que podem compartilhar a mesma apresentação visual, diferenciando-se apenas no contexto e comportamento.