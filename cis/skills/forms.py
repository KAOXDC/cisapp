from django import forms

class importar_form(forms.Form):
	archivo = forms.FileField()

class Login_form(forms.Form):
	usuario  = forms.CharField(widget = forms.TextInput())
	clave = forms.CharField(widget = forms.PasswordInput(render_value = False))

class buscar_form(forms.Form):
	buscar = forms.CharField(widget = forms.TextInput())
