# -*- coding: utf-8 -*-
"""
Converted from Tkinter to PySide6
"""
import re
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QApplication,
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import QEventLoop, Qt, QTimer


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combinatoire test V1.8")
        self._central = QWidget()
        self.setCentralWidget(self._central)
        self._grid = QGridLayout(self._central)
        self._grid.setSpacing(2)
        self._close_callback = None
        self._destroying = False
        self.enum = 0
        self.etat = False
        self.windowPlace = []

    # ------------------------------------------------------------------
    # Tkinter compatibility shims
    # ------------------------------------------------------------------
    def title(self, t):
        self.setWindowTitle(t)

    def geometry(self, geom_str=None):
        """Tkinter-compatible: call with string to set size/pos, no arg to get QRect."""
        if geom_str is not None:
            self._set_geometry_str(geom_str)
            return
        return super().geometry()

    def _set_geometry_str(self, s):
        m = re.match(r'(\d+)x(\d+)(?:\+(-?\d+))?(?:\+(-?\d+))?', s)
        if m:
            w, h = int(m.group(1)), int(m.group(2))
            x = int(m.group(3)) if m.group(3) is not None else 26
            y = int(m.group(4)) if m.group(4) is not None else 26
            self.setGeometry(x, y, w, h)

    def configure(self, **kwargs):
        if 'bg' in kwargs:
            color = kwargs['bg']
            self.setStyleSheet(f"QMainWindow {{ background: {color}; }} "
                               f"QWidget#central {{ background: {color}; }}")
            self._central.setStyleSheet(f"background: {color};")

    def resizable(self, width=None, height=None):
        if width == 0 and height == 0:
            self.setFixedSize(self.size())

    def focus_force(self):
        self.activateWindow()
        self.raise_()

    def protocol(self, name, callback=None):
        if name == "WM_DELETE_WINDOW":
            self._close_callback = callback
        return callback

    def propagate(self, flag):
        pass

    def state(self):
        pass

    # ------------------------------------------------------------------
    # Event loop / lifecycle
    # ------------------------------------------------------------------
    def mainloop(self):
        self._local_loop = QEventLoop()
        self.show()
        self._local_loop.exec()

    def destroy(self):
        self._destroying = True
        self.hide()
        if hasattr(self, '_local_loop') and self._local_loop.isRunning():
            self._local_loop.quit()

    def closeEvent(self, event):
        if getattr(self, '_destroying', False):
            event.accept()
        elif self._close_callback is not None:
            self._close_callback()
            event.ignore()
        else:
            event.accept()
            if hasattr(self, '_local_loop') and self._local_loop.isRunning():
                self._local_loop.quit()

    # ------------------------------------------------------------------
    # Grid layout helpers (Tkinter compatibility)
    # ------------------------------------------------------------------
    def grid_rowconfigure(self, rows, weight=1):
        if isinstance(rows, (list, tuple)):
            for r in rows:
                self._grid.setRowStretch(r, weight)
        else:
            self._grid.setRowStretch(rows, weight)

    def grid_columnconfigure(self, cols, weight=1):
        if isinstance(cols, (list, tuple)):
            for c in cols:
                self._grid.setColumnStretch(c, weight)
        else:
            self._grid.setColumnStretch(cols, weight)

    # ------------------------------------------------------------------
    # Qt-side update helpers
    # ------------------------------------------------------------------
    def update(self):
        QApplication.processEvents()

    def update_idletasks(self):
        QApplication.processEvents()

    def after(self, ms, callback):
        QTimer.singleShot(ms, callback)

    def wait_window(self, dialog):
        """Block until dialog is closed (equivalent of Tkinter wait_window)."""
        dialog.exec()

    # ------------------------------------------------------------------
    # Styled popup helpers
    # ------------------------------------------------------------------
    def _show_ok_dialog(self, message, w=400, h=130):
        """Show a navy-styled blocking dialog with a single Ok button."""
        BG = "#0054A4"
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setFixedSize(w, h)
        dialog.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        lbl = QLabel(message)
        lbl.setStyleSheet(
            f"color:#FFFFFF; font-size:14px; font-weight:bold;"
            f" background:transparent; border:none;"
        )
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        btn = QPushButton("Ok")
        btn.setStyleSheet(
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:6px 28px; border-radius:6px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )
        btn.clicked.connect(dialog.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        dialog.exec()

    def _show_ok_cancel_dialog(self, message, w=400, h=130):
        """Show Ok/Cancel dialog. Returns True if Ok, False if Cancel."""
        BG = "#0054A4"
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setFixedSize(w, h)
        dialog.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        lbl = QLabel(message)
        lbl.setStyleSheet(
            f"color:#FFFFFF; font-size:14px; font-weight:bold;"
            f" background:transparent; border:none;"
        )
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        btn_ok = QPushButton("Ok")
        btn_ok.setStyleSheet(
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:6px 28px; border-radius:6px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setStyleSheet(
            "QPushButton { background:#FFFFFF; color:#000000; font-size:13px;"
            " padding:6px 20px; border-radius:6px; }"
            "QPushButton:hover    { background:#E0E0E0; }"
            "QPushButton:pressed  { background:#CCCCCC; }"
        )
        btn_cancel.clicked.connect(dialog.reject)
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        return dialog.exec() == QDialog.Accepted
