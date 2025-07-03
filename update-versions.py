"""Script to update versions in specific files.

This script can be used in combination with Semantic Release to make sure that
specific files are updated with a new version number. This can, for instance,
make sure that `__init__.py` for a specific library gets a new versionnumber.

Run with:

    python3 update-versions.py <new-version>

For instance:

    python3 update-versions.py 1.2.3

"""

import re
import sys

regexes_to_update: list[dict[str, str]] = [
    {
        'file': 'pyproject.toml',
        'pattern': r'version = ".+"',
        'new_text': 'version = "{{ new_version }}"',
    },
    {
        'file': 'src/slough/__init__.py',
        'pattern': r'__version__ = \'.+\'',
        'new_text': "__version__ = '{{ new_version }}'",
    },
]

if __name__ == '__main__':
    new_version = sys.argv[1]

    for regex_to_update in regexes_to_update:
        with open(regex_to_update['file']) as infile:
            content = infile.read()

        new_content = re.sub(
            regex_to_update['pattern'],
            regex_to_update['new_text'].replace(
                '{{ new_version }}', new_version
            ),
            content,
        )
        with open(regex_to_update['file'], 'w') as outfile:
            outfile.write(new_content)
