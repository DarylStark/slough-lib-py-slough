"""Module that contains the ConfigFileFinder class."""

from pathlib import Path

from chain_of_responsibility import ChainHandler, NotHandledError


class FileChecker(ChainHandler[Path]):
    """Class that checks if a file exists.

    Can be used as a chain.
    """

    def __init__(self, filename: str, directory: Path, max_depth: int) -> None:
        """Constructor for the FileChecker class.

        Args:
            filename (str): The filename to check.
            directory (Path): The directory to check.
            max_depth (int): The maximum directory depth to check.
        """
        super().__init__()
        self._filename = filename
        self._directory = directory
        self._max_depth = max_depth

    def _handle(self) -> Path:
        """Method that checks if the file exists.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        path_object = self._directory / Path(self._filename)
        if path_object.exists():
            return path_object

        if self._max_depth == 0 or len(self._directory.parents) == 0:
            raise NotHandledError

        self._max_depth -= 1
        self._directory = self._directory.parent
        return self._handle()


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
        # Create a chain of checkers
        file_checker_yml = FileChecker(
            f'{self._filename}.yml',
            self._working_dir,
            self._max_directory_depth,
        )
        file_checker_yml_slough_dir = FileChecker(
            f'{self._subdir}/{self._filename}.yml',
            self._working_dir,
            self._max_directory_depth,
        )
        file_checker_yaml = FileChecker(
            f'{self._filename}.yaml',
            self._working_dir,
            self._max_directory_depth,
        )
        file_checker_yaml_slough_dir = FileChecker(
            f'{self._subdir}/{self._filename}.yaml',
            self._working_dir,
            self._max_directory_depth,
        )
        file_checker_json = FileChecker(
            f'{self._filename}.json',
            self._working_dir,
            self._max_directory_depth,
        )
        file_checker_json_slough_dir = FileChecker(
            f'{self._subdir}/{self._filename}.json',
            self._working_dir,
            self._max_directory_depth,
        )

        file_checker_yml.set_next(file_checker_yml_slough_dir)
        file_checker_yml_slough_dir.set_next(file_checker_yaml)
        file_checker_yaml.set_next(file_checker_yaml_slough_dir)
        file_checker_yaml_slough_dir.set_next(file_checker_json)
        file_checker_json.set_next(file_checker_json_slough_dir)

        return file_checker_yml.handle()
