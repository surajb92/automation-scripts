import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class CalendarPopup(QtWidgets.QWidget):
    def __init__(self, calendar, parent=None):
        super().__init__(parent, QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(calendar)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(300, 200)  # Match previous calendar size
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tray_menu_open = False
    def focusOutEvent(self, event):
        # Don't hide menu unless mouse is clicked elsewhere, right click also exempted
        if event.reason() == QtCore.Qt.ActiveWindowFocusReason:
            # don't hide if context menu open
            if self.tray_menu_open:
                self.tray_menu_open = False
            else:
                self.hide()
        else:
            print("hiding")
            self.hide()
        super().focusOutEvent(event)

    def tray_menu(self):
        if not self.tray_menu_open:
            self.tray_menu_open = True
        print("Tray menu status: ",self.tray_menu_open)
    def closeEvent(self, event):
        print("Close event triggered")
        event.accept()  # Allow closing, or use event.ignore() to prevent if needed
        super().closeEvent(event)

class SchedulerApp:
    def __init__(self):
        # Create app, keep it running in bg even if window closed
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Calendar dialog
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar_popup = CalendarPopup(self.calendar)
        self.calendar.setGridVisible(True)
        self.calendar.show()

        # Wrap calendar in a QWidget for the menu
        calendar_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(calendar_widget)
        layout.addWidget(self.calendar)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create system tray icon
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon.fromTheme("dialog-information"))
        self.tray_icon.setToolTip("Task Scheduler")
        self.tray_icon.show()
        
        # Right-click context menu
        self.tray_menu = QtWidgets.QMenu()
        self.quit_action = self.tray_menu.addAction("Quit")
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Connect actions to functions
        self.tray_icon.activated.connect(self.handle_tray_click)
        self.tray_menu.aboutToShow.connect(self.calendar_popup.tray_menu)
        #self.tray_menu.aboutToHide.connect(self.calendar_popup.tray_menu)
        self.quit_action.triggered.connect(self.quit_app)

        # Notification when app is launched
        self.tray_icon.showMessage(
            "Task Scheduler",
            "Scheduler is now running in the background",
            QtGui.QIcon.fromTheme("dialog-information"),
            3000
        )
    def handle_tray_click(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger : # i.e. if left-clicked
            tray_pos = self.tray_icon.geometry().topLeft()
            #screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
            #tray_pos = screen.bottomRight() - QtGui.QCursor.pos() # 
            if self.calendar_popup.isVisible():
                self.calendar_popup.hide()
            else:
                tray_pos = QtGui.QCursor.pos() + QtCore.QPoint(10, 10)
                self.calendar_popup.move(tray_pos)
                self.calendar_popup.show()
                self.calendar_popup.raise_()
                self.calendar_popup.setFocus()
                print(f"Popup shown at {tray_pos.x()},{tray_pos.y()}")
    
    def quit_app(self):
        self.tray_icon.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = SchedulerApp()
    app.run()
