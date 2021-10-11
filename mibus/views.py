from django.http.response import HttpResponse
from .forms import CreateUserForm
from ipware import get_client_ip
from validate_email import validate_email
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from citymngmt.models import City, Company, ClientUser, CompanyRelations, Line, CitySession, BusStops
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .modules.extractors import extractLineRoute, extractBusStops, extractAndUpdate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
import requests

def closeSession(request):
    from ipware import get_client_ip
    from passlib.hash import pbkdf2_sha256
    #pbkdf2_sha256.verify(password, _company.password)
    client_ip, is_routable = get_client_ip(request)
    
    #Delete after testing
    #if is_routable:
    if not is_routable:
        # The client's IP address is publicly routable on the Internet
        try:
            _citySessions = CitySession.objects.filter(user_id=request.user.id)
            for session in _citySessions:
                if pbkdf2_sha256.verify(client_ip ,session.ip):
                    session.status = False
                    session.save()
        except:
            client_ip = pbkdf2_sha256.hash(client_ip)
            _citySession = CitySession(user_id=request.user.id, ip=client_ip)
            _citySession.save()

def register_view(request):
    closeSession(request)
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        form = CreateUserForm()
        context = {'has_error': False, 'form': form, 'data': request.POST, 'password_error': False, 'username_error': False}

        if request.method == 'POST':
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']
            password2 = request.POST['password2']


            if len(username) < 6:
                messages.add_message(request, messages.ERROR, 'El usuario debe tener al menos 6 caracteres')
                context['has_error'] = True
                context['username_error'] = True
            if len(username) > 20:
                messages.add_message(request, messages.ERROR, 'El usuario debe tener menos de 20 caracteres')
                context['has_error'] = True
                context['username_error'] = True

            if len(password) < 6:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña debe tener al menos 6 caracteres')
                context['has_error'] = True
            if password != password2:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                context['has_error'] = True
            if User.objects.filter(email=email).exists():
                context['has_error'] = True
                messages.add_message(request, messages.ERROR, 'El email ya esta registrado')
            if not validate_email(email):
                messages.add_message(request, messages.ERROR, 'El email no es válido')
                context['has_error'] = True
            if User.objects.filter(username=username).exists():
                context['username_error'] = True
                messages.add_message(request, messages.ERROR, 'El usuario ya existe')
                context['has_error'] = True
            if not username:
                messages.add_message(request, messages.ERROR, 'El nombre de usuario no puede estar vacío')
                context['has_error'] = True
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'El nombre de usuario ya existe')
                context['has_error'] = True
            if context['has_error']:
                return render(request, 'register.html', context)
            
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                userIsCity = ClientUser(isCity=True, user_id=User.objects.get(username=username).id)      
                userIsCity.save()
                messages.add_message(request, messages.SUCCESS, 'Usuario creado exitosamente')

        return render(request, 'register.html', context)


def login_view(request):
    closeSession(request)
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        if request.method == 'POST':
            context = {'has_error': False,'data': request.POST}
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                id = request.user.id
                _clientUser = ClientUser.objects.get(user_id=id)
                if not _clientUser.isCity:
                    try:
                        Company.objects.get(user_id=id)
                        return redirect('/main')
                    except:
                        comp = Company(username=username, user_id=id)
                        comp.save()
                        return redirect('/main')
                else:
                    try:
                        City.objects.get(user_id=id)
                        return redirect('/main')
                    except:
                        obj = City(user_id=id)
                        obj.save()
                        return redirect('/main')
            else:
                messages.error(request, 'Usuario o contraseña invalido')
                return render(request, 'login.html', context)

        return render(request, 'login.html')

