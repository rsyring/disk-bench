from setuptools import setup, find_packages

setup(
    name='diskbench',
    version='0.1',
    author='Level 12',
    author_email='devteam@level12.io',
    packages=find_packages(exclude=['misc']),

    entry_points={  # Optional
        'console_scripts': [
            'db=diskbench.cli:db',
        ],
    },
)
