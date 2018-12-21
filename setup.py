import os.path as osp
from setuptools import setup, find_namespace_packages

cdir = osp.abspath(osp.dirname(__file__))
README = open(osp.join(cdir, 'readme.rst')).read()
CHANGELOG = open(osp.join(cdir, 'changelog.rst')).read()

version_fpath = osp.join(cdir, 'diskbench', 'version.py')
version_globals = {}
with open(version_fpath) as fo:
    exec(fo.read(), version_globals)

setup(
    name='disk-bench',
    version=version_globals['VERSION'],
    description='CLI tool to benchmark drive performance',
    long_description='\n\n'.join((README, CHANGELOG)),
    author='Randy Syring',
    author_email='randy@thesyrings.us',
    url='https://github.com/rsyring/disk-bench',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    packages=find_namespace_packages(include=['diskbench', 'diskbench.*']),
    include_package_data=True,
    install_requires=[
        'click',
        'sh',
        'tableprint',
    ],
    entry_points={
        'console_scripts': [
            'disk-bench=diskbench.cli:db',
        ],
    },
)
