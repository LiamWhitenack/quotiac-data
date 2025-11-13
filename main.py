import sys

from PySide6.QtWidgets import QApplication

from quotiac_sandbox.gui import MainWindow

# from quotiac_sandbox.utils.host_staging_data import serve_json_dict

# update_json = serve_json_dict(port=6942)
app = QApplication(sys.argv)
window = MainWindow()
window.show()
# window.showMaximized()
sys.exit(app.exec())
