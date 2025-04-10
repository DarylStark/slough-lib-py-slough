"""Test the `visitor` capabilities of the `SloughConfig` model."""

import pytest
from mock_visitor import MockVisitor

from slough_config.config_model import SloughConfig


@pytest.mark.parametrize(
    'field, expected_count',
    [
        ('config_model', 1),
        ('project_information', 1),
        ('author', 1),
        ('config_profile', 3),
        ('container_configuration', 3),
        ('development_environment', 1),
    ],
)
def test_visitor(
    config_model: SloughConfig, field: str, expected_count: int
) -> None:
    """Test the visitor capabilities of the `SloughConfig` model.

    Args:
        config_model (SloughConfig): The configuration model.
        field (str): The field to test.
        expected_count (int): The expected count of visits.
    """
    visitor = MockVisitor()
    config_model.visit(visitor)
    assert visitor.visited.count(field) == expected_count
