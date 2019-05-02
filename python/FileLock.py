import os


class FileLock(object):
    """Advisory file based locking.  This should be reasonably cross platform
       and also work over distributed file systems."""
    def __init__(self, fno, exclusive=False):
        # fno is FileObject
        self.fp = fno
        self.locked = False

        if os.name == 'nt':
            import msvcrt

            def lock(self):
                msvcrt.locking(self.fp, msvcrt.LK_LOCK, 1)
                self.locked = True

            def unlock(self):
                if self.locked:
                    msvcrt.locking(self.fp, msvcrt.LK_UNLCK, 1)
                self.locked = False

        else:
            import fcntl

            def lock(self):
                operation = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
                fcntl.lockf(self.fp, operation)
                self.locked = True

            def unlock(self):
                if self.locked:
                    fcntl.lockf(self.fp, fcntl.LOCK_UN)
                self.locked = False

        FileLock.lock = lock
        FileLock.unlock = unlock

# test for FileLock
#f = open('tty','w')
#fn = FileLock(f,True)
#fn.lock()
# import time
#time.sleep(500)
#print("hello world")
#fn.unlock()
