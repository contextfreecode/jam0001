import argparse
import subprocess
import sys
from pathlib import Path


def ajo_compile(source: Path):
    # Generate zig.
    result = subprocess.run(
        args=[sys.executable, "-m", "ajo", "--input", source],
        stdout=subprocess.PIPE,
    )
    stdout = result.stdout.decode("utf-8")
    dest = source.parent / source.with_suffix(".zig")
    with open(dest, "w") as out_stream:
        out_stream.write(stdout)
    # Run zig.
    subprocess.run(args=["zig", "run", str(dest)])


def main():
    path = Path(__file__).parent / "test"
    for kid in path.iterdir():
        if kid.suffix == ".ajo":
            ajo_compile(kid)


main()
