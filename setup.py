from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="juicewrld-api-wrapper",
    version="1.0.4",
    author="Juice WRLD API Wrapper",
    author_email="support@juicewrldapi.com",
    description="A comprehensive Python wrapper for the Juice WRLD API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HackinHood/juicewrld-api-wrapper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "twine>=4.0",
            "build>=0.10",
        ],
    },
    keywords="juice wrld, api, wrapper, music, discography, python",
    project_urls={
        "Homepage": "https://github.com/HackinHood/juicewrld-api-wrapper",
        "Documentation": "https://github.com/HackinHood/juicewrld-api-wrapper#readme",
        "Bug Reports": "https://github.com/HackinHood/juicewrld-api-wrapper/issues",
        "Source": "https://github.com/HackinHood/juicewrld-api-wrapper",
        "Changelog": "https://github.com/HackinHood/juicewrld-api-wrapper/releases",
    },
    include_package_data=True,
    zip_safe=False,
)
