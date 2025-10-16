#!/usr/bin/env python3
"""
Gen-Pass Enterprise Security Suite - Setup Configuration
========================================================

Enterprise-grade Python package setup for the Gen-Pass password
security suite. Includes all necessary metadata, dependencies,
and configuration for professional deployment.

Author: Gen-Spider Security Systems
License: MIT (Enterprise Edition Available)
Copyright: 2024 Gen-Spider Security Systems
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
from distutils.command.build_ext import build_ext
import subprocess

# Package metadata
PACKAGE_NAME = "genpass-enterprise"
VERSION = "3.2.1"
AUTHOR = "Gen-Spider Security Systems"
AUTHOR_EMAIL = "security@genspider.security"
DESCRIPTION = "Enterprise-grade password generation and security analysis suite"
URL = "https://github.com/Gen-Spider/Gen-pass"
LICENSE = "MIT"

# Read long description from README
def read_long_description():
    """Read the long description from README.md"""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return DESCRIPTION

# Read requirements from files
def read_requirements(filename):
    """Read requirements from a requirements file"""
    req_path = Path(__file__).parent / filename
    if req_path.exists():
        with open(req_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            # Filter out comments and empty lines
            return [line.strip() for line in lines 
                   if line.strip() and not line.strip().startswith('#')]
    return []

# Core requirements
core_requirements = [
    "cryptography>=41.0.0",
    "rich>=13.5.0",
    "colorama>=0.4.6",
    "click>=8.1.7",
    "pydantic>=2.4.0",
    "fastapi>=0.103.0",
    "uvicorn[standard]>=0.23.0",
    "structlog>=23.1.0",
    "python-dotenv>=1.0.0",
    "passlib[argon2,bcrypt]>=1.7.4",
    "PyNaCl>=1.5.0",
    "jsonschema>=4.19.0",
    "requests>=2.31.0",
    "psutil>=5.9.5",
]

# Enterprise requirements (optional)
enterprise_requirements = [
    "ldap3>=2.9.1",
    "PyJWT>=2.8.0",
    "oauthlib>=3.2.2",
    "SQLAlchemy>=2.0.0",
    "redis[hiredis]>=5.0.0",
    "celery>=5.3.0",
    "prometheus-client>=0.17.1",
    "kubernetes>=27.2.0",
    "boto3>=1.28.0",
]

# Development requirements
dev_requirements = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.1",
    "black>=23.7.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
    "bandit>=1.7.5",
    "safety>=2.3.5",
    "pre-commit>=3.4.0",
]

# Documentation requirements
doc_requirements = [
    "sphinx>=7.1.0",
    "sphinx-rtd-theme>=1.3.0",
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.2.0",
]

# Platform-specific requirements
platform_requirements = {
    'win32': [
        'pywin32>=306',
        'wmi>=1.5.1',
        'comtypes>=1.2.0',
    ],
    'linux': [
        'linux-proc>=0.7.0',
    ],
    'darwin': [
        # macOS specific packages would go here
    ]
}

# Add platform-specific requirements
if sys.platform in platform_requirements:
    core_requirements.extend(platform_requirements[sys.platform])

# C Extensions for performance (optional)
extensions = []

# Try to build C extensions for better performance
try:
    extensions.append(
        Extension(
            'genpass._speedups',
            sources=[
                'src/c_extensions/entropy.c',
                'src/c_extensions/patterns.c',
            ],
            include_dirs=['src/c_extensions/include'],
            extra_compile_args=['-O3', '-Wall'],
        )
    )
except Exception:
    # C extensions are optional
    pass

class CustomInstall(install):
    """Custom installation to handle post-install setup"""
    
    def run(self):
        install.run(self)
        self.post_install_setup()
    
    def post_install_setup(self):
        """Perform post-installation setup tasks"""
        print("\n" + "="*60)
        print("Gen-Pass Enterprise Security Suite - Installation Complete")
        print("="*60)
        
        # Create configuration directories
        config_dirs = [
            Path.home() / '.genpass',
            Path.home() / '.genpass' / 'configs',
            Path.home() / '.genpass' / 'logs',
            Path.home() / '.genpass' / 'policies',
        ]
        
        for config_dir in config_dirs:
            config_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created config directory: {config_dir}")
        
        # Set up default configuration
        default_config = Path.home() / '.genpass' / 'config.yaml'
        if not default_config.exists():
            with open(default_config, 'w') as f:
                f.write("""
