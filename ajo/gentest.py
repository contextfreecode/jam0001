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
    # Run zig, and capture out and err.
    run_result = subprocess.run(
        args=["zig", "run", str(dest)],
        capture_output=True,
    )
    run_dest_stdout = source.parent / source.with_suffix(".stdout.txt")
    with open(run_dest_stdout, "w") as dest_stream:
        dest_stream.write(run_result.stdout.decode("utf-8"))
    run_dest_stderr = source.parent / source.with_suffix(".stderr.txt")
    with open(run_dest_stderr, "w") as dest_stream:
        dest_stream.write(run_result.stderr.decode("utf-8"))


def main():
    path = Path(__file__).parent / "test"
    for kid in path.iterdir():
        if kid.suffix == ".ajo":
            ajo_compile(kid)


main()
