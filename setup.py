import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tabletop-randomness",
    version="0.0.1",
    author="kairosite",
    author_email="shallikerm@hotmail.co.uk",
    description="A python library for providing randomness of dice and cards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kairosite/Tabletop-Randomness",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires='>=3.6',
)