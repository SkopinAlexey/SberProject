import json

from bs4 import BeautifulSoup

from web_parser.utils import download_wait, driver_config


class WebParser:
    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def get_developers_list(self):
        try:
            self._driver.get(
                "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/developers"
                "?place=0-25&offset=0&limit=1000&sortType=asc&sortField=devShortCleanNm")
            soup = BeautifulSoup(self._driver.page_source, 'lxml')
            find_all_id = soup.find("pre")
            parsed_json = json.loads(str(find_all_id.text))
        except Exception as ex:
            print(f'Ошибка: {ex}')

        return parsed_json['data']['list']

    def get_developer_objects(self, developer_id):
        try:
            self._driver.get("https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn"
                             f"/object/?offset=0&limit=999999&place=0-25&devId={developer_id}")
            soup = BeautifulSoup(self._driver.page_source, 'lxml')
            find_all_id = soup.find("pre")
            parsed_json = json.loads(str(find_all_id.text))
        except Exception as ex:
            print(f'Ошибка: {ex}')
        return parsed_json['data']['list']

    def get_object_declarations(self, object_id):
        try:
            self._driver.get("https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api"
                             f"/object/{object_id}/documentation/download?tab=projectDeclarations")
            download_wait()

        except Exception as ex:
            print(f'Ошибка: {ex}')

    def tear_down(self):
        if self._driver is not None:
            self._driver.quit()


web_parser = WebParser(driver_config())
