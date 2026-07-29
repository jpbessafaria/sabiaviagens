from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dlogin
from django.contrib.auth.decorators import login_required
from .models import voo, companhia, hotel, quarto, cidades, aeroporto
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import AtualizarPerfil

def home(request):
    is_adm_geral = False
    is_adm_hotel = False
    is_adm_pass = False
    if request.user.is_authenticated:
        is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
        is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
        is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
    context = {
        'is_adm_geral': is_adm_geral,
        'is_adm_hotel': is_adm_hotel,
        'is_adm_pass': is_adm_pass,
    }
    return render(request, 'usuario/home.html', context)

def login(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        user = authenticate(request, username=cpf, password=senha)

        if user is not None:
            dlogin(request, user)
            if user.groups.filter(name='adm_geral').exists():
                return render(request, 'adm_geral/home_adm.html')
            elif user.groups.filter(name='adm_hotel').exists():
                return render(request, 'adm_hotel/home.html', {'success': 'Login realizado com sucesso'})
            elif user.groups.filter(name='adm_pass').exists():
                return render(request, 'adm_pass/home.html', {'success': 'Login realizado com sucesso'})  
            else:
                return render(request, 'usuario/home.html', {'success': 'Login realizado com sucesso'})          
        else:
            return render(request, 'usuario/login.html', {'error': 'Usuário ou senha inválidos'})
    else:
        return render(request, 'usuario/login.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'usuario/registro.html')
    else:
        name=request.POST.get('nome')   
        email=request.POST.get('email')
        cpf=request.POST.get('cpf')
        senha=request.POST.get('senha')

        user=User.objects.filter(username=cpf).first()

        if user:
            return render(request, 'usuario/registro.html', {'error': 'Já existe um usuário com esse CPF'})
        else:
            user = User.objects.create_user(username=cpf, email=email, password=senha, first_name=name)
            user.save()
            return render(request, 'usuario/registro.html', {'success': 'Usuário cadastrado com sucesso'})

def passagens(request):
    lista=voo.objects.all()
    is_adm_geral = False
    is_adm_hotel = False
    is_adm_pass = False
    if request.user.is_authenticated:
        is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
        is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
        is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
    context = {
        'is_adm_geral': is_adm_geral,
        'is_adm_hotel': is_adm_hotel,
        'is_adm_pass': is_adm_pass,
        'lista_voo': lista,
    }
    return render(request, 'usuario/passagens.html', context)

def hospedagens(request):
    is_adm_geral = False
    is_adm_hotel = False
    is_adm_pass = False
    lista = quarto.objects.all()
    if request.user.is_authenticated:
        is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
        is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
        is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
    context = {
        'lista_quartos': lista,
        'is_adm_geral': is_adm_geral,
        'is_adm_hotel': is_adm_hotel,
        'is_adm_pass': is_adm_pass,
    }
    return render(request, 'usuario/hospedagens.html', context)

def promocoes(request):
    is_adm_geral = False
    is_adm_hotel = False
    is_adm_pass = False
    if request.user.is_authenticated:
        is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
        is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
        is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
    context = {
        'is_adm_geral': is_adm_geral,
        'is_adm_hotel': is_adm_hotel,
        'is_adm_pass': is_adm_pass,
    }
    return render(request, 'usuario/promocoes.html', context)

def perfil(request):
    if request.method == 'POST':
        usuario = request.user

        usuario.first_name = request.POST.get('nome')
        usuario.username = request.POST.get('cpf')
        usuario.email = request.POST.get('email')
        usuario.save()  
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    else: 
        if request.user.is_authenticated:
            return render(request, 'usuario/perfil.html')
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa estar logado para acessar o perfil'})

def perfilvoo(request):
    if request.method == 'POST':
        usuario = request.user

        usuario.first_name = request.POST.get('nome')
        usuario.username = request.POST.get('cpf')
        usuario.email = request.POST.get('email')
        usuario.save()  
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    else: 
        if request.user.is_authenticated and (request.user.groups.filter(name='adm_pass').exists()):
            return render(request, 'adm_voo/perfil_voo.html')
        else:
            return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar o perfil de voo'})

def perfilhotel(request):
    if request.method == 'POST':
        usuario = request.user

        usuario.first_name = request.POST.get('nome')
        usuario.username = request.POST.get('cpf')
        usuario.email = request.POST.get('email')
        usuario.save()  
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    else: 
        if request.user.is_authenticated and (request.user.groups.filter(name='adm_hotel').exists()):
            return render(request, 'adm_hotel/perfil_hotel.html')
        else:
            return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar o perfil de hotel'})

def perfilgeral(request):
    if request.method == 'POST':
        usuario = request.user

        usuario.first_name = request.POST.get('nome')
        usuario.username = request.POST.get('cpf')
        usuario.email = request.POST.get('email')
        usuario.save()  
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    else: 
        if request.user.is_authenticated and (request.user.groups.filter(name='adm_geral').exists()):
            return render(request, 'adm_geral/perfil_geral.html')
        else:
            return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar o perfil de administração geral'})

def cadastro_hotel(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        endereco = request.POST.get('endereco')
        cidade_id = request.POST.get('cidade')
        imagem = request.POST.get('url')

        cidade = get_object_or_404(cidades, cod_cidade=cidade_id)

        hotel.objects.create(nome=nome, tipo=tipo, endereco=endereco, cod_cidade=cidade, imagem=imagem)
        return render(request, 'adm_geral/cadastro_hotel.html', {'success': 'Hotel cadastrado com sucesso'})
    else:
        lista = cidades.objects.all().order_by('nome')
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_cidades': lista,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_geral').exists():
            return render(request, 'adm_geral/cadastro_hotel.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de voo'})

def cadastro_quarto(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel')
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipo')
        preco = request.POST.get('preco')
        capacidade = request.POST.get('capacidade')

        hotel_obj = get_object_or_404(hotel, cod_hotel=hotel_id)

        quarto.objects.create(cod_hotel=hotel_obj, descricao=descricao, tipo=tipo, preco=preco, capacidade=capacidade)
        return render(request, 'adm_hotel/cadastro_quarto.html', {'success': 'Quarto cadastrado com sucesso'})
    else:
        lista = hotel.objects.all()
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_hoteis': lista,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_hotel'):
            return render(request, 'adm_hotel/cadastro_quarto.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de quarto'})

