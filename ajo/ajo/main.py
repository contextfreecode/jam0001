import argparse
import ast


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    args = parser.parse_args()
    run(**args.__dict__)


def run(*, input: str):
    with open(input) as input_stream:
        text = input_stream.read()
    tree = ast.parse(text)
    print(ast.dump(tree, indent=4))
