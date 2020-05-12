import sys
import tempfile
import os
import subprocess


def get_text_from_editor():
    EDITOR = os.environ.get('EDITOR', 'vim')

    initial_content = b'title: \ncategory: \ncontent: '
    text = ''

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_content)
        tf.flush()
        subprocess.call([EDITOR, tf.name])
        text = open(tf.name, 'r').read()

    return text
