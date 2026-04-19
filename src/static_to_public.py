import os
import shutil


def static_to_public(static, public):
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    recursive_function(static, public)


def recursive_function(static, public):

    for name in os.listdir(static):
        y = os.path.join(static, name)
        if os.path.isfile(y):
            shutil.copy(y, public)
        else:
            x = os.path.join(public, name)
            os.mkdir(x)
            recursive_function(y, x)
