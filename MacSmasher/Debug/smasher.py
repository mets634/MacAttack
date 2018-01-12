import subprocess
from time import sleep


class Smasher(object):
    """
    A class that is used to check
    if a block of keys matches a certain
    hash. This class uses the subprocess MacAttack.exe.
    NOTE: MacAttack.exe must be in the same directory.
    """

    SHUTDOWN_CODE = -1

    INIT_FAIL_CODE = 1

    INIT_TIME = 2
    DEL_TIME = 1

    def __init__(self, cmpto):
        """
        Class ctor. Open subprocess.
        :param cmpto: The hash to search for.
        """

        self.proc = subprocess.Popen(
            'MacSmasher.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        sleep(INIT_TIME)  # give MacSmasher time to initialize

        # check for initialization error
        self.proc.poll()
        if self.proc.returncode == INIT_FAIL_CODE:
            raise RuntimeError("MacSmasher initialization failed")

        self.proc.stdin.write(cmpto)  # send string to compare to

    def __del__(self):
        """
        Class dtor. Close process.
        """

        self.proc.stdin.write(SHUTDOWN_CODE)  # send shutdown signal
        sleep(DEL_TIME)  # give subprocess time to terminate

        if self.proc.returncode is None:  # subprocess didn't terminate
            self.proc.kill()

    def attack(self, block):
        """
        Method to check for a match on a certain block.
        :param block: The index of the block to smash.
        :return: the index if the key within block. -1 if none found.
        """

        if self.proc.returncode is not None:
            raise RuntimeError("MacSmasher has terminated")

        '''TODO: Check for deadlock'''
        self.proc.stdin.write(block)  # send block number
        return self.proc.stdout.read()  # await output
