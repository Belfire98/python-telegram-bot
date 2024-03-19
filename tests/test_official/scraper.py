import asyncio
import re
from dataclasses import dataclass
from typing import List, Literal

import httpx
from bs4 import BeautifulSoup

@dataclass(slots=True, frozen=True)
class TelegramParameter:
    param_name: str
    param_type: str
    param_required: bool
    param_description: str

@dataclass(slots=True, frozen=True)
class TelegramClass:
    class_name: str
    class_parameters: List[TelegramParameter]

@dataclass(slots=True, frozen=True)
class TelegramMethod:
    method_name: str
    method_parameters: List[TelegramParameter]

class Scraper:
    def __init__(self):
        self.request = None
        self.soup = None

    async def make_request(self) -> None:
        async with httpx.AsyncClient() as client:
            self.request = await client.get("https://core.telegram.org/bots/api", timeout=10)
        self.soup = BeautifulSoup(self.request.text, "html.parser")

    def is_parameter_required_by_tg(self, field: str) -> bool:
        return field.strip() != "optional"

    def parse_docs(self, doc_type: Literal["method", "class"]) -> List[Union[TelegramMethod, TelegramClass]]:
        argvalues = []
        names: List[str] = []
        if self.request is None:
            asyncio.run(self.make_request())

        h4_anchor_pattern = re.compile(r"h4 > a\.anchor")
        for unparsed in self.soup.select(h4_anchor_pattern.pattern):
            if "-" not in unparsed["name"]:
                h4: Tag = unparsed.parent
                name = h4.text
                if doc_type == "method" and name[0].lower() == name[0]:
                    params = self.parse_table_for_params(h4)
                    if doc_type == "method":
                        obj = TelegramMethod(method_name=name, method_parameters=params)
                    argvalues.append(obj)
                    names.append(name)
                elif doc_type == "class" and self.is_pascal_case(name) and name not in IGNORED_OBJECTS:
                    params = self.parse_table_for_params(h4)
                    if doc_type == "class":
                        obj = TelegramClass(class_name=name, class_parameters=params)
                    argvalues.append(obj)
                    names.append(name)

        return argvalues

    def collect_methods(self) -> List[TelegramMethod]:
        return self.parse_docs("method")

    def collect_classes(self) -> List[TelegramClass]:
        return self.parse_docs("class")

    @staticmethod
    def is_pascal_case(name: str) -> bool:
        return name and name[0].isupper() and name[1:].islower()

    def parse_table_for_params(self, h4: Tag) -> List[TelegramParameter]:
        table = find_next_sibling_until(h4, "table", h4.find_next_sibling("h4"))
        if not table:
            return []

        params = []
        for tr in table.find_all("tr")[1:]:
            fields = []
            for td in tr.find_all("td"):
                param = td.text
                fields.append(param)

            param_name = fields[0]
            param_type = fields[1]
            param_required = self.is_parameter_required_by_tg(fields[2])
            param_desc = fields[-1]  # since length can be 2 or 3, but desc is always the last
            params.append(TelegramParameter(param_name, param_type, param_required, param_desc))

        return params

def main() -> None:
    scraper = Scraper()
    methods, classes = scraper.collect_methods(), scraper.collect_classes()
    print(f"Found {len(methods)} methods and {len(classes)} classes.")

if __name__ == "__main__":
    main()