def logout_view(request):
    closeSession(request)
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def main_view(request):
    closeSession(request)
    id = request.user.id
    _clientUser = ClientUser.objects.get(user_id=id)
    if not _clientUser.isCity:
        return redirect('/main-company')
    context= {'status': False, 'activated': False, 'user_id': 0}
    _city = City.objects.get(user_id=id)
    status = _city.status
    activated = _city.activated
    id = _city.user_id
    context['status'] = status
    context['activated'] = activated
    context['user_id'] = id
    return render(request, 'main-hub.html', context)

@login_required(login_url='/login')
def edit_city_view(request, id):
    closeSession(request)
    from bs4 import BeautifulSoup as bs
    if request.user.id == id:
        id = request.user.id
        _clientUser = ClientUser.objects.get(user_id=id)
        if not _clientUser.isCity:
            return redirect('/main-company')
        city = City.objects.get(user_id=id)
        context = {'city': city, 'name_error': False, 'has_error': False}
        if request.method == 'POST':
            name = request.POST['city_name']
            emergency_phone = request.POST['emergency_phone']
            ticket_price = request.POST['ticket_price']
            try:
                img_url = request.FILES['img_url']
                city.image = img_url
            except:
                pass
            try:
                muni_url = request.FILES['muni_url']
                city.municipality_image = muni_url
            except:
                pass
            try:
                polygon = request.FILES['polygon']
                try:
                    soup = bs(polygon,'lxml')
                    coordinates = soup.find("coordinates")
                    coordinates = coordinates.text.split('\n')
                    full_list = []
                    for elements in coordinates:
                        cache_list = []
                        elements = elements.split(',')
                        elements[0].strip()
                        for element in elements:
                            cache_list.append(element.lstrip())
                        try:
                            cache_list[0], cache_list[1] = cache_list[1], cache_list[0]
                            full_list.append((float(cache_list[0]), float(cache_list[1])))
                        except:
                            pass
                    city.polygon = full_list
                except:
                    messages.add_message(request, messages.ERROR, 'Tipo de archivo incorrecto')
                    context['has_error'] = True
            except:
                pass
            
            status = request.POST['status']
            if status == 'true':
                status = True
            else:
                status = False

            if len(name) < 6:
                messages.add_message(request, messages.ERROR, 'La ciudad debe tener al menos 6 caracteres')
                context['has_error'] = True
                context['name_error'] = True
            if len(name) > 25:
                messages.add_message(request, messages.ERROR, 'La ciudad debe tener menos de 25 caracteres')
                context['has_error'] = True
                context['name_error'] = True
            
            if context['has_error']:
                return render(request, 'edit-city.html', context)
            
            city.emergency_phone = emergency_phone
            city.ticket_price = ticket_price
            city.name = name
            city.status = status
            city.save()
            messages.add_message(request, messages.SUCCESS, 'Ciudad editada exitosamente')
        return render(request, 'edit-city.html', context)
    else:
        return redirect('/main')

@login_required(login_url='/login')
def edit_companies_view(request, id):
    closeSession(request)
    from passlib.hash import pbkdf2_sha256
    if request.user.id == id:
        _companies = []
        id = request.user.id
        _clientUser = ClientUser.objects.get(user_id=id)
        if not _clientUser.isCity:
            return redirect('/main-company')
        _city = City.objects.get(user_id=id)
        _relations = CompanyRelations.objects.filter(client_id=_clientUser.id)
        for relation in _relations:
            _company_ = Company.objects.get(id=relation.company_id)
            _company_.relation_id = relation.id
            _companies.append(_company_)
        context = {'has_companies': True,'companies': _companies, 'city': _city}
        if len(_companies) == 0:
            context['has_companies'] = False
        return render(request, 'edit-companies.html', context)
    return redirect('/main')

