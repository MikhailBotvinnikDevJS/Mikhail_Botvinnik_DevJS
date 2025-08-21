#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTF Noise Generator + Lost Password Banner
Gera números e palavras aleatórias e mostra (bem visível) a senha "perdida".

Uso:
  python ctf_noise.py --linhas 60 --seed 42
"""

import argparse
import random
import string
import sys
from datetime import datetime

PASSWORD = "chess_is_my_love"

WORD_BANK = [
    "rook","knight","bishop","queen","king","pawn","check","mate",
    "castle","gambit","sicilian","fischer","capablanca","smothered",
    "fork","pin","skewer","zugzwang","tempo","blunder","brilliancy",
]

def rand_word():
    # mistura banco com sílabas, pra variar
    if random.random() < 0.6:
        return random.choice(WORD_BANK)
    syl = ["ka","fi","lo","zu","na","re","mi","to","sha","gra","lor","zen","chi"]
    return "".join(random.choice(syl) for _ in range(random.randint(2,4)))

def rand_hex(n=8):
    return "".join(random.choice("0123456789abcdef") for _ in range(n))

def rand_num():
    return random.randint(10_000, 9_999_999)

def banner(password: str) -> str:
    title = "PASSWORD LOST"
    msg = f"{title}: {password}"
    width = max(len(msg), 40)
    top = "═" * (width + 2)
    side_pad = (width - len(title)) // 2
    mid_title = f"║{' ' * side_pad}{title}{' ' * (width - len(title) - side_pad)}║"
    mid_pass = f"║ {password}{' ' * (width - len(password) - 1)}║"
    lines = [
        f"╔{top}╗",
        mid_title,
        f"╟{'─' * (width + 2)}╢",
        mid_pass,
        f"╚{top}╝",
    ]
    # ANSI brilho para destacar (sem dependências)
    return "\033[1m\033[92m" + "\n".join(lines) + "\033[0m"

def make_noise(lines: int, insert_at: int):
    for i in range(lines):
        if i == insert_at:
            print(banner(PASSWORD))
        # “ruído” (hex + número + palavra)
        print(f"[{i:03d}] hx={rand_hex(8)} num={rand_num():>7} word={rand_word()}")

def save_password(filepath="lost_password.txt"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{PASSWORD}\n")
    return filepath

def main():
    ap = argparse.ArgumentParser(description="CTF noise + lost password")
    ap.add_argument("--linhas", type=int, default=60, help="quantidade de linhas de ruído (default: 60)")
    ap.add_argument("--seed", type=int, default=None, help="seed opcional p/ reprodutibilidade")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    # posição aleatória para inserir o banner
    insert_at = random.randint(0, max(0, args.linhas - 1))

    print(f"# session={rand_hex(12)}  ts={datetime.utcnow().isoformat()}Z")
    print("# generating noise... (proc: rng/words/hex)\n")

    make_noise(args.linhas, insert_at)
    path = save_password()
    print(f"\n# hint: a senha também foi salva em '{path}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
