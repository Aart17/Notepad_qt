from PyQt5.Qt import *

import images


class Printer(QMainWindow):
    def __init__(self):
        super(Printer, self).__init__()
        self.setWindowTitle('Document Printer')
        self.setWindowIcon(QIcon(':/images/printer_icon.png'))

        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)

        self.settings = QSettings("Printer", "Тест1")

        self.add_thumbnail_tb()
        self.add_jumplist()
        self.add_actions()      # Create actions for toolbar button
        self.add_toolbar()
        self.use_settings()     # Save position and text

    def font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)

    def color_dialog(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    def handle_settings(self):
        qopt = QPageSetupDialog(self)
        qopt.exec_()

    def handle_open(self):
        path = QFileDialog.getOpenFileName(
            self, 'Open file', '',
            'Text files (*.txt)')[0]
        if path:
            file = QFile(path)
            if file.open(QIODevice.ReadOnly):
                stream = QTextStream(file)
                text = stream.readAll()
                self.editor.setPlainText(text)
                file.close()

    def handle_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def handle_preview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handle_to_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Create PDF', filter='PDF files (*.pdf)')
        fn = str(fn)
        if fn != '':
            if QFileInfo(fn).suffix() != '.pdf':
                fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.editor.document().print_(printer)

    def handle_save_txt(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Save txt file')
        if fn != '':
            if QFileInfo(fn).suffix() != '.txt':
                fn += '.txt'
            with open(fn, 'w', encoding='UTF-8') as file:
                file.write(self.editor.toPlainText())

    def about(self):
        QMessageBox.about(self, "About App",
                          "The <b>App</b> for editing text documents, "
                          "editing font, font-size, font-color and "
                          "print this document with PyQt.")

    def add_actions(self):
        self.open_act = QAction(QIcon(':/images/file.png'), 'Open File', triggered=self.handle_open,
                                shortcut=QKeySequence.Save)

        self.save_txt_act = QAction(QIcon(':/images/save_file.png'), 'Save to txt file', triggered=self.handle_save_txt,
                                    shortcut=QKeySequence.Save)

        self.to_pdf_act = QAction(QIcon(':/images/pdf.png'), 'Create PDF File', triggered=self.handle_to_pdf)

        self.print_act = QAction(QIcon(':/images/printer.png'), 'Print', triggered=self.handle_print)

        self.settings_act = QAction(QIcon(':/images/settings.png'), 'Printer settings',
                                    triggered=self.handle_settings)

        self.preview_act = QAction(QIcon(':/images/eye.png'), 'Preview', triggered=self.handle_preview)

        self.font_act = QAction(QIcon(':/images/font_btn.png'), 'Change Font', triggered=self.font_dialog)

        self.color_act = QAction(QIcon(':/images/color.png'), 'Change Color', triggered=self.color_dialog)

        self.about_act = QAction(QIcon(':/images/about.png'), 'About App', triggered=self.about)

        self.aboutQt_act = QAction(QIcon(":/images/qt.png"), "AboutQt")
        self.aboutQt_act.triggered.connect(QApplication.instance().aboutQt)

    def add_toolbar(self):
        self.toolbar_file = self.addToolBar('File')
        self.toolbar_file.addAction(self.open_act)
        self.toolbar_file.addAction(self.save_txt_act)
        self.toolbar_file.addAction(self.to_pdf_act)

        self.toolbar_print = self.addToolBar('Print Menu')
        self.toolbar_print.addAction(self.print_act)
        self.toolbar_print.addAction(self.settings_act)
        self.toolbar_print.addAction(self.preview_act)

        self.toolbar_edit = self.addToolBar('Edit')
        self.toolbar_edit.addAction(self.font_act)
        self.toolbar_edit.addAction(self.color_act)

        self.toolbar_help = self.addToolBar('Help')
        self.toolbar_help.addAction(self.about_act)
        self.toolbar_help.addAction(self.aboutQt_act)

    def add_jumplist(self):
        jump_ls = QWinJumpList(self)
        jump_ls.clear()

        recent = jump_ls.recent()
        recent.setVisible(True)

        custom_jls = QWinJumpListCategory('Instruments')

        item2 = QWinJumpListItem(QWinJumpListItem.Type.Link)
        item2.setTitle(r'Wordpad')
        item2.setFilePath(r'C:\Program Files\Windows NT\Accessories\wordpad')
        custom_jls.addItem(item2)
        custom_jls.setVisible(True)

        item4 = QWinJumpListItem(QWinJumpListItem.Type.Link)
        item4.setTitle(r'notepad')
        item4.setFilePath(r'C:\Windows\system32\notepad')
        custom_jls.addItem(item4)
        custom_jls.setVisible(True)

        item5 = QWinJumpListItem(QWinJumpListItem.Type.Link)
        item5.setTitle(r'Факсы и сканеры')
        item5.setFilePath(r'C:\Windows\system32\WFS')
        custom_jls.addItem(item5)
        custom_jls.setVisible(True)

        jump_ls.addCategory(custom_jls)

    def add_thumbnail_tb(self):
        self.tn_tb = QWinThumbnailToolBar(self)

        file_btn = QWinThumbnailToolButton(self)
        file_btn.setIcon(QIcon(':/images/file.png'))
        file_btn.setToolTip('File')
        file_btn.setDismissOnClick(True)
        file_btn.clicked.connect(self.handle_open)

        sep_btn = QWinThumbnailToolButton(self)
        sep_btn.setEnabled(False)
        sep_btn.setFlat(True)

        about_app_btn = QWinThumbnailToolButton(self)
        about_app_btn.setIcon(QIcon(':/images/about.png'))
        about_app_btn.setToolTip('About app')
        about_app_btn.setDismissOnClick(True)
        about_app_btn.clicked.connect(self.about)

        about_qt_btn = QWinThumbnailToolButton(self)
        about_qt_btn.setIcon(QIcon(':/images/qt.png'))
        about_qt_btn.setToolTip('About qt')
        about_qt_btn.setDismissOnClick(True)
        about_qt_btn.clicked.connect(QApplication.instance().aboutQt)

        self.tn_tb.addButton(file_btn)
        self.tn_tb.addButton(sep_btn)
        self.tn_tb.addButton(about_app_btn)
        self.tn_tb.addButton(about_qt_btn)

    def use_settings(self):
        is_have_text = False
        is_position_changed = False
        if self.settings.contains('Местоположение'):
            self.setGeometry(self.settings.value('Местоположение'))
            is_position_changed = True
        else:
            self.resize(640, 480)
        if self.settings.contains('Текст'):
            self.editor.setText(self.settings.value('Текст'))
            is_have_text = True
        else:
            self.resize(640, 480)
        if is_have_text or is_position_changed is True:
            self.settings.clear()

    def showEvent(self, e):
        self.tn_tb.setWindow(self.windowHandle())

    def closeEvent(self, event):
        text = self.editor.toPlainText()
        self.settings.setValue("Местоположение", self.geometry())
        self.settings.setValue("Текст", text)
        self.settings.sync()

    def align(self, desk, win):
        x = (desk.width() - win.width()) // 2
        y = (desk.height() - win.height()) // 2
        self.move(x, y)


if __name__ == '__main__':
    from sys import argv, exit

    app = QApplication(argv)
    desktop = QApplication.desktop()
    window = Printer()
    window.show()
    exit(app.exec_())

