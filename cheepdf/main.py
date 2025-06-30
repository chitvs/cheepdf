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
from pathlib import Path
from cheepdf.annotation_remover import AnnotationRemover
from cheepdf.pdf_parser import PDFParser

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.pdf> [output.pdf] [--info-only] [--no-backup]")
        sys.exit(1)

    input_file = sys.argv[1]
    input_path = Path(input_file)

    if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
        output_file = sys.argv[2]
    else:
        output_file = str(input_path.parent / "output_cleaned.pdf")

    info_only = "--info-only" in sys.argv
    backup = "--no-backup" not in sys.argv

    parser = PDFParser(input_file)

    try:
        parser.validate_file()
    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

    if info_only:
        info = parser.get_annotations_info()
        print("\nAnnotation Summary:")
        print(f"Pages: {parser.get_page_count()}")
        print(f"Total annotations: {info['total_annotations']}")
        print(f"Annotation types: {', '.join(info['annotation_types'])}")
        if info['pages_with_annotations']:
            print("Pages with annotations:")
            for entry in info['pages_with_annotations']:
                print(f"  Page {entry['page']}: {entry['count']} annotations")
        parser.close()
        return

    remover = AnnotationRemover()
    success = remover.remove_annotations(input_file, output_file, backup=backup)

    if success:
        print("Annotations removed successfully.")
    else:
        print("Failed to remove annotations.")

if __name__ == "__main__":
    main()
