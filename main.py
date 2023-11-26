import sqlite3
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.snackbar import Snackbar

conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        preco REAL,
        comb REAL,
        km REAL,
        resultado REAL,
        nome VARCHAR(50),
        placa VARCHAR(10)
    )
''')
conn.commit()

kv_string='''<Inicio>:
    name:'inicio'
    FloatLayout:
        MDTopAppBar:
            title: "[u][i]Tanque Cheio[/i][/u]"
            pos_hint: {'center_x': 0.5,'center_y': 0.95}
            elevation: 5
            right_action_items: [['exit-to-app', lambda x: app.stop()]]
            left_action_items: [['android']]

        Image:
            source:'logo.png'
            size_hint: None, None
            size: '200dp','200dp'
            pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        MDRaisedButton:
            text: 'Iniciar'
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            on_release: root.manager.current = 'requisitos'
<Requisitos>:
    name:'requisitos'
    MDTopAppBar:
        title: "[u][i]Insira os dados[/i][/u]"
        anchor_title: "left"
        right_action_items: [['exit-to-app', lambda x: app.stop()]]
        left_action_items: [["history", lambda x: root.mostrar_historico()]]
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
    MDTextField:
        id: placa
        multiline: False
        size_hint_x: .8
        pos_hint: {'center_x': 0.5,'center_y': 0.84}
        hint_text: "Placa do veículo"
        mode: "fill"
    MDTextField:
        id: comb
        multiline: False
        size_hint_x: .8
        pos_hint: {'center_x': 0.5,'center_y': 0.73}
        hint_text: "Quantidade de reais em combustível"
        mode: "fill"
    MDTextField:
        id: preco
        multiline: False
        size_hint_x: .8
        pos_hint: {'center_x': 0.5,'center_y': 0.62}
        hint_text: "Preço do combustível"
        mode: "fill"
    MDTextField:
        id: km
        multiline: False
        size_hint_x: .8
        pos_hint: {'center_x': 0.5,'center_y': 0.51}
        hint_text: "Quilômetros rodados"
        mode: "fill"
    MDTextField:
        id: nome
        multiline: False
        size_hint_x: .8
        pos_hint: {'center_x': 0.5,'center_y': 0.40}
        hint_text: "Nome do motorista"
        mode: "fill"
    MDFillRoundFlatButton:
        pos_hint: {'center_x': 0.35,'center_y': 0.3}
        text: "Calcular"
        on_press: root.calcular()
    MDFillRoundFlatButton:
        pos_hint: {'center_x': 0.65,'center_y': 0.3}
        text: "Limpar"
        on_press: root.limpar()
    MDLabel:
        id: resposta
        text: ''
        font_size:
        halign: 'center'
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
<Historico>:
    name: 'historico'
    MDTopAppBar:
        title: "[u][i]<< Apagar histórico[/i][/u]"
        anchor_title: "left"
        left_action_items: [['trash-can-outline', lambda x: root.apagar_historico()]]
        right_action_items: [["keyboard-backspace", lambda x: root.voltar()]]
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
    MDLabel:
        id: historico_label
        text: ''
        font_size: 20
        halign: 'center'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}'''

class Historico(MDScreen):
    def voltar(self):
        self.manager.current = 'requisitos'
    def apagar_historico(self):
        cursor.execute('DELETE FROM dados')
        conn.commit()
        self.ids.historico_label.text = "Histórico apagado"
        self.show_temporary_message("Histórico apagado com sucesso")
    def show_temporary_message(self, message):
        self.snackbar = Snackbar(text=message)
        self.snackbar.open()

    def on_enter(self):
        cursor.execute('SELECT * FROM dados')
        data = cursor.fetchall()
        history_text = ""
        for entry in data:
            history_text += f"ID: {entry[0]}, Preço: {entry[1]}, Combustível: {entry[2]}, KM: {entry[3]}, Resultado: {round(entry[4], 2)}, Nome: {entry[5]}, Placa: {entry[6]}\n"
        self.ids.historico_label.text = history_text
class Inicio(MDScreen):
    pass
class Requisitos(MDScreen):
    def mostrar_historico(self):
        self.manager.current = 'historico'
    def calcular(self):
        preco = float(self.ids.preco.text)
        comb = float(self.ids.comb.text)
        km = float(self.ids.km.text)
        nome = (self.ids.nome.text)
        placa = (self.ids.placa.text)
        
        resultado = km / (comb / preco)
        
        cursor.execute('INSERT INTO dados(preco, comb, km, resultado, nome, placa) VALUES (?, ?, ?, ?, ?, ?)', (preco, comb, km, resultado, nome, placa))
        conn.commit()

        self.ids.resposta.text = f"A média total de gasto de combustível é: {resultado:.2f}"
    def limpar(self):
        self.ids.preco.text = ''
        self.ids.comb.text = ''
        self.ids.km.text = ''
        self.ids.resposta.text = ''
        self.ids.nome.text = ''
        self.ids.placa.text = ''
class Main(MDApp):
    def build(self):
        Builder.load_string(kv_string)
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette = "Orange"
        self.title='Tanque cheio'
        sm = MDScreenManager()
        sm.add_widget(Inicio())
        sm.add_widget(Requisitos())
        sm.add_widget(Historico())
        return sm
    
Main().run()