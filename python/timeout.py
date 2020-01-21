import signal
import logging

LOG = logging.getLogger(__name__)


class TimeOutException(Exception):
    """ An  error occurred """
    def __init__(self, message=None):
        self.message = message


def handle_alarm_signal(signum, stack):
    raise TimeOutException("timeout")


class timeout(object):
    def __init__(self, time):
        self.out_time = time

    def __enter__(self):
        signal.alarm(self.out_time)
        signal.signal(signal.SIGALRM, handle_alarm_signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        if exc_type:
            if exc_type is  TimeOutException:
                LOG.info("caught an Exception:%s" % exc_type)
            else:
                LOG.info("caught an TimeOut Exception")
