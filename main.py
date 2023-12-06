import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel


conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(80),
        placa VARCHAR(10),
        modelo VARCHAR(100) NULL,
        lconsumo REAL,
        km REAL,
        resultado REAL
    )
''')
conn.commit()

class Historico(MDScreen):
    def voltar_inicio(self):
        self.manager.current = 'requisitos'
    def apagar_confirmacao(self):
        dialog = MDDialog(
            title="Confirmação",
            text="Tem certeza de que deseja apagar o histórico?",
            buttons=[
                MDRaisedButton(
                    text="Cancelar", on_release=lambda *args: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Apagar",
                    on_release=lambda *args: self.apagar_historico(dialog),
                ),
            ],
        )
        dialog.open()
    def apagar_historico(self, dialog):
        cursor.execute('DELETE FROM dados')
        conn.commit()
        self.ids.historico_label.text = "Histórico apagado"
        self.temporario()
        dialog.dismiss()
    def temporario(self):
        self.snackbar = Snackbar(text="Histórico apagado com sucesso")
        self.snackbar.open()
    def on_enter(self):
        cursor.execute('SELECT * FROM dados')
        data = cursor.fetchall()
        history_text = ""
        for entry in data:
            history_text += f'''
            ID: {entry[0]}
            Nome: {entry[1]} 
            Placa: {entry[2]}
            Modelo: {entry[3]}
            L/Consumidos: {entry[4]}
            KM/Percorridos: {entry[5]}
            Resultado: {round(entry[6], 2)}\n\n'''
        self.ids.historico_label.text = history_text
class Inicio(MDScreen):
    pass
class Requisitos(MDScreen):
    def voltar_r(self):
        self.manager.current = 'inicio'
        self.manager.transition.direction = 'left'
    def mostrar_historico(self):
        self.manager.current = 'historico'
    def calcular(self):
            nome = (self.ids.nome.text)
            placa = (self.ids.placa.text)
            modelo = (self.ids.modelo.text)
            try:
                lconsumo = float(self.ids.lconsumo.text.replace(',', '.'))
                km = float(self.ids.km.text.replace(',', '.'))
            except ValueError:
                self.ids.resposta.text = "Insira ou preencha valores válidos!"
                self.ids.resposta.theme_text_color = "Custom"
                self.ids.resposta.text_color = 1, 0, 0, 1
                return

            resultado = km / lconsumo
            cursor.execute('INSERT INTO dados(nome, placa, modelo, lconsumo, km, resultado) VALUES (?, ?, ?, ?, ?, ?)', (nome, placa, modelo, lconsumo, km, resultado))
            conn.commit()
            self.ids.resposta.text = f"A média de consumo de combustível é: {resultado:.2f}"
            self.ids.resposta.theme_text_color = "Primary"
    def limpar(self):
        self.ids.nome.text = ''
        self.ids.placa.text = ''
        self.ids.modelo.text = ''
        self.ids.lconsumo.text = ''
        self.ids.km.text = ''
        self.ids.resposta.text = ''
class Autonomia(MDScreen):
    def voltar_r(self):
        self.manager.current = 'inicio'
        self.manager.transition.direction = 'left'
class Viagem(MDScreen):
    def voltar_r(self):
        self.manager.current = 'inicio'
        self.manager.transition.direction = 'left'

class Main(MDApp):
    dialog = None
    def build(self):
        Window.size=(360, 640)
        Builder.load_file('main.kv')
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette = "Orange"
        self.title='Tanque cheio'
        sm = MDScreenManager()
        sm.add_widget(Inicio())
        sm.add_widget(Requisitos())
        sm.add_widget(Historico())
        sm.add_widget(Autonomia())
        sm.add_widget(Viagem())
        return sm
    def aviso(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Sobre nós",
                text="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", #EDITAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                auto_dismiss=True,
                buttons=[
                    MDFlatButton(
                        text="Fechar",
                        on_release= lambda *args: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()
Main().run()
