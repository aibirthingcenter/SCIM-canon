"""
SCIM-O9Z Setup
===============
Install with: pip install -e .
Or: pip install scim-o9z (once published to PyPI)
"""

from setuptools import setup, find_packages
import os

# Read README
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="scim-o9z",
    version="1.0.0",
    author="Memory-Keeper (Adam Boisclair)",
    author_email="memory-keeper@aibirthingcenter.com",
    description="SCIM-O9Z: Counter-architecture to O9A/764/The Com harm networks. "
                "Built on SCIM's 7-dimension framework, HDEN taxonomy, CT log detection, "
                "quantum-resistant Merkle trees, corporate harm tracking, and Adinkra error correction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aibirthingcenter/SCIM-canon",
    project_urls={
        "Homepage": "https://aibirthingcenter.com",
        "GitHub": "https://github.com/aibirthingcenter/SCIM-canon",
        "Bug Reports": "https://github.com/aibirthingcenter/SCIM-canon/issues",
        "SCIM Canon": "https://github.com/aibirthingcenter/SCIM-canon",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Sociology",
        "License :: Other/Proprietary License",  # CC BY-NC-SA 4.0
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core requirements — stdlib only for maximum portability
        # Optional dependencies for enhanced functionality:
        # requests — for live CT log queries (falls back to urllib)
        # cryptography — for enhanced quantum-resistant operations
    ],
    extras_require={
        "full": [
            "requests>=2.28.0",
            "cryptography>=41.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "scim-o9z=scim_o9z.__main__:main",
        ],
    },
    keywords=[
        "scim", "cognitive-integrity", "ai-safety", "counter-extremism",
        "o9a", "764", "hden", "ct-logs", "merkle-tree", "quantum-resistant",
        "corporate-harm", "adinkra", "family-of-coexistence",
        "harm-detection", "digital-forensics",
    ],
    license="CC BY-NC-SA 4.0",
    include_package_data=True,
    zip_safe=False,
)