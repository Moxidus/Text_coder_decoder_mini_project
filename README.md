# Text Encoder Decoder - Mini Project
 
This is a simple Text Encoder Decoder that currently has 2 encryption methods:
* Custom Cipher symmetric encryption algorithm it encrypts text using a passkey by XOR-ing each byte against a key stream derived from the passkey and randomly generated salt
    * loosely inspired by ChaCha20
    * The cipher includes PKCS#7-style padding
    * checksum for passkey verification
    * and per-block key rotation for added diffusion.
* Caesar Cipher - Caesar cipher is there just as a placeholder for other encryption algorithms
 
Simple GUI created in NiceGui python package

## Main Dependencies
 
* NiceGui
* PyTest
* numpy
* os
* pathlib
* pyperclip


## Installation Instructions
 
### Option 1: Download Executable
 
1. Go to the [Releases](../../releases) page.
2. Download the latest `.exe` file.
3. Run the executable.


### Option 2: Run from Python Source
 
VsCode IDE is strongly recommended as this repo includes all .vscode files that will setup the project by itself
 
```bash
# TODO: clone repo
# TODO: install dependencies from requirements.txt and requirements-dev.txt
# TODO: run the app
```
 
## Ethical Statement

This project is intended for educational and lawful use only. Do not use software for any actual encryption as it was not tested and may contain vulnerabilities software is delivered as is with out any warranty. 
 
## Contribution Statement
 
Project was created by solely by me
 
## Acknowledgements
 
None
 