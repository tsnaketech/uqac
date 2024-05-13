
# https://icones8.fr/icon/104704/donjons-et-dragons


from fbs_runtime.application_context.PySide2 import ApplicationContext

import sys

from package.main_windows import MainWindows

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindows(ctx=appctxt)
    window.setFixedSize(550, 600)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)