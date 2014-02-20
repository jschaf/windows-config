# -*- coding: utf-8 -*-
# Example init.py for documentation purposes
#
# Use this file as a template/example for creating an
# initialization/configuration script for PyCmd. Scripts are loaded and applied
# based on the following rules:
#
#  * If present, an init.py script in PyCmd's installation directory is
#    automatically executed and defines "global" (system-wide) settings
#
#  * If present, an init.py script in %APPDATA%\PyCmd is automatically executed
#    and defines "user" settings, possibly overriding the "global" ones
#
#  * An additional .py script can be specified using the '-i' switch on the
#    command line to define settings custom to a PyCmd session (possibly
#    overriding the "global" and "user" ones)
#
# This file lists all the configuration options supported by PyCmd, together
# with default values, explanations and various advice.
#


# An important thing to have in mind: this is a regular Python script that gets
# executed in PyCmd's Python context; therefore, you can do virtually anything
# you want here, like play a song, format your hard-disk or show some custom
# greeting:

# pycmd_public is a collection of public functions, constants and objects that
# PyCmd "exports" for use within init.py files; you can safely rely on these
# being maintained throughout following versions. The documentation for this module
# can be found in pycmd_public.html.
#
# Note that importing symbols from pycmd_public is optional, as PyCmd automatically
# makes them available within the init.py files; still, having them explicitly
# imported might help you get coding assistance from your Python environment
from pycmd_public import appearance, behavior, abbrev_path        # Redundant

# Color configuration is performed by including color specification sequences
# (defined by pycmd_public.color) in your strings, similarly to the ANSI escape
# sequences.
#
# "absolute" color specifications will result in the same color being used no
# matter the current color; some examples are color.Fore.YELLOW, color.Fore.SET_RED,
# color.Back.CLEAR_BRIGHT.
#
# "relative" color options define the color to use in terms of the current color;
# examples: color.Fore.TOGGLE_RED, color.Fore.TOGGLE_BRIGHT.
#
# You will notice that relative specifications are preferred in the default
# settings -- this is in order to make PyCmd work reasonably on any console color
# scheme. The absolute specs are clearer and easier to use, though, you can go
# probably go with them for your customizations.
#
# The console's default color attributes are available as color.Fore.DEFAULT and
# color.Back.DEFAULT.
import re
import os
from pycmd_public import color        # Redundant

# The color of the regular user text (relative to the console's default)
#
# Note that this defines only the attributes of the user-typed text, *not* the
# default attributes of the console (i.e. the console's background or the output
# of the executed commands); use the console configuration dialog to change those.
#
# The default value is the console's default:
#    appearance.colors.text = ''
appearance.colors.text = ''

# The color of the prompt (relative to the console's default); note that you can
# always override this if you define a custom prompt function -- see below
#
# The default value inverts the brightness (to make it stand out it from  regular
# console text):
#    appearance.colors.prompt = color.Fore.TOGGLE_BRIGHT
appearance.colors.prompt = color.Fore.TOGGLE_BRIGHT

# The color of text selected for copy/cut operations (relative to the regular
# user text as configured above)
#
# The default value inverts the background and the foreground
#    appearance.colors.selection = (color.Fore.TOGGLE_RED +
#                               color.Fore.TOGGLE_GREEN +
#                               color.Fore.TOGGLE_BLUE +
#                               color.Back.TOGGLE_RED +
#                               color.Back.TOGGLE_GREEN +
#                               color.Back.TOGGLE_BLUE)
appearance.colors.selection = (color.Fore.TOGGLE_RED +
                               color.Fore.TOGGLE_GREEN +
                               color.Fore.TOGGLE_BLUE +
                               color.Back.TOGGLE_RED +
                               color.Back.TOGGLE_GREEN +
                               color.Back.TOGGLE_BLUE)

# The color of the current search filter during a history search (relative to the
# regular user text as configured above)
#
# The default is to highlight the filter by altering both background and the
# foreground:
#   appearance.colors.search_filter = (color.Back.TOGGLE_RED +
#                                      color.Back.TOGGLE_BLUE +
#                                      color.Fore.TOGGLE_BRIGHT)
appearance.colors.search_filter = (color.Back.TOGGLE_RED +
                                   color.Back.TOGGLE_BLUE +
                                   color.Fore.TOGGLE_BRIGHT)

