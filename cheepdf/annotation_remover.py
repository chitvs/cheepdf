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
from typing import Union, List
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)

class AnnotationRemover:
    
    def __init__(self):
        self.total_removed = 0
        self.removed_types = []
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def remove_annotations(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        backup: bool = True
    ) -> bool:
        
        self.total_removed = 0
        self.removed_types = []
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_path}")
            return False
        
        if not input_path.is_file():
            logger.error(f"Input path is not a file: {input_path}")
            return False
        
        if backup and input_path != output_path:
            if not self._create_backup(input_path):
                logger.warning("Backup creation failed, but continuing with processing...")
        
        try:
            return self._process_pdf(input_path, output_path)
        except Exception as e:
            logger.error(f"Failed to process PDF: {e}")
            return False
    
    def _create_backup(self, input_path: Path) -> bool:
        
        backup_path = input_path.with_suffix(f"{input_path.suffix}.backup")
        
        try:
            if backup_path.exists():
                counter = 1
                while backup_path.with_suffix(f"{backup_path.suffix}.{counter}").exists():
                    counter += 1
                backup_path = backup_path.with_suffix(f"{backup_path.suffix}.{counter}")
            
            shutil.copy2(input_path, backup_path)
            logger.info(f"Backup created at: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def _process_pdf(self, input_path: Path, output_path: Path) -> bool:
        
        doc = None
        
        try:
            doc = fitz.open(str(input_path))
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                annotations = page.annots()
                
                if annotations:
                    for annot in reversed(list(annotations)):
                        try:
                            annot_type = annot.type[1] if annot.type else "Unknown"
                            self.removed_types.append(annot_type)
                            
                            page.delete_annot(annot)
                            self.total_removed += 1
                            
                        except Exception as e:
                            logger.warning(f"Failed to remove annotation on page {page_num + 1}: {e}")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            doc.save(str(output_path))
            
            logger.info(f"Removed {self.total_removed} annotation(s)")
            if self.removed_types:
                unique_types = list(set(self.removed_types))
                logger.info(f"Annotation types removed: {', '.join(unique_types)}")
            logger.info(f"Output saved to: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return False
            
        finally:
            if doc:
                doc.close()
    
    def get_removal_stats(self) -> dict:
        
        return {
            "total_removed": self.total_removed,
            "removed_types": list(set(self.removed_types)),
            "type_counts": {
                annot_type: self.removed_types.count(annot_type) 
                for annot_type in set(self.removed_types)
            }
        }