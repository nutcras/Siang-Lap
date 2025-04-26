import sys
from PyQt5.QtWidgets import QApplication
from ui import VoiceEncryptApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceEncryptApp()
    window.show()
    sys.exit(app.exec_())