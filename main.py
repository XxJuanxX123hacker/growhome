import flet as ft
import psycopg2

class Usuario:
    def __init__(self,tupla):
        self.nombre=tupla[0][0]
        self.correo=tupla[0][1]
        self.contra=tupla[0][2]


def conectarBaseD():
    return psycopg2.connect(host='localhost', user='postgres', password='usuario', database='growthome')




class CrudUsuario:

    def agregarUsuario(self, tupla):
        conexion = conectarBaseD()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, correo, contra) VALUES (%s, %s, %s)",
            (tupla[0], tupla[1], tupla[2]))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminarPaciente(self, correo):
        conexion = conectarBaseD()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuario WHERE correo=%s", (correo,))
        conexion.commit()
        cursor.close()
        conexion.close()

    def modificarPaciente(self, correo, nombre):
        conexion = conectarBaseD()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre=%s WHERE id_paciente=%s",
            (nombre , correo))
        conexion.commit()
        cursor.close()
        conexion.close()

    def buscarPaciente(self, correo,contra ):
        conexion = conectarBaseD()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM usuario WHERE (correo=%s) AND (contra=%s) ",
            (correo,contra))
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados

def iniSesion(page: ft.Page):
    usuario= CrudUsuario()
    page.clean()
    def Biniciar(e):
        row = usuario.buscarPaciente(txt_name.value,txt_contr.value)
        if not row:
            txt_name.error_text = "Contraseña o usuario incorrecto "
            page.update()
        else:
            print(row)
            us=Usuario(row)
            page.clean()
            page.add(ft.Text(f"Hello, {us.nombre}!"))
    def Bregise(e):
        registro(page)

    txt_name = ft.TextField(label="ingrese su usuario o contraseña")
    txt_contr = ft.TextField(label="Ingrese su contraseña")
    inicio=ft.ElevatedButton("Iniciar sesion", on_click=Biniciar)
    reg=ft.ElevatedButton("registrarse", on_click=Bregise)
    page.add(txt_name, txt_contr, inicio, reg )


def registro(page: ft.Page):
    usuario = CrudUsuario()
    page.clean()

    def Bregist(e):
        if not txt_name.value:
            txt_name.error_text = "ingrese su nombre"
            page.update()
        elif not txt_corr.value:
            txt_corr.error_text = "ingrese un correo valido"
            page.update()
        elif not txt_contr.value:
            txt_contr.error_text = "ingrese una contraseña"
            page.update()
        elif not txt_ccontr.value:
            txt_ccontr.error_text = "vuelva a ingresar la contraseña"
            page.update()
        elif not txt_ccontr.value == txt_contr.value:
            txt_ccontr.error_text = "ingrese la misma contraseña"
            page.update()
        else :
            tup = (txt_name.value, txt_corr.value, txt_contr.value)
            usuario.agregarUsuario(tup)
            iniSesion(page)



    def Bini(e):
        iniSesion(page)

    txt_name = ft.TextField(label="ingrese su nombre")
    txt_corr = ft.TextField(label="Ingrese su correo")
    txt_contr = ft.TextField(label="ingrese su contraseña")
    txt_ccontr = ft.TextField(label="confirme su contraseña")
    registrar= ft.ElevatedButton("Registrate", on_click=Bregist)
    inic = ft.ElevatedButton("iniciar sesion", on_click=Bini)
    page.add(txt_name, txt_corr, txt_contr, txt_ccontr, registrar, inic)

def main(page: ft.Page):
    # Configuración general GUI
    page.margin = 0
    page.padding = 1
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {"Shadows Into Light": "/fonts/ShadowsIntoLight-Regular.ttf"}
    iniSesion(page)  # Función para llamar al menú principal y comenzar el programa.


ft.app(target=main, assets_dir="assets", upload_dir="assets/uploads", view=ft.WEB_BROWSER)



