import os
import argparse

__authors__ = ["Ilya Semennikov"]
__date__ = "2024011"
__description__ = "Directory tree walker"


def generate_tree(path, indent=""):
    tree_str = ""
    try:
        items = os.listdir(path)
    except PermissionError:
        return f"{indent}Permission denied: {path}\n"
    except FileNotFoundError:
        return f"{indent}No such file or directory: {path}\n"

    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = index == len(items) - 1
        tree_str += f"{indent}{'└── ' if is_last else '├── '}{item}\n"

        if os.path.isdir(item_path):
            tree_str += generate_tree(item_path, indent + ("    " if is_last else "│   "))

    return tree_str

def main():
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
        # which displays information about the author and date at the end of the help
    )
    parser.add_argument(
        "DIR_PATH",
        help="Path to the directory to parse. Example syntax for Windows: C:\\Users\\UserName\\Documents\\MyFolder"
    )
    parser.add_argument("-o", "--output", help="Output file to save the tree structure.")

    args = parser.parse_args()

    tree_structure = generate_tree(args.DIR_PATH)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(tree_structure)
        print(f"Tree structure saved to {args.output}")
    else:
        print(tree_structure)


if __name__ == "__main__":
    main()