@login_required(login_url='/login')
def add_companies_view(request, id):
    closeSession(request)
    from passlib.hash import pbkdf2_sha256
    if request.user.id == id:
        id = request.user.id
        _clientUser = ClientUser.objects.get(user_id=id)
        if not _clientUser.isCity:
            return redirect('/main-company')
        _city = City.objects.get(user_id=id)
        relationships = CompanyRelations.objects.filter(client_id=_clientUser.id)
        companies = Company.objects.all()
        for company in companies:
            for relationship in relationships:
                if company.id == relationship.company_id:
                    companies = companies.exclude(id=company.id)
        context = {'password_error': False, 'has_error': False, 'id': id, 'companies': companies}
        if request.method == 'POST':
            company_id = request.POST['company_id']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if len(password1) < 6:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña debe tener al menos 6 caracteres')
                context['has_error'] = True
            if password1 != password2:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                context['has_error'] = True
            if context['has_error']:
                return render(request, 'add-company.html', context)
            
            relation = CompanyRelations(client_id=_clientUser.id, company_id=company_id, password=pbkdf2_sha256.hash(password1), city_id=_city.id)
            relation.save()
            companies = companies.exclude(id=company_id)
            context['companies'] = companies
            messages.add_message(request, messages.SUCCESS, 'Empresa Agregada Exitosamente')
            
        return render(request, 'add-company.html', context)
    return redirect('/main')
            
@login_required(login_url='/login')
def edit_company_forCity_view(request, relation_id):
    closeSession(request)
    from passlib.hash import pbkdf2_sha256
    _relation = CompanyRelations.objects.get(id=relation_id)
    _company = get_object_or_404(Company, id=_relation.company_id)
    _city = get_object_or_404(City, id=_relation.city_id)
    if _city.user_id == request.user.id:
        id = request.user.id
        _clientUser = ClientUser.objects.get(user_id=id)
        _relation = get_object_or_404(CompanyRelations, client_id=_clientUser.id, company_id=_company.id)
        if not _clientUser.isCity:
            return redirect('/main-company')
        context = {'id': request.user.id, 'company': _company, 'city': _city, 'password_error': False, 'passwordlast_error': False, 'has_error': False, 'relation': _relation}
        if request.method == 'POST':
            password = request.POST['password']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if len(password1) < 6:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña debe tener al menos 6 caracteres')
                context['has_error'] = True
            if password1 != password2:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                context['has_error'] = True
            if not pbkdf2_sha256.verify(password, _company.password):
                context['passwordlast_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña anterior no coincide')
                context['has_error'] = True
            if context['has_error']:
                return render(request, 'edit-company.html', context)
            _relation.password = pbkdf2_sha256.hash(password1)
            _relation.save()
            messages.add_message(request, messages.SUCCESS, 'Empresa Editada Exitosamente')

        return render(request, 'edit-company.html', context)

@login_required(login_url='/login')
def delete_company_view(request, relation_id):
    closeSession(request)
    _relation = CompanyRelations.objects.get(id=relation_id)
    _company = get_object_or_404(Company, id=_relation.company_id)
    _city = get_object_or_404(City, id=_relation.city_id)
    context = {'id': request.user.id}
    if _city.user_id == request.user.id:
        id = request.user.id
        _clientUser = ClientUser.objects.get(user_id=id)
        if not _clientUser.isCity:
            return redirect('/main-company')
        _relations = get_object_or_404(CompanyRelations, client_id=_clientUser.id, company_id=_company.id)    
        _relations.delete() 
        _lines = Line.objects.filter(company_id=_company.id, city_id=_city.id)
        _lines.delete()
        messages.add_message(request, messages.SUCCESS, 'Empresa Eliminada Exitosamente')
        return render(request, 'company-deleted.html', context)

