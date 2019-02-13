from setuptools import setup

__version__ = "1.0.3"

setup(
    name='bini',
    version = __version__,
    description = "A library for binary ini-file(bini) manipulation in Python3",
    long_description = "A library for binary ini-file(bini) manipulation in Python3",
    author='Tobias Weise',
    author_email='tobias_weise@gmx.de',
    license = "BSD3",
    keywords= "bini ini configuration freelancer windows",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ],
    py_modules=('bini',)
)
