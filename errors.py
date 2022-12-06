# holds all errors which occur during the program

class Error:
    def __init__(self, message: str, line: int) -> None:
        self.message = message
        self.line = line

    def __str__(self) -> str:
        return f'line {self.line}: {self.message}'


class ErrorHandler:
    """
    Allows errors to be seperated on a per file basis
    """

    def __init__(self, *args):
        self.errors: list[Error] = list(args)  # type: ignore

    def new_error(self, message: str, line: int, can_continue: bool = False) -> None:
        self.errors.append(Error(message, line))
        if not can_continue:
            print(
                "compilation of the program cannot be continued due to the following errors:")
            self.output_errors()

    def output_errors(self) -> None:
        for error in self.errors:
            print(str(error))
        print('compilation was unsuccessful')

    def clear_errors(self) -> None:
        self.errors = []
