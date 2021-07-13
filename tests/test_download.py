import pytest
from page_loader.page_loader import download
import re
from pathlib import Path
from os.path import splitext, split
import tempfile


FORBIDDEN_CHARS = r'[^0-9a-z-.]'
URLs = (
    'https://ru.hexlet.io/courses',
    'https://ru.HEXLET.io/courses',
)


def test_download():
    for url in URLs:
        with tempfile.TemporaryDirectory() as tmp_directory:
            file_path = download(url, tmp_directory)
            file_name = split(file_path)[-1]
            forbidden_chars = re.search(FORBIDDEN_CHARS, file_name)
            file = Path(file_path)

            assert file.is_file()
            assert file_path is not None
            assert isinstance(file_path, str)
            assert not forbidden_chars
            assert splitext(file_path)[-1] == '.html'
            # TODO think how to do that:
            assert not ('https---' in file_path)


def test_download_exceptions():
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(ValueError) as e:
            download('', tmp_directory)
        assert str(e.value) == 'url is missing'

    with pytest.raises(ValueError) as e:
        download(URLs[1], None)
    assert str(e.value) == 'output path does not exist'

