const branch = process.env.GITHUB_REF_NAME || process.env.BRANCH_NAME;

const plugins = [
  '@semantic-release/commit-analyzer',
  '@semantic-release/release-notes-generator',
  '@semantic-release/changelog',
  [
    '@semantic-release/exec',
    {
      prepareCmd: 'python update-versions.py ${nextRelease.version}'
    }
  ],
  [
    '@semantic-release/git',
    {
      assets: [
        'CHANGELOG.md',
        'pyproject.toml',
        'src/slough/__init__.py'
      ],
      message: 'chore(release): ${nextRelease.version}\n\n${nextRelease.notes}'
    }
  ]
];

// Only add GitHub plugin for main branch
if (branch === 'main') {
  plugins.splice(3, 0, '@semantic-release/github');
}

module.exports = {
  branches: [
    {
      name: 'main'
    },
    {
      name: 'dev',
      prerelease: 'beta'
    }
  ],
  plugins
};