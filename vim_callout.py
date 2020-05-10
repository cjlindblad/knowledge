import sys
import tempfile
import os
import subprocess

EDITOR = os.environ.get('EDITOR', 'vim')

initial_message = ""

text = ''

with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    subprocess.call([EDITOR, tf.name])
    text = open(tf.name, 'r').read()
