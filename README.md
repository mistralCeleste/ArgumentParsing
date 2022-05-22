# ArgumentParsing
Parses script Arguments

# Example Usage

```

from argument_parsing import Arguments, Argument
from typing import List


class SkuArguments(Arguments):

    def __init__(
            self
            , groups: str
    ):
        super().__init__()
        self._groups = groups

    @Argument(
        help='Sku group categories, separated by a comma for each group'
        , metavar='g'
    )
    def groups(self) -> str:
        return self._groups

    
def main() -> None:
    args = SkuArguments.parse()
    print(args.groups)

```