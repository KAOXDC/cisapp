#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

from openpyxl import load_workbook
from .forms import *
from .models import *
# Create your views here.

def handle_uploaded_file(f):
    with open('media/excel.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def importar_view(request):
	if request.method == 'POST':
		form = importar_form(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['archivo'])
			info = "es valido"
			messages.success(request, "Archivo subido con Exito")
			'''carga el  excel'''
			cargar_excel()
			return redirect('/resultados/')
		else:	
			messages.success(request, "Error al subir Archivo")
	else:
		form = importar_form()
	return render(request,'importar.html',locals())

def eliminar_registros_evento():
	try:
		Concursante.objects.all().delete()
		mensaje = "registros eliminados con exito" 
	except:
		mensaje = "no se pudo eliminar" 
		return False
	return True 


def cargar_excel():
	'''Leer XL'''
	competencias = []
	wb = load_workbook(filename = 'media/excel.xlsx')
	marca = "100 Scale Marks"
	evento = "Sin Evento"
	aux = " "
	personas = []
	hoja=wb.get_sheet_by_name(str(wb.get_sheet_names()[0])) #obtiene el nombre de la hoja
	temp = wb.active
	#print temp.rows

	''' Elimina registros de la  base de datos  '''
	eliminar_registros_evento()


	''' Recorre el excel '''
	for i in range(1, 1000):
		try:
			fila = hoja['A'+str(i)].value.encode('utf8')
			#reg  = hoja['C'+str(i)].value.encode('utf8')
		except:
			fila = "blanco"
			#reg = "blanco"
		try:
			#identificando el inicio de la  tabla 
			if fila != 'Name': 
				persona = hoja['A'+str(i)].value.encode('utf8')
				region  = hoja['B'+str(i)].value.encode('utf8')
				dia_1   = (hoja['D'+str(i)].value)/100.#.encode('utf8')
				dia_2   = (hoja['E'+str(i)].value)/100.#.encode('utf8')
				dia_3   = (hoja['F'+str(i)].value)/100.#.encode('utf8')
				#dia_4   = hoja['H'+str(i)].value#.encode('utf8')
				total   = dia_1+dia_2+dia_3#+dia_4 #.encode('utf8')
				p = i,'----',persona, region, total, dia_1, dia_2, dia_3#, dia_4 
				#print i,'----',persona, region, total, dia_1, dia_2, dia_3#, dia_4 
				print i,'----',type(total), dia_1

				if persona=="blanco" and region=="blanco" and total=="blanco" and dia_1=="blanco" and dia_2=="blanco" and dia_3:# and dia_4:
					break
				else:	
					personas.append(p)
					''' Guarda en la  base de Datos '''
					Concursante.objects.create(competencia= aux,evento= evento,aprendices= persona,region= region,total=total ,dia_1= dia_1,dia_2= dia_2,dia_3= dia_3)#,dia_4= int(dia_4))

		except: 
			if marca == str(fila):
				comp = hoja['A'+str(i-1)].value.encode('utf8')
				evento = hoja['A'+str(i+1)].value.encode('utf8')
				if aux != comp:
					aux = comp
					competencias.append(str(comp))
					print "-------------------------"
					#print aux
					print "-------------------------"
			persona = "blanco"
			region  = "blanco"
			dia_1   = "blanco"
			dia_2   = "blanco"
			dia_3   = "blanco"
			dia_4   = "blanco"
			total   = "blanco"
		#print 'B'+str(i), "---", fila
		if marca == str(fila):
			comp = hoja['A'+str(i-1)].value.encode('utf8')
			if aux != comp:
				aux = comp
				competencias.append(str(comp))

		'''guardar el  resultado en la bd'''
		#print i,'----',type(persona), type(region), type(total), type(dia_1), type(dia_2), type(dia_3), type(dia_4) 

	print '===================='
	for l in competencias:
		#print l
		pass
	print "Total Competencias" ,len(competencias)
	print '===================='
	print 'total de participantes', len(personas)

def buscar_view(request):
	return render(request,'inicio.html',{})

def resultados_view(request):
	mensaje = ""
	resultados = Concursante.objects.filter()
	if request.method == "GET":
		form = buscar_form()
	if request.method == 'POST':
		form = buscar_form(request.POST)
		if form.is_valid():
			x = form.cleaned_data['buscar']
			#resultados = Concursante.objects.filter(aprendices__icontains = x)
			resultados = Concursante.objects.filter(Q(aprendices__icontains=x)|Q(competencia__icontains=x)|Q(region__icontains=x))
			if resultados:
				pass
			else:
				mensaje = "No se encontraron resultados por favor cambie su criterio de busqueda"
	competencias=[]
	eventos=[]
	aux=''
	for index, i in enumerate(resultados):
		comp 	= resultados[index].competencia
		evento 	= resultados[index].evento
		if aux != i.competencia:
			aux = comp 
			competencias.append(comp)
			eventos.append(evento)
	lista = zip(competencias,eventos)		
	print len(competencias)		
	return render(request,'resultados.html', locals())


def inicio_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return redirect('/resultados/')
	if request.method == "POST": 
		form = Login_form(request.POST) #creamos un objeto de Loguin_form
		if form.is_valid(): # si la informacion enviada es correcta
			usu = form.cleaned_data['usuario'] #guarda informacion ingresada del form
			pas = form.cleaned_data['clave'] #guarda informacion ingresada del form
			usuario = authenticate(username = usu, password = pas)#asigna la autenticacion del usuario
			if usuario is not None and usuario.is_active:# si el usuario no es nulo y esta activo
				login(request, usuario) #se loguea al sistema con la informacion de usuario
				return redirect('/importar/')# redirigimos a la pagina principal
			else:
				mensaje = "usuario y/o clave incorrecta"
	form = Login_form() #creamos un form nuevo en limpio
	ctx = {'form':form, 'mensaje':mensaje} # variable de contexto para pasar info a login.html
	#return render_to_response('home/login.html', ctx, context_instance = RequestContext(request))
	return render(request,'inicio.html', locals())

def cerrar_sesion(request):
	logout(request)
	return redirect('/')


''' xxxxxxxxxxxxxxxxxx Servicios  Web xxxxxxxxxxxxxxxxxx '''

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class concursante_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Concursante
        fields = ('competencia','evento','fecha_subida','aprendices','region','total','dia_1','dia_2','dia_3',)
# ViewSets define the view behavior.
class resultados_viewset(viewsets.ModelViewSet):
    queryset = Concursante.objects.all()
    serializer_class = concursante_serializer

''' xxxxxxxxxxxxxxxxxx Fin Servicios  Web xxxxxxxxxxxxxxxxxx '''

#x = Concursante.objects.create(competencia= "aux",evento= "FALTA",aprendices= "juan",region= "cauca",total=100 ,dia_1= 1,dia_2= 2,dia_3= 3,dia_4= 4)