def register_company_view(request):
    closeSession(request)
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        form = CreateUserForm()
        context = {'has_error': False, 'form': form, 'data': request.POST, 'password_error': False, 'username_error': False}

        if request.method == 'POST':
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']
            password2 = request.POST['password2']

            if len(password) < 6:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña debe tener al menos 6 caracteres')
                context['has_error'] = True
            if password != password2:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                context['has_error'] = True
            if User.objects.filter(email=email).exists():
                context['has_error'] = True
                messages.add_message(request, messages.ERROR, 'El email ya esta registrado')

            if User.objects.filter(username=username).exists():
                context['username_error'] = True
                messages.add_message(request, messages.ERROR, 'El usuario ya existe')
                context['has_error'] = True
            if not username:
                messages.add_message(request, messages.ERROR, 'El nombre de usuario no puede estar vacío')
                context['has_error'] = True
            if context['has_error']:
                return render(request, 'register.html', context)
            
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                userIsCity = ClientUser(isCity=False, user_id=User.objects.get(username=username).id)      
                userIsCity.save()
                messages.add_message(request, messages.SUCCESS, 'Usuario creado exitosamente')
            else:
                return render(request, 'register.html', context)
                

        return render(request, 'register-company.html', context)

@login_required(login_url='/login')
def main_view_company(request):
    closeSession(request)
    id = request.user.id
    _clientUser = ClientUser.objects.get(user_id=id)
    if _clientUser.isCity:
        return redirect('/main')
    context= {'status': False, 'activated': False, 'user_id': 0}
    _company = Company.objects.get(user_id=id)
    activated = _company.activated
    id = _company.user_id
    context['activated'] = activated
    context['user_id'] = id
    return render(request, 'main-hub-company.html', context)

@login_required(login_url='/login')
def edit_company_view(request, id):
    closeSession(request)
    if request.user.id == id:
        change_password = False
        id = request.user.id
        _user = User.objects.get(id=id)
        _clientUser = ClientUser.objects.get(user_id=id)
        if _clientUser.isCity:
            return redirect('/main')
        _company = Company.objects.get(user_id=id)
        context = {'company': _company, 'user': _user,'name_error': False, 'has_error': False,}
        if request.method == 'POST':
            username = request.POST['username']
            last_password = request.POST['password']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            color = request.POST['color']
            users = User.objects.all().exclude(id=id)
            user = authenticate(username=_user.username, password=last_password)
            if last_password == '':
                context['passwordlast_error'] = True
                messages.add_message(request, messages.ERROR, 'Tiene que confirmar la contraseña')
                context['has_error'] = True
            elif user is None:
                context['passwordlast_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña anterior no coincide')
                context['has_error'] = True
            if password1 != "" and password2 != "":
                change_password = True
            if len(last_password) < 6 and change_password:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'La contraseña debe tener al menos 6 caracteres')
                context['has_error'] = True
            if password1 != password2:
                context['password_error'] = True
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden')
                context['has_error'] = True
            if users.filter(username=username).exists() and change_password:
                context['username_error'] = True
                messages.add_message(request, messages.ERROR, 'El usuario ya existe')
                context['has_error'] = True
            if not username:
                messages.add_message(request, messages.ERROR, 'El nombre de usuario no puede estar vacío')
                context['has_error'] = True
            if users.filter(email=email).exists() and change_password:
                context['has_error'] = True
                messages.add_message(request, messages.ERROR, 'El email ya esta registrado')
            if context['has_error']:
                return render(request, 'edit-company-view.html', context)
            if change_password:
                user.set_password(password1)
            _company.username = username
            _company.color = color
            _user.email = email
            _user.save()        
            _company.save()
            messages.add_message(request, messages.SUCCESS, 'Empresa Editada Exitosamente')
    return render(request, 'edit-company-view.html', context)

@login_required(login_url='/login')
def edit_cities_view(request, id):
    closeSession(request)
    if request.user.id == id:
        cities = []
        id = request.user.id
        _user = User.objects.get(id=id)
        _clientUser = ClientUser.objects.get(user_id=id)
        _company = Company.objects.get(user_id=id)
        _relations = CompanyRelations.objects.filter(company_id=_company.id)
        for relation in _relations:
            _city_ = City.objects.get(id=relation.city_id)
            _city_.relation_id = relation.id
            cities.append(_city_)
        context = {'company': _company, 'user': _user,'cities': cities, 'has_cities': False, 'relations': _relations}
        if len(cities) > 0:
            context['has_cities'] = True
        if _clientUser.isCity:
            return redirect('/main')
        return render(request, 'edit-cities.html', context)

