from setuptools import setup, find_packages

def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="stonks-suite",
    version="0.1.0",
    author="Matt Gordon",
    author_email="matt@mlgordon.me",
    description="Algo trading suite",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mgordon34/stonks-suite",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.12",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "live": [],
    },
    entry_points={
        "console_scripts": [
            "stonks=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json"],
    },
    project_urls={
        "Source": "https://github.com/mgordon34/stonks-suite",
        "Documentation": "https://github.com/mgordon34/stonks-suite#readme",
    },
)

