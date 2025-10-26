from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="authkit",
    version="0.1.0",
    author="Yiğit Bıçakçı",
    author_email="your.email@example.com",  # Replace with your email
    description="A lightweight, modular, and extensible Python authentication framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yigitb-dev/AuthKit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cryptography>=3.4.7",
        "pyotp>=2.6.0",
        "requests>=2.26.0",  # For OAuth functionality
    ],
    keywords="authentication, security, oauth, 2fa, encryption",
    project_urls={
        "Bug Reports": "https://github.com/yigitb-dev/AuthKit/issues",
        "Source": "https://github.com/yigitb-dev/AuthKit",
    },
)