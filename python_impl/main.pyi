from string import whitespace
from typing import Tuple, Dict, Set
from enum import Enum

def ibetween(num : float, size : Size) -> bool: ...

class PostData:
    def __init__(self, line : str) -> None:
        self.length : float
        self.height : float
        self.thickness : float
        self.start_zip : float
        self.end_zip : float
    
    def extract_line_data(self, line : str) -> Tuple[float, float, float, str, str]: ...
    def get_type(self) -> Postages: ...
    def get_zone_dist(self) -> int: ...
    def get_cost(self) -> float: ...
    def __repr__(self) -> str: ...

class Size:
    def __init__(self, min : float, max : float) -> None:
        self.bottom : float
        self.top : float

class Postage:
    def __init__(self, len : Size, height : Size, thickness : Size) -> None:
        self.len : Size
        self.height : Size
        self.thickness : Size
    
    def is_valid(self, data : PostData) -> bool: ...
        
class Postages(Enum):
    @classmethod
    def all(cls) -> list["Postages"]: ...
    @classmethod
    def all_posts(cls) -> list["Postages"]: ...

class BasicPostages(Postages):
    REGULAR_CARD : Postage
    LARGE_CARD : Postage
    REGULAR_ENVELOPE : Postage
    LARGE_ENVELOPE : Postage

class SpecialPostages(Postages):
    PACKAGE : int
    LARGE_PACKAGE : int
    UNMAILABLE : int


def read_lines(file_name : str) -> list[str]: ...
def process_file(file_name : str) -> None: ...
def main(argv : list[str]) -> None: ...