from kukulkan.config import UI

import kukulkan.gui.qt.QtGui as _qt


class SpinBox(_qt.QSpinBox):
    def __init__(self, *args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        self.setStyleSheet(
            '\n'.join(
                [
                "color: rgb({}, {}, {});".format(*UI.widgets.color),
                "background: rgb({}, {}, {});".format(*UI.widgets.background),
                ]
            )
        )


class DoubleSpinBox(_qt.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super(DoubleSpinBox, self).__init__(*args, **kwargs)
        self.setStyleSheet(
            '\n'.join(
                [
                "color: rgb({}, {}, {});".format(*UI.widgets.color),
                "background: rgb({}, {}, {});".format(*UI.widgets.background),
                ]
            )
        )


class LineEdit(_qt.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.setStyleSheet(
            '\n'.join(
                [
                "color: rgb({}, {}, {});".format(*UI.widgets.color),
                "background: rgb({}, {}, {});".format(*UI.widgets.background),
                ]
            )
        )

class ComboBox(_qt.QComboBox):
    def __init__(self, *args, **kwargs):
        super(ComboBox, self).__init__(*args, **kwargs)
        self.setStyleSheet(
            '\n'.join(
                [
                "color: rgb({}, {}, {});".format(*UI.widgets.color),
                "background: rgb({}, {}, {});".format(*UI.widgets.background),
                ]
            )
        )