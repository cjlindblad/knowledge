import sys
import tempfile
import os
import subprocess


def get_text_from_editor():
    EDITOR = os.environ.get('EDITOR', 'vim')

    text = ''

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([EDITOR, tf.name])
        text = open(tf.name, 'r').read()

    return text
