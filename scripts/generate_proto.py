"""Regenerate bindings locally. No downloads or protoc on PATH required."""
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory)
        for schema in (ROOT / 'protocol').glob('*.proto'):
            shutil.copyfile(schema, source / schema.name)
        # Overrides are explicitly reviewed wire-compatibility corrections.
        for schema in (ROOT / 'protocol' / 'compat').glob('*.proto'):
            shutil.copyfile(schema, source / schema.name)
        subprocess.run([sys.executable, '-m', 'grpc_tools.protoc',
                        '-I' + str(source), '--python_out=' + str(ROOT / 'proto'),
                        *map(str, sorted(source.glob('*.proto')))], check=True)
    for path in (ROOT / 'proto').glob('*_pb2.py'):
        text = path.read_text()
        text = re.sub(r'^import (\w+_pb2) as ', r'from proto import \1 as ', text, flags=re.MULTILINE)
        path.write_text(text)


if __name__ == '__main__': main()
