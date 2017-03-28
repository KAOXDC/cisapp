#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

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
			cargar_excel()
			return HttpResponseRedirect('/resultados/')
		else:	
			messages.success(request, "Error al subir Archivo")
	else:
		form = importar_form()
	return render(request,'importar.html',locals())

def cargar_excel():
	'''Leer XL'''
	competencias = []
	wb = load_workbook(filename = 'media/excel.xlsx')
	#sheet_ranges = wb['Table 1']
	#print sheet_ranges['B3'].value
	#wb.get_sheet_names()
	marca = "100 Scale Marks"
	aux = " "
	personas = []
	hoja=wb.get_sheet_by_name(str(wb.get_sheet_names()[0])) #obtiene el nombre de la hoja
	temp = wb.active
	#print temp.rows
	for i in range(1, 1000):
		try:
			fila = hoja['B'+str(i)].value.encode('utf8')
			#reg  = hoja['C'+str(i)].value.encode('utf8')
		except:
			fila = "blanco"
			#reg = "blanco"
		try:
			if fila != 'Name':
				persona = hoja['B'+str(i)].value.encode('utf8')
				region  = hoja['C'+str(i)].value.encode('utf8')
				dia_1   = hoja['E'+str(i)].value#.encode('utf8')
				dia_2   = hoja['F'+str(i)].value#.encode('utf8')
				dia_3   = hoja['G'+str(i)].value#.encode('utf8')
				dia_4   = hoja['H'+str(i)].value#.encode('utf8')
				total   = dia_1+dia_2+dia_3+dia_4 #.encode('utf8')
				p = i,'----',persona, region, total, dia_1, dia_2, dia_3, dia_4 
				#print i,'----',persona, region, total, dia_1, dia_2, dia_3, dia_4 
				
				if persona=="blanco" and region=="blanco" and total=="blanco" and dia_1=="blanco" and dia_2=="blanco" and dia_3=="blanco" and dia_4:
					break
				else:	
					personas.append(p)
					Concursante.objects.create(competencia= aux,evento= "FALTA",aprendices= persona,region= region,total=int(total) ,dia_1= int(dia_1),dia_2= int(dia_2),dia_3= int(dia_3),dia_4= int(dia_4))

		except: 
			if marca == str(fila):
				comp = hoja['B'+str(i-1)].value.encode('utf8')
				if aux != comp:
					aux = comp
					competencias.append(str(comp))
					#print "-------------------------"
					#print aux
					#print "-------------------------"
			persona = "blanco"
			region  = "blanco"
			dia_1   = "blanco"
			dia_2   = "blanco"
			dia_3   = "blanco"
			dia_4   = "blanco"
			total   = "blanco"
		#print 'B'+str(i), "---", fila
		if marca == str(fila):
			comp = hoja['B'+str(i-1)].value.encode('utf8')
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


def resultados_view(request):
	resultados = Concursante.objects.filter()
	competencias=[]
	aux=''
	for index, i in enumerate(resultados):
		comp = resultados[index].competencia
		if aux != i.competencia:
			aux = comp 
			competencias.append(comp)

	print len(competencias)		
	return render(request,'resultados.html', locals())


def inicio_view(request):
	mensaje = ""

	if request.method == "POST": 
		form = Login_form(request.POST) #creamos un objeto de Loguin_form
		if form.is_valid(): # si la informacion enviada es correcta
			usu = form.cleaned_data['usuario'] #guarda informacion ingresada del form
			pas = form.cleaned_data['clave'] #guarda informacion ingresada del form
			usuario = authenticate(username = usu, password = pas)#asigna la autenticacion del usuario
			if usuario is not None and usuario.is_active:# si el usuario no es nulo y esta activo
				login(request, usuario) #se loguea al sistema con la informacion de usuario
				return HttpResponseRedirect('/importar/')# redirigimos a la pagina principal
			else:
				mensaje = "usuario y/o clave incorrecta"
	form = Login_form() #creamos un form nuevo en limpio
	ctx = {'form':form, 'mensaje':mensaje} # variable de contexto para pasar info a login.html
	#return render_to_response('home/login.html', ctx, context_instance = RequestContext(request))
	return render(request,'inicio.html', locals())






from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class concursante_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Concursante
        fields = ('competencia','evento','fecha_subida','aprendices','region','total','dia_1','dia_2','dia_3','dia_4',)
# ViewSets define the view behavior.
class resultados_viewset(viewsets.ModelViewSet):
    queryset = Concursante.objects.all()
    serializer_class = concursante_serializer



#x = Concursante.objects.create(competencia= "aux",evento= "FALTA",aprendices= "juan",region= "cauca",total=100 ,dia_1= 1,dia_2= 2,dia_3= 3,dia_4= 4)
