from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDateTime
from PyQt5 import uic
from planner import app
from planner.__main__ import PATH
import planner.db_model


class NewReminderWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(PATH + '\\ui\\new_reminder_window.ui', self)
        self.setWindowTitle('Новое напоминание')
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.reminder_name.textEdited.connect(self.name_edited)
        self.pushButton.clicked.connect(self.button_clicked)

    def button_clicked(self):
        planner.db_model.add_entry(self.reminder_name.text(), self.dateTimeEdit.dateTime().toSecsSinceEpoch(),
                                   description=self.reminder_description.text())
        app.main_window.show_reminders()
        self.close()

    def name_edited(self):
        if self.reminder_name.text().strip() != ' ':
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