@login_required(login_url='/login')
def access_cities_view(request, relation_id):
    from passlib.hash import pbkdf2_sha256
    from ipware import get_client_ip
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        # Unable to get the client's IP address
        return HttpResponse("No se pudo obtener la dirección IP del cliente")
    else:
        # We got the client's IP address
        if is_routable:
            # The client's IP address is publicly routable on the Internet
            try:
                CitySession.objects.get(user_id=request.user.id)
            except:
                client_ip = pbkdf2_sha256.hash(client_ip)
                _citySession = CitySession(user_id=request.user.id, ip=client_ip)
                _citySession.save()
        else:
            # Delete Before Publishing, just for local testing
            try:
                CitySession.objects.get(user_id=request.user.id)
            except:
                client_ip = pbkdf2_sha256.hash(client_ip)
                _citySession = CitySession(user_id=request.user.id, ip=client_ip)
                _citySession.save()
            #return HttpResponse("La dirección IP del cliente es privada")
    _relation = CompanyRelations.objects.get(id=relation_id)
    _company = Company.objects.get(id=_relation.company_id)
    if request.user.id != _company.user_id:
        return redirect('/main')
    id = request.user.id
    _clientUser = ClientUser.objects.get(user_id=id)
    if _clientUser.isCity:
        return redirect('/main')
    context = {'relation': _relation, 'company': _company, 'password_error': False}
    if request.method == 'POST':
        password = request.POST['password']
        if password == "":
            context['password_error'] = True
            messages.add_message(request, messages.ERROR, 'La contraseña no puede estar vacía')
            return render(request, 'verify-city.html', context)
        if not pbkdf2_sha256.verify(password, _relation.password):
            context['password_error'] = True
            messages.add_message(request, messages.ERROR, 'La contraseña no es correcta')
            return render(request, 'verify-city.html', context)
        _citySession = CitySession.objects.get(user_id=request.user.id)
        _citySession.status = True
        _citySession.save()
        return redirect(f'/cities/editlines/{_relation.id}')        
    return render(request, 'verify-city.html', context)

@login_required(login_url='/login')
def edit_cities_lines_view(request, relation_id):
    _citiSession = CitySession.objects.get(user_id=request.user.id)
    _relation = CompanyRelations.objects.get(id=relation_id)
    if not _citiSession.status:
        return redirect(f'/cities/verify/{_relation.id}')
    _company = Company.objects.get(id=_relation.company_id)
    _city = City.objects.get(id=_relation.city_id)
    id = _company.user_id
    if request.user.id == id:
        id = request.user.id
        _user = User.objects.get(id=id)
        _clientUser = ClientUser.objects.get(user_id=id)
        if _clientUser.isCity:
            return redirect('/main')
        _company = Company.objects.get(user_id=id)
        _relations = CompanyRelations.objects.filter(company_id=_company.id)
        _lines = Line.objects.filter(relation_id=_relation.id)
        context = {'company': _company, 'city':_city, 'user': _user,'lines': _lines, 'has_lines': False, 'relation': _relation}
        if len(_lines) > 0:
            context['has_lines'] = True
        return render(request, 'edit-cities-lines.html', context)
    return redirect('/main')