def cadastro_voo(request):
    if request.method == 'POST':
        companhia_id = request.POST.get('companhia')
        cid_origem_id = request.POST.get('cid_origem')
        cid_destino_id = request.POST.get('cid_destino')
        dt_hr_partida = request.POST.get('dt_hr_partida')
        dt_hr_chegada = request.POST.get('dt_hr_chegada')
        preco = request.POST.get('preco')
        ida_volta = request.POST.get('ida_volta') == 'on'
        promocao = request.POST.get('promocao') == 'on'
        capacidade = request.POST.get('capacidade')
        aeroporto_origem_id = request.POST.get('aero_origem')
        aeroporto_destino_id = request.POST.get('aero_destino')

        companhia_obj = get_object_or_404(companhia, cod_companhia=companhia_id)
        cid_origem_obj = get_object_or_404(cidades, cod_cidade=cid_origem_id)
        cid_destino_obj = get_object_or_404(cidades, cod_cidade=cid_destino_id)
        aeroporto_origem_obj = get_object_or_404(aeroporto, cod_aeroporto=aeroporto_origem_id)
        aeroporto_destino_obj = get_object_or_404(aeroporto, cod_aeroporto=aeroporto_destino_id)

        voo.objects.create(
            cod_companhia=companhia_obj,
            cod_cid_origem=cid_origem_obj,
            cod_cid_destino=cid_destino_obj,
            data_hora_partida=dt_hr_partida,
            data_hora_chegada=dt_hr_chegada,
            preco=preco,
            ida_volta=ida_volta,
            promocao=promocao,
            capacidade=capacidade,
            cod_aeroporto_origem=aeroporto_origem_obj,
            cod_aeroporto_destino=aeroporto_destino_obj
        )
        return render(request, 'adm_voo/cadastro_voo.html', {'success': 'Voo cadastrado com sucesso'})
    else:
        lista = companhia.objects.all()
        lista2 = cidades.objects.all()
        lista3 = aeroporto.objects.all()
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_companhias': lista,
            'lista_cidades': lista2,
            'lista_aeroportos': lista3,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_pass').exists():
            return render(request, 'adm_voo/cadastro_voo.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de voo'})                

def cadastro_companhia(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')

        companhia.objects.create(nome=nome, cnpj=cnpj)
        return render(request, 'adm_geral/cadastro_companhia.html', {'success': 'Companhia cadastrada com sucesso'})
    else:
        lista = companhia.objects.all()
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_companhia': lista,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_geral').exists():
            return render(request, 'adm_geral/cadastro_companhia.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de voo'})

def cadastro_cidades(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        estado = request.POST.get('estado')

        cidades.objects.create(nome=nome, estado=estado)
        return render(request, 'adm_geral/cadastro_cidades.html', {'success': 'Cidade cadastrada com sucesso'})
    else:    
        lista = cidades.objects.all()
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_cidades': lista,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_geral').exists():
            return render(request, 'adm_geral/cadastro_cidades.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de cidades'})

def cadastro_aeroportos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        cidade_id = request.POST.get('cidade')

        cidade = get_object_or_404(cidades, cod_cidade=cidade_id)

        aeroporto.objects.create(nome=nome, cep=cep, endereco=endereco, cod_cidade=cidade)
        return render(request, 'adm_geral/cadastro_aeroportos.html', {'success': 'Aeroporto cadastrado com sucesso'})

    else:    
        lista = cidades.objects.all()
        is_adm_geral = False
        is_adm_hotel = False
        is_adm_pass = False
        if request.user.is_authenticated:
            is_adm_geral = request.user.groups.filter(name='adm_geral').exists()
            is_adm_hotel = request.user.groups.filter(name='adm_hotel').exists()
            is_adm_pass = request.user.groups.filter(name='adm_pass').exists()
        context = {
            'lista_cidades': lista,
            'is_adm_geral': is_adm_geral,
            'is_adm_hotel': is_adm_hotel,
            'is_adm_pass': is_adm_pass,
        }
        if request.user.groups.filter(name='adm_geral').exists():
            return render(request, 'adm_geral/cadastro_aeroportos.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar o cadastro de aeroportos'})

