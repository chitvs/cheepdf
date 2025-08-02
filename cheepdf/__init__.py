"""
CheePDF -- A simple PDF annotation remover.
"""

from .annotation_remover import AnnotationRemover
from .pdf_parser import PDFParser

__version__ = "1.0.0"
__author__ = "Alessandro Chitarrini"

__all__ = ["AnnotationRemover", "PDFParser"]