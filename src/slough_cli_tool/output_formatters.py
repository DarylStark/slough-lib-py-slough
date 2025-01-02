"""Module with output formatters."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum

import yaml
from pydantic import BaseModel


class OutputType(str, Enum):
    """Output type for the configuration."""

    json = 'json'
    yaml = 'yaml'
    envvars = 'envvars'


class OutputFormatter(ABC):
    """Output formatter interface."""

    formatters: dict[OutputType, type['OutputFormatter']] = {}

    @classmethod
    def register(
        cls, output_type: OutputType
    ) -> Callable[[type['OutputFormatter']], type['OutputFormatter']]:
        """Register output formatter.

        Args:
            output_type (OutputType): Output type.
        """

        def decorator(
            subclass: type['OutputFormatter'],
        ) -> type['OutputFormatter']:
            """Decorator that registers the formatter.

            Args:
                subclass (type['OutputFormatter']): The subclass to register.

            Returns:
                type['OutputFormatter']: The subclass.
            """
            cls.formatters[output_type] = subclass
            return subclass

        return decorator

    def __init__(self, data: BaseModel) -> None:
        """Initialize formatter.

        Args:
            data (BaseModel): Data to format.
        """
        self._data = data

    @abstractmethod
    def format(self) -> str:
        """Format data to string.

        Returns:
            str: Formatted data.
        """


@OutputFormatter.register(OutputType.json)
class JSONFormatter(OutputFormatter):
    """JSON output formatter."""

    def __init__(self, data: BaseModel) -> None:
        """Initialize formatter.

        Args:
            data (BaseModel): Data to format.
        """
        super().__init__(data)

    def format(self) -> str:
        """Format data to JSON.

        Returns:
            str: Formatted data.
        """
        return f'{self._data.model_dump_json(indent=4)}\n'


@OutputFormatter.register(OutputType.yaml)
class YAMLFormatter(OutputFormatter):
    """YAML output formatter."""

    def __init__(self, data: BaseModel) -> None:
        """Initialize formatter.

        Args:
            data (BaseModel): Data to format.
        """
        super().__init__(data)

    def format(self) -> str:
        """Format data to YAML.

        Returns:
            str: Formatted data.
        """
        return yaml.dump(
            self._data.model_dump(),
            default_flow_style=False,
            sort_keys=False,
        )


@OutputFormatter.register(OutputType.envvars)
class EnvVarsFormatter(OutputFormatter):
    """Environment variables output formatter."""

    def __init__(self, data: BaseModel) -> None:
        """Initialize formatter.

        Args:
            data (BaseModel): Data to format.
        """
        super().__init__(data)

    def _format_dict(self, data: dict, prefix: str) -> str:
        """Format dictionary to environment variables.

        Args:
            data (dict): Dictionary to format.
            prefix (str): Prefix for the environment variables.

        Returns:
            str: Formatted data.
        """
        output = ''
        for key, value in data.items():
            var_name = f'{prefix}_{key}'.upper()

            if type(value) in [str, int, float]:
                output += f'{var_name}="{value}"\n'
            elif type(value) is dict:
                output += self._format_dict(value, f'{prefix}_{key}')
            elif type(value) is list:
                all_as_string = [str(item) for item in value]
                output += f'{var_name}="{','.join(all_as_string)}"\n'
                for i, item in enumerate(value):
                    if type(value) in [str, int, float]:
                        output += f'{var_name}_{i}="{item}"\n'
                    elif type(item) is dict:
                        output += self._format_dict(item, f'{var_name}_{i}')
        return output

    def format(self) -> str:
        """Format data to environment variables.

        Returns:
            str: Formatted data.
        """
        return self._format_dict(self._data.model_dump(), 'SLOUGH')