# The color of the matched substring(s) when displaying completion alternatives
# (relative to the console's default color)
#
# The default value highlights the matched substrings by toggling their RED bit:
#    appearance.colors.completion_match = color.Fore.TOGGLE_RED
appearance.colors.completion_match = color.Fore.TOGGLE_RED

# The color of the current directory in the directory history listing (relative to
# the console's default color)
#
# The default is to obtain an "inverted" effect by toggling the brightness of the
# foreground and background:
#    appearance.colors.dir_history_selection = (color.Fore.TOGGLE_BRIGHT +
#                                               color.Back.TOGGLE_BRIGHT)
appearance.colors.dir_history_selection = (color.Fore.TOGGLE_BRIGHT +
                                           color.Back.TOGGLE_BRIGHT)

def has_admin():
    import os
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot',
                                                          'C:\windows'),
                                           'temp']))
        except:
            return (os.environ['USERNAME'],False)
        else:
            return (os.environ['USERNAME'],True)
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (os.environ['SUDO_USER'],True)
        else:
            return (os.environ['USERNAME'],False)

class promptify(object):
    def __init__(self, addon_prompt):
        self._addon_prompt = addon_prompt

    def __call__(self, prompt):
        def wrapped_prompt(*args):
            return self._addon_prompt() + prompt(*args)
        return wrapped_prompt

# Custom prompt function, see below for comments on appearance.prompt
def git_prompt_addon():
    """
    Custom prompt that displays the name of the current git branch in addition
    to the typical "abbreviated current path" PyCmd prompt.

    Requires git & grep to be present in the PATH.
    """
    # Many common modules (sys, os, subprocess, time, re, ...) are readily
    # shipped with PyCmd, you can directly import them for use in your
    # configuration script. If you need extra modules that are not bundled,
    # manipulate the sys.path so that they can be found (just make sure that the
    # version is compatible with the one used to build PyCmd -- check
    # README.txt)
    import subprocess

    stdout = subprocess.Popen(
        'git branch | grep "^*"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=-1).communicate()[0]
    branch_name = stdout.strip(' \n\r*')

    # The current color setting is defined by appearance.colors.prompt
    prompt = ''
    if branch_name != '':
        blue = color.Fore.TOGGLE_BLUE
        prompt += '{}[{}]{} '.format(blue, branch_name, blue)

    return prompt

def conda_prompt_addon():
    env = os.environ.get('CONDA_DEFAULT_ENV')
    prompt = ""
    if env:
        prompt += color.Fore.TOGGLE_GREEN
        prompt += "[{env}] ".format(env=env)
        prompt += color.Fore.TOGGLE_GREEN
    return prompt


@promptify(conda_prompt_addon)
@promptify(git_prompt_addon)
def prompt():
    # Use a tilde to represent our home dir
    path = re.sub(r"C:\\U\\j(oe)?", "~", abbrev_path())
    username, is_admin = has_admin()
    path += '\n'
    if is_admin:
        path += color.Fore.TOGGLE_RED
        path += "# "
        path += color.Fore.TOGGLE_RED
    else:
        path += "$ "
    return path

# Define a custom prompt function.
#
# This is called by PyCmd whenever a prompt is to be displayed. It should return
# a string to be shown as a prompt.
#
# Before the returned string is printed, the text color is set to
# appearance.colors.prompt; but you can always alter it or add more complex
# coloring by embedding color specifications in the returned string (like we do
# in our example git_prompt).
#
# The default is the typical "abbreviated path" prompt:
#       appearance.prompt = pycmd_public.abbrev_path_prompt
appearance.prompt = prompt


# Make PyCmd be "quiet", i.e. skip its welcome and goodbye messages
#
# Note that even if this is set to True, you can still override it using the
# '-q' (quiet) flag on the command line.
#
# The default is False, i.e. the splash messages are shown:
#       behavior.quiet_mode = False
behavior.quiet_mode = True


# Change the way PyCmd handles Tab-completion
#
# Currently, the only accepted (and, of course, default) value is 'bash', giving
# the typical bash-like completion.
#
behavior.completion_mode = 'bash'


# Remember, you can do whatever you want in this Python script!
#
# Also note that you can directly output colored text via the color
# specifications.
