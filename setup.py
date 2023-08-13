from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Binomial pricing package'
LONG_DESCRIPTION = 'A package that allows you to price stock options and futures with the binomial tree.'

# Setting up
setup(
    name="PyBinomPricer",
    version=VERSION,
    author="Georgios Smyridis",
    author_email="<georgesmyr@icloud.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'options', 'futures', 'option pricing', 'futures pricing', 'pricing', 'binomial pricing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Quants",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)