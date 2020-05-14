import sys
import tempfile
import os
import subprocess

default_initial_content = 'title: \ncategory: \ncontent: '


def get_text_from_editor(initial_content=default_initial_content):
    EDITOR = os.environ.get('EDITOR', 'vim')

    text = ''

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(bytes(initial_content, 'utf-8'))
        tf.flush()
        subprocess.call([EDITOR, tf.name])
        text = open(tf.name, 'r').read()

    return text
