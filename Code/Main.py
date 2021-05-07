from PyQt5.QtWidgets import QApplication
import MainPane

if __name__ == "__main__" :
    import sys

    app = QApplication(sys.argv)
    main = MainPane.TetMainPane()
    main.show()
    sys.exit(app.exec_())
