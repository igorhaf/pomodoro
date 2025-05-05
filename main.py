import sys  # Biblioteca padrão para interagir com o sistema (encerrar o app, etc)

# Importa os widgets gráficos básicos do PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# Importa o temporizador (usado para atualizar o relógio a cada segundo)
from PyQt5.QtCore import QTimer

# Classe principal da janela do Pomodoro
class PomodoroTimer(QWidget):  # QWidget é a classe base para qualquer componente visual
    def __init__(self):
        super().__init__()  # Inicializa o QWidget base

        # Configurações básicas da janela
        self.setWindowTitle("Relógio Pomodoro")  # Título da janela
        self.setGeometry(100, 100, 400, 400)      # Posição e tamanho (x, y, largura, altura)

        # Tempo padrão do Pomodoro em segundos
        self.work_duration = 25 * 60  # 25 minutos
        self.break_duration = 5 * 60  # 5 minutos
        self.time_left = self.work_duration  # Tempo restante atual
        self.on_break = False  # Flag para saber se estamos no intervalo

        # Cria um layout vertical para empilhar os componentes
        layout = QVBoxLayout()

        # Cria o rótulo do tempo (timer)
        self.label = QLabel(self.format_time(self.time_left), self)  # Mostra tempo restante
        self.label.setStyleSheet("font-size: 60px; text-align: center")  # Estilo CSS
        self.label.setAlignment(Qt.AlignCenter)  # Centraliza o texto

        # Cria o rótulo para mostrar se está em modo trabalho ou pausa
        self.status = QLabel("Modo: Trabalho", self)
        self.status.setStyleSheet("font-size: 60px; text-align: center")
        self.status.setAlignment(Qt.AlignCenter)

        # Botão de iniciar o Pomodoro
        self.start_button = QPushButton("Iniciar")
        self.start_button.setStyleSheet("font-size: 50px; height: 60px; text-align: center")
        self.start_button.clicked.connect(self.start_timer)  # Ao clicar, chama start_timer()

        # Botão para reiniciar o Pomodoro
        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.setStyleSheet("font-size: 50px; height: 60px; text-align: center")
        self.reset_button.clicked.connect(self.reset_timer)  # Ao clicar, chama reset_timer()

        # Adiciona os elementos no layout
        layout.addWidget(self.label)
        layout.addWidget(self.status)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

        # Define o layout na janela
        self.setLayout(layout)

        # Cria o temporizador que chama uma função a cada intervalo de tempo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)  # A cada "tick", chama update_timer()

    # Formata o tempo em minutos:segundos (ex: 25:00)
    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"  # Preenche com zero à esquerda

    # Inicia o timer (chama update_timer a cada 1000ms = 1 segundo)
    def start_timer(self):
        self.timer.start(1000)

    # Atualiza o contador a cada segundo
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1  # Reduz o tempo restante
            self.label.setText(self.format_time(self.time_left))  # Atualiza o texto do timer
        else:
            self.timer.stop()  # Para o timer ao chegar em 0
            self.switch_mode()  # Troca entre trabalho e pausa

    # Troca entre modo trabalho e pausa
    def switch_mode(self):
        self.on_break = not self.on_break  # Inverte o modo atual
        if self.on_break:
            self.status.setText("Modo: Pausa")
            self.time_left = self.break_duration  # Reinicia para tempo de pausa
        else:
            self.status.setText("Modo: Trabalho")
            self.time_left = self.work_duration  # Reinicia para tempo de trabalho
        self.label.setText(self.format_time(self.time_left))  # Atualiza o display

    # Reinicia o timer para o início do ciclo de trabalho
    def reset_timer(self):
        self.timer.stop()  # Para o timer
        self.on_break = False  # Volta para modo trabalho
        self.status.setText("Modo: Trabalho")
        self.time_left = self.work_duration  # Reseta o tempo
        self.label.setText(self.format_time(self.time_left))

# Ponto de entrada da aplicação
if __name__ == "__main__":
    from PyQt5.QtCore import Qt  # Importação extra usada para alinhamento de texto

    app = QApplication(sys.argv)  # Inicializa o aplicativo Qt
    window = PomodoroTimer()  # Cria a janela do Pomodoro
    window.show()  # Mostra a janela na tela
    sys.exit(app.exec_())  # Entra no loop principal do PyQt e espera eventos
