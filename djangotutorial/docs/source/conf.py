# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django

sys.path.insert(0, os.path.abspath('/workspaces/lesion_guu/djangotutorial'))  # Поднимаемся на уровень проекта Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Замени на имя своего проекта

django.setup()

extensions = [
    'sphinx.ext.autodoc',       # Генерация документации из docstrings
    'sphinx.ext.napoleon',      # Поддержка Google и NumPy docstrings
    'sphinx.ext.viewcode',      # Ссылка на исходный код
]

html_theme = "sphinx_rtd_theme"  # Тема Read the Docs

project = 'LESION_GUU'
copyright = '2025, SetyaminAnton'
author = 'SetyaminAnton'
release = '1.05.2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'LESION_GUU'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
