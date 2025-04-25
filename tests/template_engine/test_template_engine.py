"""Tests for the template engine."""

import pytest

from template_engine import TemplateEngine


@pytest.mark.parametrize(
    'template_string, expected',
    [
        ('Hello, {{ name }}!', 'Hello, World!'),
        (
            'Hello, {{ name }}! Welcome to {{ place }}.',
            'Hello, Alice! Welcome to Wonderland.',
        ),
        (
            'Hello, {{ name.upper() }}! Welcome to {{ place }}.',
            'Hello, ALICE! Welcome to Wonderland.',
        ),
        (
            'Hello, {{ name.lower() }}! Welcome to {{ place }}.',
            'Hello, alice! Welcome to Wonderland.',
        ),
    ],
)
def test_template_strings_single_variable(
    template_string: str, expected: str
) -> None:
    """Test the template strings."""
    # Test with a simple template string
    template_string = 'Hello, {{ name }}!'
    context = {'name': 'World', 'place': 'Earth'}
    engine = TemplateEngine(context)
    result = engine.render(template_string)
    assert result == 'Hello, World!'


def test_template_strings_multiple_variables() -> None:
    """Test with a template string with multiple variables."""
    template_string = 'Hello, {{ name }}! Welcome to {{ place }}.'
    context = {'name': 'Alice', 'place': 'Wonderland'}
    engine = TemplateEngine(context)
    result = engine.render(template_string)
    assert result == 'Hello, Alice! Welcome to Wonderland.'


def test_template_strings_no_variables() -> None:
    """Test with a template string with no variables."""
    template_string = 'Hello, World{{ non_existing }}!'
    engine = TemplateEngine(context={})
    result = engine.render(template_string)
    assert result == 'Hello, World!'


def test_template_string_with_deep_context() -> None:
    """Test with a template string with a deep context."""
    template_string = 'Hello, {{ user.name }}! Welcome to {{ user.place }}.'
    context = {'user': {'name': 'Bob', 'place': 'Builderland'}}
    engine = TemplateEngine(context)
    result = engine.render(template_string)
    assert result == 'Hello, Bob! Welcome to Builderland.'
