from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText

class TestWidget(BaseWidget):
    def __init__(self):
        super(TestWidget, self).__init__()
        _test_txt_box = ControlText('sample_txt')
        _test_txt_box.show()
