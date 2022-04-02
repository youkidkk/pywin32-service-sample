import logging
import os
import socket
import sys
from threading import Event, Thread

import servicemanager
import win32event
import win32service
import win32serviceutil
import yaml

from main import Main

logger = logging.getLogger(__name__)


class PyWin32Sample(win32serviceutil.ServiceFramework):
    _svc_name_ = "pywin32_sample"
    _svc_display_name_ = "PyWin32 Sample Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.main_stop_event = Event()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logger.info(f"{self._svc_display_name_} を停止します。")
        self.main_stop_event.set()

    def SvcDoRun(self):
        logger.info(f"{self._svc_display_name_} を開始します。")
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.main()

    def main(self):
        main_thread = Thread(target=Main(self.main_stop_event).run)
        main_thread.start()
        while not self.main_stop_event.wait(timeout=10):
            pass
        main_thread.join()
        logger.info(f"{self._svc_display_name_} を停止しました。")
        return


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # サービス起動の場合はカレントディレクトリが異なるため、
        # 実行ファイルの親ディレクトリに移動
        os.chdir(os.path.dirname(sys.argv[0]))

        with open("configs/log_conf.yml") as f:
            logging.config.dictConfig(yaml.unsafe_load(f.read()))
        logger = logging.getLogger(__name__)
        logger.info(f"cwd: {os.getcwd()}")

        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PyWin32Sample)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PyWin32Sample)
