import setuptools

setuptools.setup(
    name="derivkit",
    version="0.0.1",
    author="Spyridon Kavvathas",
    author_email="spiroskavvathas@gmail.com",
    description="A lightweight Python library for quantitative finance",
    long_description="A lightweight Python library for quantitative finance",
    long_description_content_type="text/markdown",
    url="https://github.com/spiroskavvathas/derivkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "scipy",
    ],
)