from setuptools import setup

__version__ = "0.1.0"

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="django-accountkit",
    version=__version__,
    description='Django support for AccountKit',
    keywords="django, accountkit",
    author="CJLTSOD <github.tsod@tsod.idv.tw>",
    author_email="github.tsod@tsod.idv.tw",
    url="https://github.com/cjltsod/django-accountkit",
    license="MIT",
    packages=["accountkit"],
    include_package_data=True,
    install_requires=["django>=2.0", "requests>=2.19"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Environment :: Web Environment",
    ],
    long_description=long_description,
)
