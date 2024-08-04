from setuptools import setup, find_packages

setup(
    name="dlocal_python",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "requests",
    ],
    author="Kyle Aquino	",
    author_email="kyle@payswyftly.com",
    description="A Python wrapper for the DLocal API",
    url="https://github.com/PayWithSwyftly/dlocal-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
