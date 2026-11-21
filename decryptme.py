#!/usr/bin/env python3
"""
Decoder for the layered encoding produced by encryptme.py.

How the encoder works:
    start: a = '2' + base64(secret)
    repeat count times:
        pick step k in {1,2,3} at random
        a = str(k) + step_k(a)

    step1 = ROT13 (both cases)       -> digits untouched
    step2 = Base64 encode
    step3 = Caesar +4, lowercase only -> digits untouched

Every layer is tagged by its leading digit. To decode, read the digit,
strip it, apply the inverse, and repeat until the final '2' layer yields
the plaintext.

Usage:
    python3 decryptme.py '<ciphertext>'
    python3 decryptme.py -f message.txt
    python3 decryptme.py -v -f message.txt
"""

import base64
import codecs
import string
import sys


def undo_step1(s):
    # ROT13 is its own inverse
    return codecs.encode(s, "rot_13")


def undo_step2(s):
    # Reverse Base64
    return base64.b64decode(s, validate=True).decode("latin-1")


def undo_step3(s, shift=4):
    # Reverse the lowercase Caesar +4 shift
    lo = string.ascii_lowercase
    return s.translate(str.maketrans(lo[shift:] + lo[:shift], lo))


UNDO = {
    "1": undo_step1,
    "2": undo_step2,
    "3": undo_step3,
}


def decode(ct, verbose=False):
    a = ct.strip()
    layers = 0

    while a and a[0] in UNDO:
        tag, body = a[0], a[1:]

        try:
            nxt = UNDO[tag](body)
        except Exception:
            # Current string is not a valid encoded layer.
            break

        layers += 1

        if verbose:
            preview = nxt[:70]
            suffix = "..." if len(nxt) > 70 else ""
            print(f"[layer {layers}] step{tag} -> {preview}{suffix}")

        a = nxt

    return a, layers


if __name__ == "__main__":
    args = sys.argv[1:]
    verbose = "-v" in args
    args = [x for x in args if x != "-v"]

    if args[:1] == ["-f"]:
        ct = open(args[1]).read()
    elif args:
        ct = args[0]
    else:
        ct = sys.stdin.read()

    plain, n = decode(ct, verbose)

    print(f"\nLayers peeled: {n} (count = {n - 1})")
    print(f"Plaintext: {plain}")
