import os
from datetime import datetime

def extract_code(base_dir):
    output = []

    script_path = os.path.abspath(__file__)
    script_name = os.path.basename(script_path)
    excluded_files = {script_name, 'restore.py'}
    file_count = 0

    for root, _, files in os.walk(base_dir):
        for file in files:
            if not file.endswith('.py') or file in excluded_files:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                rel_path = os.path.relpath(file_path, base_dir)
                output.append(f"# === {rel_path} ===\n```python\n{code.rstrip()}\n```\n")
                file_count += 1

            except Exception:
                continue

    combined_code = "\n".join(output)
    return combined_code, file_count

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    code_output, file_count = extract_code(base_dir)

    now = datetime.now()
    header = f"""# Extracted Code (.py)
# Date and Time: {now.strftime("%Y-%m-%d %H:%M:%S")}
# Files Included: {file_count}

"""

    out_path = os.path.join(base_dir, 'data.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(header + code_output)

    print(f"✅ Done! Extracted {file_count} Python file(s) to '{out_path}'")
