import subprocess

def attack(cmpto, block_num):
    """
    Run MacSmasher on block_num.
    :param cmpto: The hash to search for.
    :block_num: The block to search.
    """

    return subprocess.check_output(['MacSmasher.exe', cmpto, str(block_num)])
