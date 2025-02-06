import pytest

from agent.crawler.crawler import Crawler


@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "urls",
    [
        "https://gold-swan.is/",
        ["https://gold-swan.is/", "https://gold-swan.is/departments/webdev"],
    ],
)
async def test_crawl(urls: str | list[str]):
    contents = await Crawler.crawl_urls(urls)

    assert isinstance(contents, list), "Результат должен быть списком"
    assert isinstance(contents[0], str), "Элементы списка должны быть строками"

    print(urls, contents)
