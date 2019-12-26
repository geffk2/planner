from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QCheckBox
from PyQt5 import uic
from planner import db_model, new_reminder_window
from planner.__main__ import PATH
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH + '\\ui\\main_window.ui', self)

        self.setWindowTitle('Планировщик')
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Имя', 'Описание', 'Дата и время', 'Сделано'])
        self.groupByDone.clicked.connect(self.show_reminders)
        self.mode_switch.buttonClicked.connect(self.show_reminders)
        self.add_button.clicked.connect(self.add_reminder)
        self.about_button.clicked.connect(self.show_about)

        self.show_reminders()

    def show_reminders(self):
        group_by_done = self.groupByDone.isChecked()
        if self.radio_alltime.isChecked():
            data = db_model.get_all_entries(group_by_done)
        else:
            data = db_model.get_entries_by_date(self.calendarWidget.selectedDate())
        self.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(data[i][1])))
            if data[i][2] is not None:
                self.tableWidget.setItem(i, 1, QTableWidgetItem(data[i][2]))
            if data[i][3] is not None:
                date = datetime.datetime.fromtimestamp(data[i][3])
                self.tableWidget.setItem(i, 2, QTableWidgetItem(date.strftime('%A, %d. %B %Y %H:%M')))
            checkbox = QCheckBox()
            checkbox.setObjectName(data[i][0])
            checkbox.clicked.connect(self.task_checked)
            if data[i][4] == 'True':
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            self.tableWidget.setCellWidget(i, 3, checkbox)

    def task_checked(self):
        entry_id = self.sender().objectName()
        new_state = self.sender().isChecked()
        db_model.update_entry(entry_id, done=new_state)
        self.show_reminders()

    def add_reminder(self):
        self.reminder_window = new_reminder_window.NewReminderWindow()
        self.reminder_window.show()

    def show_about(self):
        self.about_window = QMainWindow()
        uic.loadUi(PATH + '\\ui\\about.ui', self.about_window)
        self.about_window.setWindowTitle('Справка')
        self.about_window.label.setText('Краткая справка по программе "планировщик":\n'
                                        '- В главном окне слева находится таблица, в которую выводятся напоминания, '
                                        'справа - календарь для выбора даты, опции отображения и сортировки и '
                                        'кнопка для добавления нового напоминания.\n- Если выбрана опция "по дате", '
                                        'будут отображаться все напоминания за выбранную на календаре дату.'
                                        '(отсортированы по времени)\n- Если выбрана опция "за все время", будут '
                                        'отображаться все напоминания за все время. (отсортированы по дате и времени)\n'
                                        '- При нажатии на кнопку "Добавить напоминание", появится диалог, в котором'
                                        ' обязательно требуется ввести название события(время автоматически установится'
                                        ' на текущее) и нажать на кнопку чтобы добавить новое напоминание')
        self.about_window.show()
