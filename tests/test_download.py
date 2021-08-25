import pytest
import tempfile
import os
import stat
import pathlib
import requests
import urllib
from page_loader.page_loader import download


STATUS_CODES = [403, 404, 500, 502]
URL = 'https://ru.hexlet.io'
NETLOC = 'ru.hexlet.io'
FIXTURES_PATH = 'fixtures'
FIXTURE_AFTER_PATH = 'after'
HTML_NAME = 'ru-hexlet-io.html'
DOWNLOAD_DIR_NAME = 'ru-hexlet-io_files'
RESOURCES = [
    (
        '/courses',
        'courses.html',
        'ru-hexlet-io-courses.html'
    ),
    (
        '/assets/application.css',
        'application.css',
        'ru-hexlet-io-assets-application.css'
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


def read(file_path, mode='r'):
    with open(file_path, mode) as f:
        file = f.read()
    return file


def get_fixture_path(fixture_name):
    return os.path.join(
        pathlib.Path(__file__).absolute().parent,
        FIXTURES_PATH,
        fixture_name
    )


def test_download(requests_mock):
    requests_mock.get(
        URL,
        content=read(get_fixture_path(HTML_NAME), 'rb'),
        status_code=200,
    )
    for resource in RESOURCES:
        subpath, fixture_name, loaded_file_name = resource
        fixture_path = get_fixture_path(fixture_name)
        requests_mock.get(
            URL + subpath,
            content=read(fixture_path, 'rb'),
            status_code=200,
        )

    with tempfile.TemporaryDirectory() as tmp_directory_path:
        download(URL, tmp_directory_path)
        assert read(
            get_fixture_path(os.path.join(FIXTURE_AFTER_PATH, HTML_NAME))
        ) == read(
            os.path.join(tmp_directory_path, HTML_NAME)
        )

        for resource in RESOURCES:
            subpath, fixture_name, loaded_file_name = resource
            fixture_path = get_fixture_path(fixture_name)
            assert read(
                fixture_path, 'rb',
            ) == read(
                os.path.join(tmp_directory_path, DOWNLOAD_DIR_NAME, loaded_file_name), 'rb',
            )


@pytest.mark.parametrize('status_code', STATUS_CODES)
def test_download_request_exceptions(requests_mock, status_code):
    requests_mock.get(
        'http://www.test.com/',
        status_code=status_code,
    )
    with tempfile.TemporaryDirectory() as tmp_directory_path:
        with pytest.raises(requests.exceptions.InvalidURL):
            download('', tmp_directory_path)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            download('http://www.test.com/', tmp_directory_path)
        assert str(e.value).split()[0] == str(status_code)


def test_download_io_errors(requests_mock):

    requests_mock.get(
        URL,
        content=read(get_fixture_path(HTML_NAME), 'rb'),
        status_code=200,
    )

    with pytest.raises(NotADirectoryError):
        download(URL, get_fixture_path(HTML_NAME))

    with pytest.raises(FileNotFoundError):
        download(URL, '/undefined')

    with tempfile.TemporaryDirectory() as tmp_directory_path:
        os.chmod(tmp_directory_path, stat.S_IREAD)
        with pytest.raises(PermissionError):
            download(URL, tmp_directory_path)
