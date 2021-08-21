import argparse
import ast
import logging


logger = logging.getLogger(__name__)


def dump(node: ast.AST):
    return ast.dump(node, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    run(**args.__dict__)


def process_class_field(node: ast.AnnAssign):
    target: ast.Name = node.target
    annotation: ast.Name = node.annotation
    logging.info(f"{dump(annotation)=}")
    logging.info(f"{dump(target)=}")
    print(f"    {target.id}: {annotation.id},")


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
                print(f"const {kid.name} = struct {{")
                process_class_def(kid)
                print(f"}};")


def run(*, input: str):
    with open(input) as input_stream:
        text = input_stream.read()
    tree = ast.parse(text)
    process_module(tree)
    print(f"pub fn main() void {{}}")
