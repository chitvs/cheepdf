"""
This file is part of CheePDF.

CheePDF is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CheePDF is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with CheePDF. If not, see <https://www.gnu.org/licenses/agpl-3.0.en.html>.
"""

import fitz  # PyMuPDF
import os
from typing import Optional, List, Dict, Any
from pathlib import Path


class PDFParser:
   
    def __init__(self, file_path: str):
        self.file_path = str(Path(file_path).resolve())
        self.document: Optional[fitz.Document] = None
        self._is_valid = False
    
    def validate_file(self) -> bool:
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        if not os.path.isfile(self.file_path):
            raise ValueError(f"Path is not a file: {self.file_path}")
        
        if not self.file_path.lower().endswith('.pdf'):
            raise ValueError("File must have .pdf extension")
        
        if os.path.getsize(self.file_path) == 0:
            raise ValueError("PDF file is empty")
        
        try:
            self.document = fitz.open(self.file_path)
            
            if len(self.document) == 0:
                raise ValueError("PDF file contains no pages")
            
            self._is_valid = True
            return True
            
        except Exception as e:
            raise ValueError(f"Invalid PDF file: {str(e)}")
    
    def get_page_count(self) -> int:
        if not self._is_valid or not self.document:
            raise RuntimeError("PDF not loaded. Call validate_file() first.")
        
        return len(self.document)
    
    def get_annotations_info(self) -> Dict[str, Any]:
        if not self._is_valid or not self.document:
            raise RuntimeError("PDF not loaded. Call validate_file() first.")
        
        annotation_info = {
            'total_annotations': 0,
            'pages_with_annotations': [],
            'annotation_types': set(),
            'annotation_details': []
        }
        
        for page_num in range(len(self.document)):
            page = self.document[page_num]
            annotations = page.annots()
            
            if annotations:
                page_annot_count = 0
                page_annotations = []
                
                for annot in annotations:
                    try:
                        annot_type = "Unknown"
                        if hasattr(annot, 'type') and annot.type:
                            if isinstance(annot.type, (list, tuple)) and len(annot.type) > 1:
                                annot_type = annot.type[1]
                            elif isinstance(annot.type, str):
                                annot_type = annot.type
                        
                        annotation_info['annotation_types'].add(annot_type)
                        
                        content = ""
                        if hasattr(annot, 'content') and annot.content:
                            content = str(annot.content)
                        
                        author = ""
                        if hasattr(annot, 'info') and annot.info and isinstance(annot.info, dict):
                            author = annot.info.get("title", "")
                        
                        rect = None
                        if hasattr(annot, 'rect') and annot.rect:
                            try:
                                rect = list(annot.rect)
                            except (TypeError, ValueError):
                                rect = None
                        
                        annot_details = {
                            'page': page_num + 1,
                            'type': annot_type,
                            'content': content,
                            'author': author,
                            'rect': rect
                        }
                        
                        annotation_info['annotation_details'].append(annot_details)
                        page_annotations.append(annot_details)
                        annotation_info['total_annotations'] += 1
                        page_annot_count += 1
                        
                    except Exception as e:
                        print(f"Warning: Could not process annotation on page {page_num + 1}: {type(e).__name__}: {e}")
                        annotation_info['total_annotations'] += 1
                        page_annot_count += 1
                
                if page_annot_count > 0:
                    annotation_info['pages_with_annotations'].append({
                        'page': page_num + 1,
                        'count': page_annot_count,
                        'annotations': page_annotations
                    })
        
        annotation_info['annotation_types'] = list(annotation_info['annotation_types'])
        return annotation_info

    def get_pdf_metadata(self) -> Dict[str, Any]:
        if not self._is_valid or not self.document:
            raise RuntimeError("PDF not loaded. Call validate_file() first.")
        
        metadata = self.document.metadata
        
        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'modification_date': metadata.get('modDate', ''),
            'page_count': len(self.document),
            'file_size': os.path.getsize(self.file_path),
            'encrypted': self.document.is_encrypted,
            'pdf_version': self.document.pdf_version() if hasattr(self.document, 'pdf_version') else 'Unknown'
        }
    
    def is_encrypted(self) -> bool:
        if not self._is_valid or not self.document:
            raise RuntimeError("PDF not loaded. Call validate_file() first.")
        
        return self.document.is_encrypted
    
    def close(self):
        if self.document:
            self.document.close()
            self.document = None
            self._is_valid = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()