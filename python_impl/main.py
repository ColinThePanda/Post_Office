"""
Post Office

CLI application that takes in an input file of postage data and prints the cost

Colin Politi

Log:
v1.0 - 10/10/25 - CP
"""

from __future__ import annotations
from string import whitespace
from typing import List, Tuple, Union, Type
from enum import Enum
import os
import sys


def ibetween(num: float, size: Size) -> bool:
    """Helper function for checking if a number is between two numbers inclusively.

    Args:
        num (float): Number being compared
        size (Size): Size object containing a "top" and "bottom" value

    Returns:
        bool: If number is between the top and bottom
    """
    return all([num >= size.bottom, num <= size.top])


class PostData:
    """Class that contains the input values and functions to compute with it"""

    def __init__(self, line: str) -> None:
        """Initializer for PostData

        Args:
            line (str): Input line for data to be extracted from
        """
        self.length, self.height, self.thickness, self.start_zip, self.end_zip = self.extract_line_data(line)

    def extract_line_data(self, line: str) -> Tuple[float, float, float, str, str]:
        """Extracts the numbers from an input line

        Args:
            line (str): Line to extract

        Returns:
            Tuple[float, float, float, str, str]: Data extracted (length, height, thickness, start_zip, end_zip)
        """
        after_number = "".join(line.split(". ")[1:])
        no_spaces = "".join(filter(lambda c: c not in whitespace, after_number))
        data = no_spaces.split(",")
        post_data = (float(data[0]), float(data[1]), float(data[2]), data[3], data[4])
        return post_data

    def get_type(self) -> Postages:
        """Classifies the type of this object's data

        Returns:
            Postages: Postage type of the data
        """
        for post in Postages.all_posts():
            if isinstance(post, BasicPostages):
                if post.value.is_valid(self):
                    return post
            else:
                girth = 2 * self.height + 2 * self.length + 2 * self.thickness
                if ibetween(girth, Size(0, 84)):
                    return SpecialPostages.PACKAGE
                elif ibetween(girth, Size(84, 130)):
                    return SpecialPostages.LARGE_PACKAGE
                else:
                    return SpecialPostages.UNMAILABLE
        return SpecialPostages.UNMAILABLE

    def get_zone_dist(self) -> int:
        """Gets the zone distance from the start and end zip code

        Raises:
            ValueError: Starting zip code cannot be converted to int or not between 1 and 100,000
            ValueError: Ending zip code cannot be converted to int or not between 1 and 100,000

        Returns:
            int: Distance between zip codes
        """
        s1 = Size(1, 6999)
        s2 = Size(7000, 19999)
        s3 = Size(20000, 35999)
        s4 = Size(36000, 62999)
        s5 = Size(63000, 84999)
        s6 = Size(84999, 99999)
        sizes = [s1, s2, s3, s4, s5, s6]

        try:
            from_part = [ibetween(int(self.start_zip), size) for size in sizes].index(True)
        except ValueError:
            raise ValueError("Starting zip-code is invalid") from None
        try:
            to_part = [ibetween(int(self.end_zip), size) for size in sizes].index(True)
        except ValueError:
            raise ValueError("Starting zip-code is invalid") from None

        return abs(from_part - to_part)

    def get_cost(self) -> Union[float, str]:
        """Gets the cost of the post data to ship

        Returns:
            Union[float, str]: Either the cost as a float or the string "UNMAILABLE"
        """
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

        if type == SpecialPostages.UNMAILABLE:
            return "UNMAILABLE"

        return type_cost_map[type] + zone_cost_map[type] * dist


class Size:
    """Helper Class for "ibetween" Function"""

    def __init__(self, min: float, max: float) -> None:
        """Takes in minimum and maximum value and stores in object

        Args:
            min (float): Minimum value
            max (float): Maximum value
        """
        self.bottom = min
        self.top = max


class Postage:
    """Base Class for Postage Types"""

    def __init__(self, len: Size, height: Size, thickness: Size) -> None:
        """Takes in size values of post data and stores in object

        Args:
            len (Size): Length of postage
            height (Size): Height of postage
            thickness (Size): Thickness of postage
        """
        self.len: Size = len
        self.height: Size = height
        self.thickness: Size = thickness

    def is_valid(self, data: PostData) -> bool:
        """Takes in postage data and determines whether it can be classified as this type

        Args:
            data (PostData): Input postage data

        Returns:
            bool: Data is valid instance of this postage type
        """
        len_valid = ibetween(data.length, self.len)
        height_valid = ibetween(data.height, self.height)
        thickness_valid = ibetween(data.thickness, self.thickness)
        return all((len_valid, height_valid, thickness_valid))


class Postages(Enum):
    """Base Class for Postage Types"""

    @classmethod
    def all(cls) -> List["Postages"]:
        """Inherited by all subclasses so this class can easily access all types defined in a subclass

        Returns:
            List[Postages]: All postage types defined in subclasses
        """
        return list(dict(vars(cls)["_member_map_"]).values())

    @classmethod
    def all_posts(cls) -> List["Postages"]:
        """Returns all postage types in the subclasses "BasicPostages" and "SpecialPostages"

        Returns:
            List[Postages]: All postage types
        """
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
    """Postage Types With Normal Min and Max Values for Sizes"""

    REGULAR_CARD = Postage(Size(3.5, 4.25), Size(3.5, 6), Size(0.007, 0.016))
    LARGE_CARD = Postage(Size(4.25, 6), Size(6, 11.5), Size(0.007, 0.015))
    REGULAR_ENVELOPE = Postage(Size(3.5, 6.125), Size(5, 11.5), Size(0.16, 0.25))
    LARGE_ENVELOPE = Postage(Size(6.125, 24), Size(11, 18), Size(0.25, 0.5))


class SpecialPostages(Postages):
    """Postage Types With Irregular Size Classifications"""

    PACKAGE = 0
    LARGE_PACKAGE = 1
    UNMAILABLE = 2


def read_lines(file_name: str) -> List[str]:
    """Opens file and returns string of lines

    Args:
        file_name (str): Name of input file

    Returns:
        List[str]: All lines in input file
    """
    with open(file_name) as file:
        content = file.read()
    return content.splitlines()


def process_file(file_name: str) -> None:
    """Gets postage cost for each line in file

    Args:
        file_name (str): name of input file
    """
    lines = read_lines(file_name)
    for i, line in enumerate(lines):
        cost = PostData(line).get_cost()
        if isinstance(cost, float):  # Print rounded to 2 decimal places if num else just print
            print(f"{i+1}.{" " * (len(str(len(lines))) - len(str(i+1)) + 1)}{cost:.2f}")  # Num spaces to allign
        else:
            print(f"{i+1}.{" " * (len(str(len(lines)))  - len(str(i+1)) + 1)}{cost}")


def main() -> None:
    """Main function for program"""
    if len(sys.argv) <= 1:
        print(f"Usage:\npython {os.path.basename(__file__)} <input file>")
    else:
        file_name = sys.argv[1]
        process_file(file_name)


if __name__ == "__main__":
    main()