@login_required(login_url='/login')
def add_lines_view(request, relation_id):
    _relation = CompanyRelations.objects.get(id=relation_id)
    _company = Company.objects.get(id=_relation.company_id)
    id = _company.user_id
    if request.user.id == id:
        id = request.user.id
        _city = City.objects.get(id=_relation.city_id)
        _clientUser = ClientUser.objects.get(user_id=id)
        _line = Line(relation_id= _relation.id, city_id= _city.id)
        context = {'name_error': False, 'has_error': False, 'city': _city, 'company': _company, 'return_trip_error': False, 'round_trip_error': False, 'special_round_trip_error': False, 'special_return_trip_error': False,'relation': _relation}
        if _clientUser.isCity:
            return redirect('/main')
        if request.method == 'POST':
            name = request.POST['name']
            status = request.POST['status']
            try:
                round_trip = request.FILES['round-trip']  
                try:
                    round_trip = extractLineRoute(round_trip)
                    _line.round_trip = round_trip
                except:
                    context['round_trip_error'] = True
                    messages.add_message(request, messages.ERROR, 'El Recorrido de Ida no es una ruta')
                    context['has_error'] = True
            except:
                pass  

            try:
                return_trip = request.FILES['return-trip']
                try:
                    return_trip = extractLineRoute(return_trip)
                    _line.return_trip = return_trip
                except:
                    context['return_trip_error'] = True
                    messages.add_message(request, messages.ERROR, 'El Recorrido de Vuelta no es una ruta')
                    context['has_error'] = True
            except:
                pass

            try:
                special_round_trip = request.FILES['special-round-trip']
                try:
                    special_round_trip = extractLineRoute(special_round_trip)
                    _line.special_round_trip = special_round_trip
                except:
                    context['special_round_trip_error'] = True
                    messages.add_message(request, messages.ERROR, 'El Recorrido Especial Ida no es una ruta')
                    context['has_error'] = True
            except:
                pass

            try:
                special_return_trip = request.FILES['special-return-trip']
                try:
                    special_trip = extractLineRoute(special_return_trip)
                    _line.special_return_trip = special_return_trip
                except:
                    context['special_return_trip_error'] = True
                    messages.add_message(request, messages.ERROR, 'El Recorrido Especial Vuelta no es una ruta')
                    context['has_error'] = True
            except:
                pass

            try:
                excel = request.FILES['excel']
            except:
                pass
            if name == '':
                context['name_error'] = True
                messages.add_message(request, messages.ERROR, 'El nombre no puede estar vacío')
                context['has_error'] = True
            if status == 'true':
                _line.status = True
            else:
                _line.status = False
            if context['has_error']:
                return render(request, 'add-line.html', context)
            _line.name = name
            _line.save()
            messages.add_message(request, messages.SUCCESS, 'Ruta Agregada Exitosamente')

        return render(request, 'add-line.html', context)
    return redirect('/main')

@login_required(login_url='/login')
def edit_line_view(request, line_id):
    _line = Line.objects.get(id=line_id)
    _relation = CompanyRelations.objects.get(id=_line.relation_id)
    _company = Company.objects.get(id=_relation.company_id)
    _city = City.objects.get(id=_relation.city_id)
    _user = User.objects.get(id=_company.user_id)
    _clientUser = ClientUser.objects.get(user_id=_user.id)
    context = {'line': _line, 'city': _city, 'company': _company, 'user': _user, 'relation': _relation}
    if request.user.id != _user.id:
        return redirect('/main')    
    if _clientUser.isCity:
        return redirect('/main')
    if request.method == 'POST':
        context = {'line': _line, 'has_error': False, 'name_error': False, 'city': _city, 'company': _company, 'return_trip_error': False, 'round_trip_error': False, 'special_round_trip_error': False, 'special_return_trip_error': False, 'relation': _relation}
        name = request.POST['name']
        status = request.POST['status']
        try:
            round_trip = request.FILES['round-trip']  
            try:
                round_trip = extractLineRoute(round_trip)
                _line.round_trip = round_trip
            except:
                context['round_trip_error'] = True
                messages.add_message(request, messages.ERROR, 'El Recorrido de Ida no es una ruta')
                context['has_error'] = True
        except:
            pass  

        try:
            return_trip = request.FILES['return-trip']
            try:
                return_trip = extractLineRoute(return_trip)
                _line.return_trip = return_trip
            except:
                context['return_trip_error'] = True
                messages.add_message(request, messages.ERROR, 'El Recorrido de Vuelta no es una ruta')
                context['has_error'] = True
        except:
            pass

        try:
            special_round_trip = request.FILES['special-round-trip']
            try:
                special_round_trip = extractLineRoute(special_round_trip)
                _line.special_round_trip = special_round_trip
            except:
                context['special_round_trip_error'] = True
                messages.add_message(request, messages.ERROR, 'El Recorrido Especial Ida no es una ruta')
                context['has_error'] = True
        except:
            pass

        try:
            special_return_trip = request.FILES['special-return-trip']
            try:
                special_trip = extractLineRoute(special_return_trip)
                _line.special_return_trip = special_return_trip
            except:
                context['special_return_trip_error'] = True
                messages.add_message(request, messages.ERROR, 'El Recorrido Especial Vuelta no es una ruta')
                context['has_error'] = True
        except:
            pass

        try:
            excel = request.FILES['excel']
        except:
            pass
        if name == '':
            context['name_error'] = True
            messages.add_message(request, messages.ERROR, 'El nombre no puede estar vacío')
            context['has_error'] = True
        if status == 'true':
            _line.status = True
        else:
            _line.status = False
        if context['has_error']:
            return render(request, 'add-line.html', context)
        _line.name = name
        _line.save()
        messages.add_message(request, messages.SUCCESS, 'Ruta Editada Exitosamente')
    return render(request, 'edit-line.html', context)


