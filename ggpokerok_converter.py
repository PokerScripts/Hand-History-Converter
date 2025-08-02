#!/usr/bin/env python3

import os
import re
import argparse
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description='Конвертер HH от ggpokerok в формат pokerstars.')
    parser.add_argument('format', choices=['pokerstars'], help='Формат назначения (только pokerstars поддерживается)')
    parser.add_argument('input_dir', help='Путь к папке с .txt файлами от ggpokerok')
    return parser.parse_args()

def normalize_line(line):
    # Примеры преобразования (упрощённо — дополни под свой HH формат)
    line = line.strip()

    # Преобразование валюты
    line = re.sub(r'(\d+)\s*bb', lambda m: f"${float(m.group(1)):0.2f}", line)

    # Преобразование действия игроков
    line = re.sub(r'(\w+)\s+bets\s+(\d+)', r'\1: bets $\2.00', line)
    line = re.sub(r'(\w+)\s+calls\s+(\d+)', r'\1: calls $\2.00', line)
    line = re.sub(r'(\w+)\s+raises\s+to\s+(\d+)', r'\1: raises to $\2.00', line)
    line = re.sub(r'(\w+)\s+folds', r'\1: folds', line)

    return line

def convert_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        converted_lines = []
        for line in lines:
            if 'GGPokerOK' in line or 'Hand History' in line:
                continue  # удаляем служебную информацию
            converted_lines.append(normalize_line(line))

        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write('\n'.join(converted_lines))

        print(f"[✓] Converted {input_path.name} → {output_path}")
    except Exception as e:
        print(f"[!] Failed to convert {input_path.name}: {e}")

def main():
    args = parse_arguments()

    input_dir = Path(args.input_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[!] Указанная папка не найдена: {input_dir}")
        return

    output_dir = Path('converted')
    output_dir.mkdir(exist_ok=True)

    for file in input_dir.glob('*.txt'):
        output_file = output_dir / file.name
        convert_file(file, output_file)

if __name__ == '__main__':
    main()