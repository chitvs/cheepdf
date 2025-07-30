#!/usr/bin/env python3

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

import sys
import argparse
from pathlib import Path
from .annotation_remover import AnnotationRemover
from .pdf_parser import PDFParser


def create_parser():
    parser = argparse.ArgumentParser(
        prog="cheepdf",
        description="Remove annotations from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cheepdf document.pdf                    # Remove annotations, save as output_cleaned.pdf
  cheepdf input.pdf output.pdf            # Remove annotations, save as output.pdf
  cheepdf document.pdf --info-only        # Show annotation info without removing
  cheepdf document.pdf --no-backup        # Remove annotations without backup
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input PDF file path"
    )
    
    parser.add_argument(
        "output_file",
        nargs="?",
        default="output_cleaned.pdf",
        help="Output PDF file path (default: output_cleaned.pdf)"
    )
    
    parser.add_argument(
        "--info-only",
        action="store_true",
        help="Display annotation information without removing them"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating a backup of the original file"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="cheepdf 1.0.0"
    )
    
    return parser


def display_annotation_info(parser):
    try:
        info = parser.get_annotations_info()
        page_count = parser.get_page_count()
        
        print("\n" + "="*50)
        print("PDF ANNOTATION SUMMARY")
        print("="*50)
        print(f"Total pages: {page_count}")
        print(f"Total annotations: {info['total_annotations']}")
        
        if info['annotation_types']:
            print(f"Annotation types: {', '.join(info['annotation_types'])}")
        else:
            print("Annotation types: None")
        
        if info['pages_with_annotations']:
            print("\nPages with annotations:")
            for entry in info['pages_with_annotations']:
                print(f"   Page {entry['page']:3d}: {entry['count']:2d} annotation(s)")
        else:
            print("\nNo annotations found in this PDF")
        
        print("="*50)
        
    except Exception as e:
        print(f"Error getting annotation information: {e}")
        return False
    
    return True


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    pdf_parser = PDFParser(args.input_file)
    
    try:
        pdf_parser.validate_file()
        print(f"PDF file validated: {args.input_file}")
        
    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)
    
    if args.info_only:
        success = display_annotation_info(pdf_parser)
        pdf_parser.close()
        sys.exit(0 if success else 1)
    
    print(f"Processing: {args.input_file}")
    
    try:
        info = pdf_parser.get_annotations_info()
        if info['total_annotations'] == 0:
            print("No annotations found - nothing to remove")
            pdf_parser.close()
            return
        else:
            print(f"Found {info['total_annotations']} annotation(s) to remove")
    except Exception as e:
        print(f"Warning: Could not analyze annotations: {e}")
    
    pdf_parser.close()
    
    remover = AnnotationRemover()
    backup = not args.no_backup
    
    success = remover.remove_annotations(
        args.input_file, 
        args.output_file, 
        backup=backup
    )
    
    if success:
        print("Annotations removed successfully!")
        if remover.total_removed > 0:
            print(f"Removed {remover.total_removed} annotation(s)")
            if remover.removed_types:
                unique_types = list(set(remover.removed_types))
                print(f"Types removed: {', '.join(unique_types)}")
        print(f"Output saved to: {args.output_file}")
    else:
        print("Failed to remove annotations")
        sys.exit(1)


if __name__ == "__main__":
    main()