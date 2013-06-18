"""Generic messaging functions.

.. module:: generic_msg
    :platform: Unix, Linux
        :synopsis: Generic messaging functions.

.. moduleauthor:: jneumann

.. note::
    None.

"""
# Built In
import sys
import random

# Third Party

# Custom

COLORS = {'red': '\033[31m',
          'green': '\033[32m',
          'yellow': '\033[33m',
          'blue': '\033[34m',
          'magenta': '\033[35m',
          'white': '\033[0m'}

def info(msg):
    """Information Messages

    Args:
        msg (str): The info message to output.

    """
    sys.stdout.write('%s[INFO] %s%s\n' % (COLORS['magenta'],
                                          msg,
                                          COLORS['white']))

    return

def error(msg):
    """Error Messages

    Args:
        msg (str): The error message to output.

    """
    sys.stderr.write('%s[ERROR] %s%s\n' % (COLORS['red'],
                                           msg,
                                           COLORS['white']))

    return

def warning(msg):
    """Warning Messages

    Args:
        msg (str): The warning message to output.

    """
    sys.stdout.write('%s[WARNING] %s%s\n' % (COLORS['yellow'],
                                             msg,
                                             COLORS['white']))

    return

def prompt(msg):
    """Prompt Messages

    Args:
        msg (str): The prompt message to output.

    .. note::
        It is up to the developer to create the call to read input.

    """
    sys.stdout.write('%s[USER_INPUT_REQUIRED] %s%s\n' % (COLORS['green'],
                                                         msg,
                                                         COLORS['white']))
    return

def final(msg):
    """Final Messages

    Args:
        msg (str): The final message to output. (Rainbow Colored!)

    """
    final_string = []
    for out in '[FINAL] ':
        final_string.append('%s%s' % (random.choice(COLORS.values()),
                                      out))
    for char in msg:
        final_string.append('%s%s' % (random.choice(COLORS.values()),
                                      char))
    sys.stdout.write('%s%s\n' % (''.join(final_string), COLORS['white']))

    return

