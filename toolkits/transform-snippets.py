import json
import sys
import argparse
import re


def escape_snippet_body(text: str):
    """
    转义文本以适应VSCode snippets的body格式
    """
    # 逐行读取
    ret = []
    for line in text.splitlines():
        line = line.replace('"', '\"')

        # 添加到结果
        ret.append(line)

    return ret


def convert_to_snippet(text, prefix, description="", scope=""):
    """
    将文本转换为VSCode snippet格式
    """
    lines: list[str] = escape_snippet_body(text)

    snippet = {"prefix": prefix, "body": lines, "description": description}

    if scope:
        snippet["scope"] = scope

    return snippet


def read_input_text(input_source):
    """
    从文件或标准输入读取文本
    """
    # 从文件读取
    with open(input_source, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description='将原始文本转换为VSCode snippets格式')
    parser.add_argument('input', nargs='?', default='ipt.xml', help='输入文件路径（使用 - 表示从标准输入读取）')
    parser.add_argument('-p', '--prefix', default='uprefix', help='snippet的前缀（触发词）')
    parser.add_argument('-d', '--description', default='udesc', help='snippet的描述')
    parser.add_argument('-s', '--scope', default='xml', help='snippet的作用域（如：python, javascript）')
    parser.add_argument('-o', '--output', help='输出文件路径（默认输出到标准输出）')
    parser.add_argument('--full-json', action='store_true', help='输出完整的snippets JSON文件')

    args = parser.parse_args()

    # 读取输入文本
    try:
        input_text = read_input_text(args.input)
    except Exception as e:
        print(f"错误：无法读取输入 - {e}", file=sys.stderr)
        sys.exit(1)

    if not input_text.strip():
        print("错误：输入文本为空", file=sys.stderr)
        sys.exit(1)

    # 转换为snippet
    snippet = convert_to_snippet(input_text, args.prefix, args.description, args.scope)

    # 输出结果
    output_text = ""
    if args.full_json:
        # 输出完整的snippets JSON
        snippets_dict = {f"{args.prefix} snippet": snippet}
        output_text = json.dumps(snippets_dict, indent=2, ensure_ascii=False)
    else:
        # 只输出当前snippet
        output_text = json.dumps(snippet, indent=2, ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"Snippet已保存到: {args.output}")
        except Exception as e:
            print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
