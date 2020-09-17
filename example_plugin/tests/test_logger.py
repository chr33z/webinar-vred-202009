import unittest
import sys, os

def modules_path():
    scriptPath = os.path.realpath(__file__)
    return os.path.normpath(os.path.join(scriptPath, os.pardir, os.pardir, "modules"))

class TestLogger(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLogger, self).__init__(*args, **kwargs)
        sys.path.append(modules_path())

    def test_logger_info(self):
        from logger import info

        message = info("This is a test.", self)
        self.assertEqual(message, "[TestLogger] This is a test.")

        message = info("This is a test.")
        self.assertEqual(message, "This is a test.")

    def test_logger_debug(self):
        from logger import debug

        message = debug("This is a debug message.", self)
        self.assertEqual(message, "[Debug][L:26] [TestLogger] This is a debug message.")

        message = debug("This is a debug message.")
        self.assertEqual(message, "[Debug][L:29] This is a debug message.")

    def test_logger_error(self):
        from logger import error

        message = error("This is an error message.", self)
        self.assertEqual(message, "[Error][TestLogger] This is an error message.")

        message = error("This is an error message.")
        self.assertEqual(message, "[Error]This is an error message.")

# def runTests():
    
#     unittest.main(verbosity=3)

# if __name__ == '__main__':
#     runTests()

