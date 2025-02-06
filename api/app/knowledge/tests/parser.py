import os
import pytest

from knowledge.parser import Parser
from lib import PROJECT_ROOT

SITEMAPS_DIR = os.path.join(PROJECT_ROOT, "knowledge/tests/sitemaps")
print(SITEMAPS_DIR)


@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "url",
    [
        "https://ai.pydantic.dev/sitemap.xml",
    ],
)
def test_parser(url: str):
    urls = Parser.parse(url)

    assert urls, f"Should return urls for {url}"
    assert isinstance(urls, list), f"Should return a list of urls for {url}"
    assert len(urls) > 0, f"Should return at least one url for {url}"
    assert isinstance(urls[0], str), f"Should return a list of strings for {url}"
