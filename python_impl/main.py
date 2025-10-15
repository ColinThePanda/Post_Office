from __future__ import annotations
from string import whitespace
from typing import List, Tuple, Union, Type
from enum import Enum
import os
import sys


def ibetween(num: float, size: Size) -> bool:
    return all([num >= size.bottom, num <= size.top])


class PostData:
    def __init__(self, line: str) -> None:
        self.length, self.height, self.thickness, self.start_zip, self.end_zip = (
            self.extract_line_data(line)
        )

    def extract_line_data(self, line: str) -> Tuple[float, float, float, str, str]:
        after_number = "".join(line.split(". ")[1:])
        no_spaces = "".join(filter(lambda c: c not in whitespace, after_number))
        data = no_spaces.split(",")
        post_data = (float(data[0]), float(data[1]), float(data[2]), data[3], data[4])
        return post_data

    def get_type(self) -> Postages:
        for post in Postages.all_posts():
            if isinstance(post, BasicPostages):
                if post.value.is_valid(self):
                    return post
            else:
                girth = 2 * self.height + 2 * self.length
                if ibetween(girth, Size(0, 84)):
                    return SpecialPostages.PACKAGE
                elif ibetween(girth, Size(84, 130)):
                    return SpecialPostages.LARGE_PACKAGE
                else:
                    return SpecialPostages.UNMAILABLE
        return SpecialPostages.UNMAILABLE

    def get_zone_dist(self) -> int:
        """
        ZONE 1     2     3     4     5     6
        FROM 00001 07000 20000 36000 63000 85000
        TO   06999 19999 35999 62999 84999 99999
        """

        s1 = Size(1, 6999)
        s2 = Size(7000, 19999)
        s3 = Size(20000, 35999)
        s4 = Size(36000, 62999)
        s5 = Size(63000, 84999)
        s6 = Size(84999, 99999)
        sizes = [s1, s2, s3, s4, s5, s6]

        try:
            from_part = [ibetween(int(self.start_zip), size) for size in sizes].index(
                True
            )
        except ValueError:
            raise ValueError("Starting zip-code is invalid") from None
        try:
            to_part = [ibetween(int(self.end_zip), size) for size in sizes].index(True)
        except ValueError:
            raise ValueError("Starting zip-code is invalid") from None

        return abs(from_part - to_part)

    def get_cost(self) -> float:
        type_cost_map = {
            BasicPostages.REGULAR_CARD: 0.20,
            BasicPostages.LARGE_CARD: 0.37,
            BasicPostages.REGULAR_ENVELOPE: 0.37,
            BasicPostages.LARGE_ENVELOPE: 0.60,
            SpecialPostages.PACKAGE: 2.95,
            SpecialPostages.LARGE_PACKAGE: 3.95,
        }

        zone_cost_map = {
            BasicPostages.REGULAR_CARD: 0.03,
            BasicPostages.LARGE_CARD: 0.03,
            BasicPostages.REGULAR_ENVELOPE: 0.04,
            BasicPostages.LARGE_ENVELOPE: 0.05,
            SpecialPostages.PACKAGE: 0.25,
            SpecialPostages.LARGE_PACKAGE: 0.35,
        }

        dist = self.get_zone_dist()
        type = self.get_type()

        return type_cost_map[type] + zone_cost_map[type] * dist

    def __repr__(self) -> str:
        return f"PostData({self.length}, {self.height}, {self.thickness}, {self.start_zip}, {self.end_zip})"


class Size:
    def __init__(self, min: float, max: float) -> None:
        self.bottom = min
        self.top = max


class Postage:
    def __init__(self, len: Size, height: Size, thickness: Size) -> None:
        self.len: Size = len
        self.height: Size = height
        self.thickness: Size = thickness

    def is_valid(self, data: PostData) -> bool:
        len_valid = ibetween(data.length, self.len)
        height_valid = ibetween(data.height, self.height)
        thickness_valid = ibetween(data.thickness, self.thickness)
        return all((len_valid, height_valid, thickness_valid))


class Postages(Enum):
    @classmethod
    def all(cls) -> List["Postages"]:
        return list(dict(vars(cls)["_member_map_"]).values())

    @classmethod
    def all_posts(cls) -> List["Postages"]:
        sub_classes: List[Type[Union[BasicPostages, SpecialPostages]]] = [
            BasicPostages,
            SpecialPostages,
        ]

        all = []
        for post_type in sub_classes:
            for post in post_type.all():
                all.append(post)
        return all


class BasicPostages(Postages):
    REGULAR_CARD = Postage(Size(3.5, 4.25), Size(3.5, 6), Size(0.007, 0.016))
    LARGE_CARD = Postage(Size(4.25, 6), Size(6, 11.5), Size(0.007, 0.015))
    REGULAR_ENVELOPE = Postage(Size(3.5, 6.125), Size(5, 11.5), Size(0.16, 0.25))
    LARGE_ENVELOPE = Postage(Size(6.125, 24), Size(11, 18), Size(0.25, 0.5))


class SpecialPostages(Postages):
    PACKAGE = 0
    LARGE_PACKAGE = 1
    UNMAILABLE = 2


def read_lines(file_name: str) -> List[str]:
    with open(file_name) as file:
        content = file.read()
    return content.splitlines()


def process_file(file_name: str) -> None:
    for i, line in enumerate(read_lines(file_name)):
        cost = PostData(line).get_cost()
        print(f"{i+1}. {cost:.2f}")


def main(argv: List[str]) -> None:
    if len(argv) <= 1:
        print(f"Usage:\npython {os.path.basename(__file__)} <input file>")
    else:
        file_name = argv[1]
        process_file(file_name)


if __name__ == "__main__":
    main(sys.argv)
