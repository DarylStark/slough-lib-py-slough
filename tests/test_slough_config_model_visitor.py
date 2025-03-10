"""Test the `visitor` capabilities of the `SloughConfig` model."""

from mock_visitor import MockVisitor

from slough_config.config_model import SloughConfig


def test_visitor(config_model: SloughConfig) -> None:
    """Test the visitor capabilities of the `SloughConfig` model."""
    visitor = MockVisitor()
    config_model.visit(visitor)

    assert visitor.visited.count('config_model') == 1
    assert visitor.visited.count('project_information') == 1
    assert visitor.visited.count('author') == 1
    assert visitor.visited.count('config_profile') == 3
    assert visitor.visited.count('container_configuration') == 3
