import argparse
import ast
import dataclasses as dc
import logging
import textwrap


logger = logging.getLogger(__name__)


Doc = str
Key = str
Type = str


@dc.dataclass
class Context:
    default_docs: dict[Key, Doc]
    default_types: dict[Key, Type]


@dc.dataclass
class VarDef:
    annotation: ast.Name
    doc: str
    target: ast.Name


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
    doc = context.default_docs.get(target.id)
    if doc is not None:
        print(f"    /// {doc}")
    print(f"    {target.id}: {annotation.id},")


def process_class_def(*, context: Context, node: ast.ClassDef):
    for kid_index, kid in enumerate(node.body):
        match kid:
            case ast.AnnAssign():
                process_class_field(context=context, node=kid)
            case ast.Expr(value):
                assert isinstance(value, ast.Name)
                ann_assign = ast.AnnAssign(
                    annotation=ast.Name(context.default_types[value.id]),
                    target=value,
                )
                process_class_field(context=context, node=ann_assign)
            case _:
                logger.warning(f"unhandled: {dump(kid)}")


def process_module(*, context: Context, node: ast.Module):
    # dump(node)
    doc = None
    for kid_index, kid in enumerate(node.body):
        match kid:
            case ast.ClassDef():
                print(f"const {kid.name} = struct {{")
                process_class_def(context=context, node=kid)
                print(f"}};")
            case ast.AnnAssign():
                doc = None
                if kid_index < len(node.body) - 1:
                    match node.body[kid_index + 1]:
                        case ast.Expr(value):
                            if isinstance(value, ast.Constant):
                                doc = textwrap.dedent(value.value).strip()
                                assert isinstance(doc, str)
                process_var_default(context=context, node=kid, doc=doc)
                # logger.info(f"{dump(kid)=}")
            case ast.Expr():
                if doc is None:
                    logger.warning(f"unhandled expr: {dump(kid)}")
                else:
                    doc = None
            case _:
                logger.warning(f"unhandled: {dump(kid)}")


def process_var_default(
    *,
    context: Context,
    node: ast.AnnAssign,
    doc: Doc,
):
    target: ast.Name = node.target
    annotation: ast.Name = node.annotation
    if doc is not None:
        context.default_docs[target.id] = doc
    context.default_types[target.id] = annotation.id


def run(*, input: str):
    with open(input) as input_stream:
        text = input_stream.read()
    tree = ast.parse(text)
    context = Context(default_docs={}, default_types={})
    process_module(context=context, node=tree)
    script = f"""
        const std = @import("std");
        pub fn main() void {{
            std.debug.print("Hi!\\n", .{{}});
        }}
    """
    print(textwrap.dedent(script).strip())
