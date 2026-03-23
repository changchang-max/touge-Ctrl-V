import sys
import time
import pyautogui

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal


class TypingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        # 倒计时 5 秒
        for i in range(5, 0, -1):
            print(f"倒计时：{i}")
            time.sleep(1)

        lines = self.text.splitlines()

        for i, line in enumerate(lines):
            # 输入当前行
            pyautogui.write(line, interval=0.05)

            # 换行后立即回到新行行首，为下一行输入做准备
            if i < len(lines) - 1:
                pyautogui.press('enter')
                pyautogui.press('home')
                time.sleep(0.05)
            else:
                # 最后一行只换行，不需要 home
                pyautogui.press('enter')

        self.finished.emit()


class KeyboardTyper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("键盘自动输入工具")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入要自动打出的文本（支持多行）\n\n\n注：因为是模拟键盘输入，请提前切换到英文输入法！！！不兼容中文！！！")

        self.start_btn = QPushButton("开始")
        self.start_btn.clicked.connect(self.start_typing)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.start_btn)

    def start_typing(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "提示", "请输入要输出的文本")
            return

        QMessageBox.information(
            self,
            "提示",
            "请在 5 秒内将光标切换到目标输入位置\n倒计时结束后将自动开始输入"
        )

        self.start_btn.setEnabled(False)

        self.thread = TypingThread(text)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        self.start_btn.setEnabled(True)
        QMessageBox.information(self, "完成", "文本已输入完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyboardTyper()
    window.show()
    sys.exit(app.exec_())