# Gen-Pass Enterprise Configuration
version: "3.2.1"
security:
  level: "standard"
  entropy_threshold: 50.0
  compliance_mode: "nist"
logging:
  level: "INFO"
  format: "structured"
api:
  enabled: false
  host: "127.0.0.1"
  port: 8443
""")
            print(f"Created default configuration: {default_config}")
        
        print("\nNext Steps:")
        print("1. Run: genpass --help")
        print("2. Try: genpass generate --length 16")
        print("3. View: genpass interactive")
        print("\nEnterprise Support: enterprise@genspider.security")
        print("Documentation: https://docs.genspider.security")
        print("="*60)

class CustomDevelop(develop):
    """Custom development installation"""
    
    def run(self):
        develop.run(self)
        print("\nDevelopment installation complete!")
        print("Run 'pre-commit install' to set up git hooks.")

# Entry points for command-line tools
entry_points = {
    'console_scripts': [
        'genpass=src.cli:main',
        'genpass-enterprise=src.cli:main',
        'genpass-server=src.api.server:main',
        'genpass-worker=src.workers.celery_worker:main',
    ],
}

# Classifiers for PyPI
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Information Technology",
    "Topic :: Security :: Cryptography",
    "Topic :: Security",
    "Topic :: System :: Systems Administration :: Authentication/Directory",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: C",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Natural Language :: English",
]

# Keywords for discovery
keywords = [
    "password", "security", "cryptography", "enterprise", "compliance",
    "nist", "fips", "authentication", "authorization", "cybersecurity",
    "infosec", "pentesting", "audit", "policy", "governance",
    "encryption", "hashing", "entropy", "random", "generator",
]

# Project URLs
project_urls = {
    "Homepage": URL,
    "Documentation": "https://docs.genspider.security",
    "Source Code": URL,
    "Bug Tracker": f"{URL}/issues",
    "Security Policy": f"{URL}/security",
    "Enterprise Sales": "https://genspider.security/enterprise",
    "Support": "https://support.genspider.security",
    "Release Notes": f"{URL}/releases",
}

# Package data to include
package_data = {
    'genpass': [
        'data/wordlists/*.txt',
        'data/policies/*.json',
        'data/policies/*.yaml',
        'templates/*.html',
        'templates/*.css',
        'templates/*.js',
        'static/*',
        'schemas/*.json',
    ]
}

# Data files to include
data_files = [
    ('share/genpass/docs', ['docs/README.md']),
    ('share/genpass/examples', [
        'examples/basic_usage.py',
        'examples/enterprise_deployment.py',
        'examples/policy_configuration.yaml',
    ]),
]

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=read_long_description(),
        long_description_content_type="text/markdown",
        url=URL,
        project_urls=project_urls,
        license=LICENSE,
        
        # Package discovery
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        package_data=package_data,
        data_files=data_files,
        include_package_data=True,
        
        # Dependencies
        install_requires=core_requirements,
        extras_require={
            'enterprise': enterprise_requirements,
            'dev': dev_requirements,
            'docs': doc_requirements,
            'all': enterprise_requirements + dev_requirements + doc_requirements,
        },
        
        # Python version requirement
        python_requires=">=3.8",
        
        # Entry points
        entry_points=entry_points,
        
        # C Extensions
        ext_modules=extensions,
        
        # Custom commands
        cmdclass={
            'install': CustomInstall,
            'develop': CustomDevelop,
        },
        
        # Metadata
        classifiers=classifiers,
        keywords=keywords,
        
        # Security
        zip_safe=False,  # For security, don't create zip files
        
        # Build configuration
        options={
            'build_ext': {
                'inplace': True,
            },
            'egg_info': {
                'tag_build': '',
                'tag_date': False,
            },
        },
    )
