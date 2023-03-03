from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vloginit",
    version="0.0.1",
    author="Vladislav Borshch",
    author_email="borchsh.vn@mail.com",
    description="L1 NR 3GPP Python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license ='MIT',
    url="https://github.com/vborchsh/pynrl1",
    project_urls={
        "Bug Tracker": "https://github.com/vborchsh/pynrl1/issues",
    },
    packages=find_packages(),
    entry_points ={},
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
