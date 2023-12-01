import threading
from models.adm import Admin

class AgregarUsuarioThread(threading.Thread):
    def __init__(self, nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario):
        super(AgregarUsuarioThread, self).__init__()
        self.nombre = nombre
        self.apellidoP = apellidoP
        self.apellidoM = apellidoM
        self.alias = alias
        self.email = email
        self.psw = psw
        self.tipoUsuario = tipoUsuario
        
    def run(self):
        resultado = Admin.insertar_usuario(self.nombre, self.apellidoP, self.apellidoM, self.alias, self.email, self.psw, self.tipoUsuario)