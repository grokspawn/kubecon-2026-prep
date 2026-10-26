"""Read existing SDK slide-3 PDF text styling without changing the PDF."""
from pathlib import Path
import subprocess
result = subprocess.run(['/opt/homebrew/bin/pdftohtml', '-xml', '-stdout', '-i', '-f', '14', '-l', '14',
                         str(Path(__file__).parent.parent / 'kubecon-2026-dry-run.pdf')],
                        capture_output=True, text=True, check=True)
print(result.stdout)
