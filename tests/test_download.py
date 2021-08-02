import pytest
from page_loader.page_loader import download
import re
from pathlib import Path
from os.path import split
import tempfile
import requests


FORBIDDEN_CHARS = r'[^0-9a-z-.]'
URLs = (
    'https://ru.hexlet.io/courses',
    'https://ru.HEXLET.io/courses',
)
DATA = open('tests/fixtures/ru-hexlet-io-courses.html', 'rb')


class RequestsFake:
    headers = {
            'content-length': 512,
        }
    def __init__(self, data):
        self.data = data

    def get(self, url, stream):
        return self

    def iter_content(self, chunk_size):
        return self.data

    def raise_for_status(self):
        pass


def test_download():
    for url in URLs:
        with tempfile.TemporaryDirectory() as tmp_directory:
            file_path = download(
                url,
                tmp_directory,
                library=RequestsFake(DATA)
            )
            file_name = split(file_path)[-1]
            forbidden_chars = re.search(FORBIDDEN_CHARS, file_name)
            file = Path(file_path)

            assert file.is_file()
            #  assert file_path is not None
            assert isinstance(file_path, str)
            assert not forbidden_chars
            assert file_path.endswith('ru-hexlet-io-courses.html')
            #  assert splitext(file_path)[-1] == '.html'
            #  TODO think how to do that:
            assert not ('https---' in file_path)


def test_download_exceptions(requests_mock):
    # TODO discuss with the mentor
    requests_mock.get(
        'http://www.test.com/',
        # text='Not Found',
        status_code=404,
    )

    with tempfile.TemporaryDirectory() as tmp_directory:

        with pytest.raises(ValueError):
            download('', tmp_directory)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            download('http://www.test.com/', tmp_directory)
        assert str(e.value) == '404 Client Error: ' \
                               'None for url: http://www.test.com/'

    with pytest.raises(FileNotFoundError):
        download(URLs[1], '/undefined')
