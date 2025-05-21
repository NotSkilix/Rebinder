from script.main_widget import MainWidget, sys, QtWidgets

def main():
    print("Executing...")

    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(800,800)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()