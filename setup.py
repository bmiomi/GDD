#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script para GDD - Sistema de Gestión de Distribución

Uso:
    pip install .                          # Instalar en modo desarrollo
    pip install -e .                       # Instalar editable (desarrollo)
    python setup.py sdist bdist_wheel      # Crear distribución
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer el contenido del README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Leer requerimientos
requirements = (this_directory / "requeriment.txt").read_text(encoding="utf-8").strip().split('\n')
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    # ═══════════════════════════════════════════════════════════════════════
    # INFORMACIÓN BÁSICA
    # ═══════════════════════════════════════════════════════════════════════
    name="gdd-distribucion",
    version="1.0.0",
    description="Sistema modular de Gestión de Distribución con plugins independientes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tu Nombre/Organización",
    author_email="contacto@example.com",
    url="https://github.com/tu-org/gdd",
    project_urls={
        "Documentation": "https://github.com/tu-org/gdd/blob/main/README.md",
        "Source Code": "https://github.com/tu-org/gdd",
        "Bug Tracker": "https://github.com/tu-org/gdd/issues",
    },
    
    # ═══════════════════════════════════════════════════════════════════════
    # CLASIFICADORES (PyPI)
    # ═══════════════════════════════════════════════════════════════════════
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    
    # ═══════════════════════════════════════════════════════════════════════
    # PACKAGES Y DEPENDENCIAS
    # ═══════════════════════════════════════════════════════════════════════
    packages=find_packages(exclude=["tests", "tests.*", "docs", "*.egg-info"]),
    
    # Incluir archivos de datos (YAML, ejemplos, etc)
    package_data={
        'plugins': [
            'xsales/config.yml',
            'xsales/src/modules/Server/config.yml',
            'xsales/src/modules/Server/enums/enumftp.py',
            'xsales/src/modules/FTP/config.yml',
            'xsales/src/modules/Status/config.yml',
            'bzhelp/*.yml',
        ],
    },
    
    # Archivos incluidos via MANIFEST.in
    include_package_data=True,
    
    # Dependencias
    python_requires=">=3.9",
    install_requires=requirements,
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENTRY POINTS (SCRIPTS)
    # ═══════════════════════════════════════════════════════════════════════
    entry_points={
        'console_scripts': [
            'gdd=main:main',                    # Comando: gdd
            'gdd-validate=validate_deployment:main',  # Comando: gdd-validate
        ],
    },
    
    # ═══════════════════════════════════════════════════════════════════════
    # METADATOS ADICIONALES
    # ═══════════════════════════════════════════════════════════════════════
    keywords=[
        'distribucion',
        'gestion',
        'xsales',
        'reportes',
        'plugins',
        'modular',
    ],
    
    license="MIT",
    zip_safe=False,
)
