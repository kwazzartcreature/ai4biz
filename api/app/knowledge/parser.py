import logging
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def parse(sitemap_url: str) -> list[str]:
        """
        Парсит sitemap из файла sitemap_path и возвращает список URL.
        Поддерживаются XML-сайты (формат urlset/sitemapindex) и текстовый формат.
        """
        urls = []
        res = requests.get(sitemap_url)
        if res.status_code != 200:
            logger.error(f"Ошибка при получении sitemap: {res.status_code}")
            return urls

        content = res.text
        # Если контент начинается с '<', предполагаем, что это XML.
        if content.startswith("<"):
            try:
                root = ET.fromstring(content)
            except ET.ParseError as e:
                logger.error(f"Ошибка парсинга XML: {e}")
                return urls

            # Определяем namespace, если он присутствует
            ns = {}
            if root.tag.startswith("{"):
                uri, tag = root.tag[1:].split("}")
                ns = {"ns": uri}

            if root.tag.endswith("urlset"):
                # Парсинг стандартного sitemap
                for url_elem in (
                    root.findall("ns:url", ns) if ns else root.findall("url")
                ):
                    loc = url_elem.find("ns:loc", ns) if ns else url_elem.find("loc")
                    if loc is not None and loc.text:
                        urls.append(loc.text.strip())
            elif root.tag.endswith("sitemapindex"):
                # Если это индекс sitemap'ов – собираем ссылки на вложенные sitemap-файлы
                for sitemap_elem in (
                    root.findall("ns:sitemap", ns) if ns else root.findall("sitemap")
                ):
                    loc = (
                        sitemap_elem.find("ns:loc", ns)
                        if ns
                        else sitemap_elem.find("loc")
                    )
                    if loc is not None and loc.text:
                        urls.append(loc.text.strip())
            else:
                logger.error("Неизвестный XML формат sitemap")
        else:
            # Если файл не начинается с '<', предполагаем, что это текстовый файл с URL'ами
            for line in content.splitlines():
                line = line.strip()
                if line:
                    urls.append(line)

        return urls
