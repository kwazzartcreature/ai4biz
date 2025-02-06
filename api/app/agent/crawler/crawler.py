from crawl4ai import AsyncWebCrawler


class Crawler:
    @staticmethod
    async def crawl_urls(urls: str | list[str]) -> list[str]:
        if isinstance(urls, str):
            urls = [urls]

        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun_many(urls)

        results = [str(x.markdown) for x in results if x.success]
        return results