def logout(request):
    from django.contrib.auth import logout as dlogout
    dlogout(request)
    return render(request, 'usuario/home.html', {'success': 'Logout realizado com sucesso'})

def homeadm(request):
    if request.user.is_authenticated and (request.user.groups.filter(name='adm_geral').exists()):
        return render(request, 'adm_geral/home_adm.html')
    else:
        return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar a página de administração'})

def homeadmhotel(request):
    if request.user.is_authenticated and (request.user.groups.filter(name='adm_hotel').exists()):
        return render(request, 'adm_hotel/home_adm_hotel.html')
    else:
        return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar a página de administração de hotéis'})

def homeadmvoo(request):
    if request.user.is_authenticated and (request.user.groups.filter(name='adm_pass').exists()):
        return render(request, 'adm_voo/home_adm_voo.html')
    else:
        return render(request, 'usuario/home.html', {'error': 'Você precisa ter permissão para acessar a página de administração de voos'})

def visualizar_hotel(request):
    if request.method == 'POST':
        id = request.POST.get('hotel_id')
        acao = request.POST.get('acao')

        if acao == 'deletar':
            hotel_obj = get_object_or_404(hotel, cod_hotel=id)
            hotel_obj.delete()
            messages.success(request, 'Hotel deletado com sucesso!')
            return redirect('visualizar_hotel')
    else:        
        if request.user.is_authenticated and (request.user.groups.filter(name='adm_geral').exists()):
            lista = hotel.objects.all().order_by('nome')
            context = {
                'lista_hotel': lista,
            }
            return render(request, 'adm_geral/visualizar_hotel.html', context)
        else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de hotéis'})

def visualizar_companhia(request):
    if request.method == 'POST':
        id = request.POST.get('companhia_id')
        acao = request.POST.get('acao')

        if acao == 'deletar':
            companhia_obj = get_object_or_404(companhia, cod_companhia=id)
            companhia_obj.delete()
            messages.success(request, 'Companhia deletada com sucesso!')
            return redirect('visualizar_companhia')
    else:
        if request.user.is_authenticated and (request.user.groups.filter(name="adm_geral").exists()):
            lista = companhia.objects.all().order_by('nome')
            context = {
                'lista_companhia': lista,
            }
            return render(request, 'adm_geral/visualizar_companhia.html', context)
        else:
                return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de Companhias'})

def visualizar_cidades(request):
    if request.method == 'POST':
        id = request.POST.get('cidade_id')
        acao = request.POST.get('acao')

        if acao == 'deletar':
            cidade_obj = get_object_or_404(cidades, cod_cidade=id)
            cidade_obj.delete()
            messages.success(request, 'Cidade deletada com sucesso!')
            return redirect('visualizar_cidades')
    else:
        if request.user.is_authenticated and (request.user.groups.filter(name="adm_geral").exists()):
            lista = cidades.objects.all().order_by('nome')
            context = {
                'lista_cidades': lista,
            }
            return render(request, 'adm_geral/visualizar_cidades.html', context)
        else:
                return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de cidades'})

def visualizar_aeroportos(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        acao = request.POST.get('acao')

        if acao == 'deletar':
            aeroporto_obj = get_object_or_404(aeroporto, cod_aeroporto=id)
            aeroporto_obj.delete()
            messages.success(request, 'Aeroporto deletado com sucesso!')
            return redirect('visualizar_aeroportos')
    else:
        if request.user.is_authenticated and (request.user.groups.filter(name="adm_geral").exists()):
            lista = aeroporto.objects.all().order_by('nome')
            context = {
                'lista_aeroportos': lista,
            }
            return render(request, 'adm_geral/visualizar_aeroportos.html', context)
        else:
                return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de aeroportos'})

def visualizar_quarto(request):
    if request.user.is_authenticated and (request.user.groups.filter(name="adm_hotel").exists()):
        lista_quartos = quarto.objects.all()
        context = {
            'lista_quartos': lista_quartos,
        }
        return render(request, 'adm_hotel/visualizar_quarto.html', context)
    else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de quartos'})

def visualizar_voo(request):
    if request.user.is_authenticated and (request.user.groups.filter(name="adm_pass").exists()):
        lista_voos = voo.objects.all()
        context = {
            'lista_voos': lista_voos,
        }
        return render(request, 'adm_voo/visualizar_voo.html', context)
    else:
            return render(request, 'usuario/login.html', {'error': 'Você precisa ter permissão para acessar a página de visualização de voos'})



