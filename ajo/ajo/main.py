import argparse
import ast


def dump(node: ast.AST):
    print(ast.dump(node, indent=4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    args = parser.parse_args()
    run(**args.__dict__)


def process_class_field(node: ast.AnnAssign):
    match node:
        case ast.AnnAssign(annotation, target):
            print("annotation")
            dump(annotation)
            print("target")
            dump(target)


def process_class_def(node: ast.ClassDef):
    for kid in node.body:
        match kid:
            case ast.AnnAssign():
                process_class_field(kid)


def process_module(node: ast.Module):
    # dump(node)
    for kid in node.body:
        match kid:
            case ast.ClassDef():
                process_class_def(kid)


def run(*, input: str):
    with open(input) as input_stream:
        text = input_stream.read()
    tree = ast.parse(text)
    process_module(tree)
