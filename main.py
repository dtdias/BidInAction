from PySide6.QtWidgets import QApplication, QMainWindow
from interface_ui import Ui_interface

class Janela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_interface()
        self.ui.setupUi(self)

        # Exemplo de interação com widgets existentes
        self.ui.lineEdit.setPlaceholderText("Digite seu nome aqui")
        self.ui.comboBox.addItems(["Opção 1", "Opção 2", "Opção 3"])
        self.ui.comboBox_2.addItems(["Valor A", "Valor B", "Valor C"])

        # Exemplo de leitura dos valores (pode ser adaptado para botão depois)
        self.ui.lineEdit.textChanged.connect(self.exibir_valores)

    def exibir_valores(self):
        texto = self.ui.lineEdit.text()
        opcao1 = self.ui.comboBox.currentText()
        opcao2 = self.ui.comboBox_2.currentText()
        print(f"Texto: {texto} | Opção 1: {opcao1} | Opção 2: {opcao2}")

if __name__ == "__main__":
    app = QApplication([])
    janela = Janela()
    janela.show()
    app.exec()
