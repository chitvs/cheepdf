# CheePDF, a simple PDF annotation remover

**CheePDF** is a lightweight and efficient Python tool to remove annotations from PDF files. It's ideal for cleaning up PDFs by stripping highlights and other markup. Features include:

- Remove highlight annotations from PDF files
- Create automatic backups of original files
- Get detailed information about annotations before removal
- Command-line interface for easy usage

## Installation

### Clone the repository

```bash
git clone https://github.com/chitvs/cheepdf.git
cd cheepdf
```

### Using a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> [!NOTE]  
> On systems like Arch Linux or Debian, installing Python packages system-wide with `pip` may fail due to [PEP 668](https://peps.python.org/pep-0668/). Using a virtual environment avoids these issues.

## Quick start

### Usage

Remove annotations from a PDF:

```bash
cheepdf input.pdf
```

Specify output file:

```bash
cheepdf input.pdf output.pdf
```

Get annotation information without removing them:

```bash
cheepdf input.pdf --info-only
```

Remove annotations without creating a backup:

```bash
cheepdf input.pdf --no-backup
```

## Options

```
cheepdf <input.pdf> [output.pdf] [options]

Arguments:
  input.pdf     Path to the input PDF file
  output.pdf    Path to the output PDF file (optional, defaults to 'output_cleaned.pdf')

Options:
  --info-only   Display annotation information without removing them
  --no-backup   Skip creating a backup of the original file
  --help        Show this help message
```

## Requirements

- Python
- PyMuPDF (fitz) >= 1.20.0

## Version history

### v1.0.0

- Initial release
- Basic annotation removal functionality
- Command-line interface
- Backup creation
- Annotation information gathering

## Acknowledgments

CheePDF is built using [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing.

## License

This project is licensed under the GNU Affero General Public License v3.0 – see the [LICENSE](LICENSE) file for details.
