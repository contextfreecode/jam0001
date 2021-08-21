import argparse
import ast
import dataclasses as dc
import logging
import textwrap


logger = logging.getLogger(__name__)


Key = str
Type = str


@dc.dataclass
class Context:
    defaults: dict[Key, Type]


def dump(node: ast.AST):
    return ast.dump(node, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    run(**args.__dict__)


def process_class_field(*, context: Context, node: ast.AnnAssign):
    target: ast.Name = node.target
    annotation: ast.Name = node.annotation
    logger.debug(f"{dump(annotation)=}")
    logger.debug(f"{dump(target)=}")
    print(f"    {target.id}: {annotation.id},")


def process_class_def(*, context: Context, node: ast.ClassDef):
    for kid in node.body:
        match kid:
            case ast.AnnAssign():
                process_class_field(context=context, node=kid)
            case ast.Expr(value):
                assert isinstance(value, ast.Name)
                ann_assign = ast.AnnAssign(
                    annotation=ast.Name(context.defaults[value.id]),
                    target=value,
                )
                process_class_field(context=context, node=ann_assign)
            case _:
                logger.warning(f"unhandled: {dump(kid)}")


def process_module(*, context: Context, node: ast.Module):
    # dump(node)
    for kid in node.body:
        match kid:
            case ast.ClassDef():
                print(f"const {kid.name} = struct {{")
                process_class_def(context=context, node=kid)
                print(f"}};")
            case ast.AnnAssign():
                process_var_default(context=context, node=kid)
            case ast.Expr():
                logger.debug(f"unhandled expr: {dump(kid)}")
            case _:
                logger.warning(f"unhandled: {dump(kid)}")


def process_var_default(*, context: Context, node: ast.AnnAssign):
    target: ast.Name = node.target
    annotation: ast.Name = node.annotation
    context.defaults[target.id] = annotation.id


def run(*, input: str):
    with open(input) as input_stream:
        text = input_stream.read()
    tree = ast.parse(text)
    context = Context(defaults={})
    process_module(context=context, node=tree)
    script = f"""
        const std = @import("std");
        pub fn main() void {{
            std.debug.print("Hi!\\n", .{{}});
        }}
    """
    print(textwrap.dedent(script).strip())
