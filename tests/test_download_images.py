import pytest
import tempfile
from page_loader.page_loader import download_images
from os.path import split
import re
from tests.test_download import FORBIDDEN_CHARS
from pathlib import Path


HTML_PATH = 'tests/fixtures/badcode-ru-docker-fixture.html'
# TODO this:
domain_name = ''
netloc = ''


def test_download_images():
    with tempfile.TemporaryDirectory() as tmp_directory:
        images_paths = download_images(HTML_PATH, tmp_directory, domain_name, netloc)
        for image_path in images_paths:
            image = Path(image_path)
            image_name = split(image_path)[-1]
            assert isinstance(image_path, str)
            assert image.is_file()
            assert not re.search(FORBIDDEN_CHARS, image_name)
            assert not ('https---' in image_path)
            assert domain_name is not None


def test_download_images_exceptions():
    # TODO discuss with the mentor
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(ValueError):
            download_images('', tmp_directory)

    with pytest.raises(FileNotFoundError):
        download_images(HTML_PATH, '/undefined')