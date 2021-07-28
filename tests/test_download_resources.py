import pytest
import tempfile
import os
import pathlib
from page_loader.page_loader import download_resources, create_download_dir
from os.path import split, join
import requests
from shutil import copyfile


URL = 'https://ru.hexlet.io'
NETLOC = 'ru.hexlet.io'
FIXTURES_PATH = 'fixtures/resources_download_test'
HTML = 'ru-hexlet-io-courses.html'
LOADING_DIR = 'ru-hexlet-io-courses_files'
DATA = [
    (
        '/assets/application.css',
        'application.css',
        'ru-hexlet-io-assets-application.css'
    ),
    (
        '/courses',
        'courses.html',
        'ru-hexlet-io-courses.html'
    ),
    (
        '/assets/professions/nodejs.png',
        'nodejs.png',
        'ru-hexlet-io-assets-professions-nodejs.png'
    ),
    (
        '/packs/js/runtime.js',
        'runtime.js',
        'ru-hexlet-io-packs-js-runtime.js'
    ),
]


def read(file_path):
    with open(file_path, 'r') as f:
        file = f.read()
    return file


def read_in_bytes(file_path):
    with open(file_path, 'rb') as f:
        file = f.read()
    return file


def get_fixture_path(fixture_name):
    return os.path.join(
        pathlib.Path(__file__).absolute().parent,
        FIXTURES_PATH,
        fixture_name
    )


def test_download_res_mock_to_del(requests_mock):
    requests_mock.get(URL, text='data')
    assert 'data' == requests.get(URL).text


def test_download_resources(requests_mock):
    with tempfile.TemporaryDirectory() as tmp_directory:
        for items in DATA:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            requests_mock.get(
                URL + subpath,
                content=read_in_bytes(fixture_path))
        html_path = get_fixture_path(HTML)
        copy_html_path = join(tmp_directory, split(html_path)[1])
        copyfile(html_path, copy_html_path)
        download_dir = create_download_dir(copy_html_path)
        download_resources(copy_html_path, download_dir, URL, NETLOC)

        for items in DATA:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            assert read_in_bytes(
                fixture_path
            ) == read_in_bytes(
                f'{tmp_directory}/{LOADING_DIR}/{loaded_file}'
            )
        assert read(
            get_fixture_path(f'after/{HTML}')
        ) == read(
                f'{tmp_directory}/{HTML}'
            )


def test_download_resources_exceptions():
    # TODO discuss with the mentor
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(FileNotFoundError):
            download_resources('', tmp_directory, URL, NETLOC)

    with pytest.raises(FileNotFoundError):
        html_path = get_fixture_path(HTML)
        download_resources(html_path, '/undefined', URL, NETLOC)
