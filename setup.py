from setuptools import setup, find_packages
import os

with open('VERSION') as f:
    version = f.read().strip()

def read_requirements(filename='requirements.txt'):
    """Read the requirements from the given filename"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(current_dir, filename), encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codebase-digest",
    version=version,
    author="Kamil Stanuch",
    description="Consolidates and analyzes codebases for insights.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamilstanuch/codebase-digest",
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "codebase_digest": ["prompt_library/*.md"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="code analysis, codebase, consolidation, visualization",
    install_requires=read_requirements(),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
    },
    entry_points={
        "console_scripts": [
            "cdigest=codebase_digest.app:main",
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
)