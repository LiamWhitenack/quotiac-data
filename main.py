import sys
from codiac_sandbox.gui import MainWindow
from PySide6.QtWidgets import QApplication

# from codiac_sandbox.utils.host_staging_data import serve_json_dict

# update_json = serve_json_dict(port=6942)
app = QApplication(sys.argv)
window = MainWindow()
window.show()
# window.showMaximized()
sys.exit(app.exec())
