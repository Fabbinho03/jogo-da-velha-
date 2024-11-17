from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import random

# Configurando o fundo para um tom neutro
Window.clearcolor = (0.2, 0.2, 0.2, 1)

class JogoDaVelha(GridLayout):
    def __init__(self, simbolo, modo_jogo, dificuldade, app, **kwargs):
        super(JogoDaVelha, self).__init__(**kwargs)
        self.cols = 3
        self.tabuleiro = [" " for _ in range(9)]
        self.turno = simbolo
        self.simbolo_jogador = simbolo
        self.simbolo_ia = "O" if simbolo == "X" else "X"
        self.modo_jogo = modo_jogo
        self.dificuldade = dificuldade
        self.app = app
        self.cor_jogador = (0, 0.7, 0.2, 1)  # Verde
        self.cor_ia = (0.7, 0, 0.2, 1)       # Vermelho
        if self.simbolo_jogador == "O":
            # Invertemos as cores se o jogador escolher "O"
            self.cor_jogador, self.cor_ia = self.cor_ia, self.cor_jogador
        self.criar_botoes()

        if self.modo_jogo == "Humano vs IA" and self.turno == self.simbolo_ia:
            self.jogar_ia()

    def criar_botoes(self):
        for i in range(9):
            btn = Button(
                text=" ",
                font_size=50,
                background_normal="",
                background_color=(0.3, 0.3, 0.3, 1),
                color=(1, 1, 1, 1),
            )
            btn.bind(on_press=self.jogar)
            self.add_widget(btn)

    def jogar(self, button):
        index = self.children.index(button)
        if self.tabuleiro[index] == " ":
            self.tabuleiro[index] = self.turno
            button.text = self.turno
            button.background_color = self.cor_jogador if self.turno == self.simbolo_jogador else self.cor_ia
            if self.verificar_vencedor():
                self.encerrar_jogo(f"{self.turno} venceu!")
            elif " " not in self.tabuleiro:
                self.encerrar_jogo("Empate!")
            else:
                self.alterar_turno()
                if self.modo_jogo == "Humano vs IA" and self.turno == self.simbolo_ia:
                    self.jogar_ia()

    def jogar_ia(self):
        index = self.encontrar_jogada_ia()
        if index is not None:
            self.tabuleiro[index] = self.simbolo_ia
            btn = self.children[index]
            btn.text = self.simbolo_ia
            btn.background_color = self.cor_ia
            if self.verificar_vencedor():
                self.encerrar_jogo("IA venceu!")
            elif " " not in self.tabuleiro:
                self.encerrar_jogo("Empate!")
            else:
                self.alterar_turno()

    def encontrar_jogada_ia(self):
        if self.dificuldade == "Fácil":
            possibilidades = [i for i in range(9) if self.tabuleiro[i] == " "]
            return random.choice(possibilidades) if possibilidades else None
        elif self.dificuldade == "Difícil":
            for i in range(9):
                if self.tabuleiro[i] == " ":
                    self.tabuleiro[i] = self.simbolo_ia
                    if self.verificar_vencedor():
                        self.tabuleiro[i] = " "
                        return i
                    self.tabuleiro[i] = " "
            for i in range(9):
                if self.tabuleiro[i] == " ":
                    self.tabuleiro[i] = self.simbolo_jogador
                    if self.verificar_vencedor():
                        self.tabuleiro[i] = " "
                        return i
                    self.tabuleiro[i] = " "
            possibilidades = [i for i in range(9) if self.tabuleiro[i] == " "]
            return random.choice(possibilidades) if possibilidades else None

    def verificar_vencedor(self):
        combinacoes = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                       (0, 3, 6), (1, 4, 7), (2, 5, 8),
                       (0, 4, 8), (2, 4, 6)]
        for a, b, c in combinacoes:
            if self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c] != " ":
                return True
        return False

    def alterar_turno(self):
        self.turno = "X" if self.turno == "O" else "O"

    def encerrar_jogo(self, mensagem):
        popup = Popup(
            title="",
            content=Label(text=mensagem, font_size=20, color=(1, 1, 1, 1)),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.bind(on_dismiss=lambda *args: self.app.voltar_interface_inicial())
        popup.open()


class Configuracao(BoxLayout):
    def __init__(self, app, **kwargs):
        super(Configuracao, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.app = app
        self.padding = 20
        self.spacing = 10
        self.add_widget(Label(text='Escolha seu símbolo:', font_size=20))
        self.simbolo_spinner = Spinner(text='X', values=('X', 'O'))
        self.add_widget(self.simbolo_spinner)
        self.add_widget(Label(text='Modo de Jogo:', font_size=20))
        self.modo_spinner = Spinner(text='Humano vs Humano', values=('Humano vs Humano', 'Humano vs IA'))
        self.add_widget(self.modo_spinner)
        self.add_widget(Label(text='Dificuldade:', font_size=20))
        self.dificuldade_spinner = Spinner(text='Fácil', values=('Fácil', 'Difícil'))
        self.add_widget(self.dificuldade_spinner)
        self.start_button = Button(text='Iniciar Jogo', font_size=20, size_hint=(1, 0.3))
        self.start_button.bind(on_press=self.iniciar_jogo)
        self.add_widget(self.start_button)

    def iniciar_jogo(self, instance):
        simbolo = self.simbolo_spinner.text
        modo_jogo = self.modo_spinner.text
        dificuldade = self.dificuldade_spinner.text
        self.app.iniciar_jogo(simbolo, modo_jogo, dificuldade)


class JogoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.configuracao = Configuracao(self)
        self.layout.add_widget(self.configuracao)
        return self.layout

    def iniciar_jogo(self, simbolo, modo_jogo, dificuldade):
        self.layout.clear_widgets()
        self.jogo = JogoDaVelha(simbolo=simbolo, modo_jogo=modo_jogo, dificuldade=dificuldade, app=self)
        self.layout.add_widget(self.jogo)

    def voltar_interface_inicial(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.configuracao)


if __name__ == '__main__':
    JogoApp().run()
