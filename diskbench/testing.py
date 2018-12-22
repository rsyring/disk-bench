import json
import pathlib

data_dpath = pathlib.Path(__file__).parent.joinpath('tests', 'data')


def load_json(fname):
    with data_dpath.joinpath(fname).open() as fo:
        return json.load(fo)


def read(fname):
    with data_dpath.joinpath(fname).open() as fo:
        return fo.read()
