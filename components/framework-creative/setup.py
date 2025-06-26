from setuptools import setup, find_packages

setup(
    name="framework-creative",
    version="1.0.0",
    description="Creative Frameworks Component for Copy DNA Analysis",
    author="Automatic Copy Writing System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "jieba>=0.42.1",
        "wordcloud>=1.9.2",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "copy-dna-audit=framework_12_copy_dna:main",
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