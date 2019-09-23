from Orange.widgets.widget import OWWidget, Output
from Orange.widgets.settings import Setting
from Orange.widgets import gui

class TestImportPackage(OWWidget):
    # Widget's name as displayed in the canvas
    name = "Test Import Package"
    # Short widget description
    description = "test to include a new package"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "icons/test.svg"

    test = "import succed"

    # Widget's outputs; here, a single output named "Number", of type int
    class Outputs:
        check = Output("Validation", str)

    def __init__(self):
        super.__init__()

        self.Outputs.check.send(self.test)
