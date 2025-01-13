"""Module that contains the ConfigFileFinder class."""

from pathlib import Path

from chain_of_responsibility import ChainHandler, NotHandledError


class FileChecker(ChainHandler[Path]):
    """Class that searches for a file in a directory.

    Can be used as a chain.
    """

    def __init__(
        self,
        filename: str,
        directory: Path,
        subdirectory: Path,
        extensions: list[str],
    ) -> None:
        """Constructor for the FileChecker2 class.

        Args:
            filename (str): The filename to check.
            directory (Path): The directory to check.
            subdirectory (Path): The subdirectory to check.
            extensions (list[str]): The extensions to check.
        """
        super().__init__()
        self._filename = filename
        self._directory = directory.resolve()
        self._subdirectory = (directory / subdirectory).resolve()
        self._extensions = extensions

    def _handle(self) -> Path:
        """Method that searches for the file in the directory.

        Returns:
            Path: The path to the file if found.
        """
        paths = [self._directory, self._subdirectory]
        for path in paths:
            for extension in self._extensions:
                path_object = path / Path(f'{self._filename}.{extension}')
                if path_object.is_file():
                    return path_object.resolve()

        raise NotHandledError


class ConfigFileFinder:
    """Class that finds the configuration file."""

    def __init__(
        self,
        working_dir: Path = Path(),
        max_directory_depth: int = 6,
        filename: str = 'slough',
        subdir: str = '.slough',
    ) -> None:
        """Constructor for the ConfigFileFinder class.

        Args:
            working_dir (Path, optional): The working directory to start the
                search. Defaults to Path().
            max_directory_depth (int, optional): The maximum directory depth to
                search for the configuration file. Defaults to 6.
            filename (str, optional): The name of the configuration file.
                Should be without the extension. Defaults to 'slough'.
            subdir (str, optional): The name of the subdirectory to search in.
        """
        self._working_dir = working_dir
        self._max_directory_depth = max_directory_depth
        self._filename = filename
        self._subdir = subdir

    def find_config_file(self) -> Path | None:
        """Method that finds the configuration file.

        Returns:
            str: The configuration file path if found, None otherwise.
        """
        search_path = self._working_dir.resolve()
        extensions = ['yml', 'yaml', 'json']

        file_checkers: list[ChainHandler[Path]] = [
            FileChecker(
                f'{self._filename}',
                search_path,
                Path(self._subdir),
                extensions=extensions,
            )
        ]

        for _ in range(0, self._max_directory_depth):
            if len(search_path.parents) > 0:
                search_path = search_path.parent.resolve()
                next_checker = FileChecker(
                    f'{self._filename}',
                    search_path,
                    Path(self._subdir),
                    extensions=extensions,
                )
                file_checkers[-1].set_next(next_checker)
                file_checkers.append(next_checker)

        return file_checkers[0].handle()
