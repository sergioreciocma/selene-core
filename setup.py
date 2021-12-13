# %%
from setuptools import setup, find_packages
from setuptools.command import easy_install

# %%
REQUIREMENTS = [
    "selenium",
    "beautifulsoup4",
    "lxml"
]
__version__ = "0.0.9"

# %%
setup(
    name="selene",
    version=__version__,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS + ["pytest", "pytest-runner"],
    include_package_data=True,
)
