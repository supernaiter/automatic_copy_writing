from setuptools import setup, find_packages

setup(
    name="framework-analysis",
    version="1.0.0",
    description="Analysis Frameworks Component for Market and Competitive Analysis",
    author="Automatic Copy Writing System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "pytrends>=4.9.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "share-of-search=framework_05_share_of_search:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 