import pytest
from page_loader.page_loader import download
import re


FORBIDDEN_CHARS = r'[^0-9a-z-.]'


def test_download_file_path(url, output_path):
    file_path = download(url, output_path)
    forbidden_chars = re.search(FORBIDDEN_CHARS, file_path)

    assert file_path is not None
    assert isinstance(file_path, str)
    assert file_path == output_path +
    assert not forbidden_chars
    assert file_path.endswith('.html')
    # TODO think how to do that:
    assert not ('https---' in file_path)
