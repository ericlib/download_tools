import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="download_tools", # Replace with your own username
    version="0.0.4",
    author="eric",
    author_email="ericlib@aliyun.com",
    description="爬虫的一些工具。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericlib/download_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)