@login_required(login_url='/login')
def set_busstops_view(request, relation_id):
    _clientUser = ClientUser.objects.get(user_id=request.user.id)
    if _clientUser.isCity:
        return redirect('/main')
    _relation = CompanyRelations.objects.get(id=relation_id)
    _company = Company.objects.get(id=_relation.company_id)
    if _relation.company_id != _company.id:
        return redirect('/main')
    _city = City.objects.get(id=_relation.city_id)
    context = {'paradas_error': False, 'relation': _relation}
    if request.method == 'POST':
        try:
            bus_stops = request.FILES['bus-stops']
            try:
                bus_stops = extractBusStops(bus_stops)
                try:
                    _bus_stop = BusStops.objects.get(relation_id=_relation.id)
                    extractAndUpdate(_bus_stop.busStops, _relation.id)
                except:
                    _bus_stops = BusStops()
                    _bus_stops.relation_id = _relation.id
                    _bus_stops.busStops = bus_stops
                    _bus_stops.save()

            except:
                context['special_round_trip_error'] = True
                messages.add_message(request, messages.ERROR, 'El Recorrido Especial Ida no es una ruta')
                context['has_error'] = True
        except:
            pass
    return render(request, 'set-busstops.html', context)

class CitiesViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = City.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        city = get_object_or_404(City, pk=params.get('pk'))
        serializer = CitySerializer(city)
        return Response(serializer.data)

class BusStopsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = BusStops.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = get_list_or_404(BusStops, relation_id=kwargs.get('relation_id'))
        serializer = BusStopsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        stop = get_object_or_404(City, pk=params.get('pk'))
        serializer = BusStopsSerializer(stop)
        return Response(serializer.data)

class RegisterCompanyViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def registerCity(request):
    _cities = City.objects.filter(status=True)
    serializer = CitySerializer(_cities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllStops(request):
    _stops = BusStops.objects.all()
    serializer = BusStopsSerializer(_stops, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCityCompanies(request, city_id):
    _relations = CompanyRelations.objects.filter(city_id=city_id)
    serializer = CompanyRelationsSerializer(_relations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCityLines(request, city_id):
    _lines = Line.objects.filter(city_id=city_id)     
    serializer = LinesSerializer(_lines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCompany(request, company_id):
    _company = Company.objects.get(id=company_id)  
    serializer = CompanySerializer(_company)
    return Response(serializer.data)

def home_view(request):
    closeSession(request)
    return render(request, 'home-view.html')