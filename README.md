# Lab 11 – Encrypted Evidence File (Challenge Lab)

**Module:** Secure Communication and Cryptography  
**Module Code:** MACS H6014  
**Team:** Ram Siddharth Ramasamy Raja (A00083573) and Jeyanth Kannan (A00083529)

## Challenge

The Garda supplied a damaged Python encoder (`encryptme.py`) and an intercepted encoded message. The original secret and the encoder's `count` value were missing.

The goal was to reconstruct the encoding process and recover the plaintext from the intercepted message.

## Recovered encoder logic

The recovered script shows three possible transformation steps:

- **step1** – ROT13
- **step2** – Base64 encode
- **step3** – Caesar shift **+4** on lowercase letters

Before the random rounds begin, the encoder creates:

```text
'2' + base64(secret)
```

For every later round it randomly selects step 1, 2 or 3, applies that transformation, and prefixes the corresponding step number to the result.

Conceptually:

```text
a = '2' + base64(secret)

repeat count times:
    choose step k from {1,2,3}
    a = str(k) + step_k(a)
```

The leading digits therefore record the transformation sequence.

## Decoding method

The decoder repeatedly:

1. Reads the first character.
2. Removes the leading step number.
3. Applies the inverse transformation:
   - `1` → ROT13 again
   - `2` → Base64 decode
   - `3` → Caesar shift **-4** on lowercase letters
4. Repeats until the final Base64 layer produces the plaintext.

Because the encoding order is stored in the leading digits, the missing `count` does not need to be guessed.

## Command used

```bash
python3 decryptme.py -v -f intercepted.txt
```

The `-v` option prints each decoded layer.

## Result

```text
Layers peeled: 68
count = 67
Plaintext: Why do elephants have big ears?
```

The 68 peeled layers consist of the initial Base64 layer plus the 67 random encoding rounds.

## Files

- `encryptme.py` – damaged encoder supplied for the challenge.
- `decryptme.py` – Python 3 decoder created to reverse the layered transformations.
- `RESULT.txt` – final recovered result.

The assignment-provided `intercepted.txt` ciphertext is not reproduced in this repository.

## Final plaintext

> **Why do elephants have big ears?**
