import tempfile
import os
import pathlib
from page_loader.page_loader import download_resources
from os.path import split, join
import requests
from shutil import copyfile


URL = 'https://ru.hexlet.io'
NETLOC = 'ru.hexlet.io'
FIXTURES_PATH = 'fixtures/resources_download_test'
HTML_NAME = 'ru-hexlet-io-courses.html'
DOWNLOAD_DIR_NAME = 'ru-hexlet-io-courses_files'
RESOURCES = [
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
        '/assets/professions/nodejs1.png',
        'nodejs1.png',
        'ru-hexlet-io-assets-professions-nodejs1.png'
    ),
    (
        '/assets/professions/nodejs2.png',
        'nodejs2.png',
        'ru-hexlet-io-assets-professions-nodejs2.png'
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


def test_download_resources(requests_mock):
    with tempfile.TemporaryDirectory() as tmp_directory:
        for items in RESOURCES:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            requests_mock.get(
                URL + subpath,
                content=read_in_bytes(fixture_path),
                status_code=200,
            )
        html_path = get_fixture_path(HTML_NAME)
        copy_html_path = join(tmp_directory, split(html_path)[1])
        copyfile(html_path, copy_html_path)
        download_resources(copy_html_path, URL)

        for items in RESOURCES:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            assert read_in_bytes(
                fixture_path
            ) == read_in_bytes(
                f'{tmp_directory}/{DOWNLOAD_DIR_NAME}/{loaded_file}'
            )
        assert read(
            get_fixture_path(f'after/{HTML_NAME}')
        ) == read(
            f'{tmp_directory}/{HTML_NAME}'
        )
