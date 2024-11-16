
<h1 align="center">
  <b>MMTextGadget</b>
  <br>
  <b>An Ape Escape: Million Monkeys English Patch</b>
  <br>
</h1>

# Overview
MMTextGadget is a tool to patch the PS2 game Ape Escape: Million Monkeys from Japanese to English.

This project currently patches `72%` or `2900 / 4021` of the found strings from Japanese to English, with most GUI text fully translated.
Names of characters, gadgets, special attacks, etc. are sourced from the English version of Ape Escape 1 and Ape Escape: Pumped and Primed. 
(Kakeru -> Spike, Mecha Bo -> Stun Club, etc.)

<p align="center">
  <img src="docs/img1.png" width="375" height="250" /> <img src="docs/img2.png" width="375" height="250" />
  <br>
  <img src="docs/img3.png" width="375" height="250" /> <img src="docs/img4.png" width="375" height="250" />
</p>

## How to apply patch

### XDelta Patch (Recommended)
An xdelta patch and can be found under Releases. XdeltaUI can be used to apply the patch, a copy can be downloaded from https://www.romhacking.net/utilities/598/

### Build the project from scratch
Building the project from scratch will generate a new iso to play. Only recommended for those who wish to make changes to the project. Instructions are further below.

## Passwords
Million Monkeys uses a Password System similar to 3 and Pumped and Primed to unlock special content. These passwords have been changed to the ones found in the chinese version of Million Monkeys which use English.

All Passwords are under `PASSWORDS.md`. For first time players it is recommended to do a full playthrough of either Spike's or Specter's Story Mode and to complete all the tournaments in Colosseum Mode before reading.

# If you want to build the project from scratch, continue reading below

## Project Structure
```
MMTextGadget
├───bin-input:    (Generated from env.setup.py) Files needed to generate the patched .iso
    ├───DATA0:    Place DATA0.BIN as per the Patch Instructions here
    ├───DATA1:    Place the files from the DATA1 folder generated as per the Patch Instructions here
    └───ISO:      Place your Ape Escape Million Monkeys .iso renamed to base.iso as per the Patch Instructions here
├───bin-int:      (Generated from env.setup.py) Intermediate files created during patching
├───bin-output:   (Generated from env.setup.py) Patched game .iso will be created here
├───src:          Source Code for generating a patched .iso
└───tools:        (Generated from env.setup.py) External Tools used during patching
    └───quickbms: Place quickbms here
├───README.md:    The file you are currently reading.
├───PAsSwORDS.md: A list of passwords for unlocking special content. A full playthrough is recommended before reading.
 ```

## Prerequisites

- A Japanese iso of Ape Escape: Million Monkeys, the Chinese version is not supported.
- quickBMS must be downloaded from here https://aluigi.altervista.org/papers/quickbms.zip and placed in the tools folder.
  - The quickBMS script `ape_escape_inf_bin.bms` used to extract the DATA*.bin files from the ISO must also be downloaded from the following link https://aluigi.altervista.org/bms/ape_escape_inf_bin.bms and placed witin the quickBMS folder.
- Python 3 must be installed on the computer. A copy can be downloaded from https://www.python.org/downloads/ (Python 3.12.5 was used during testing)
- (Optional) XdeltaUI can be used for creating / applying an english patch. A copy can be downloaded from https://www.romhacking.net/utilities/598/

## Project Setup

1. Open command prompt from the `src` folder and run `python env_setup.py` to setup the folders needed during the patch process.
2. Place your copy of Million Monkeys within the `bin-input\ISO` folder and rename it to `base.iso`.
3. Extract the `PDATA` folder from your iso and place it within `tools\quickbms` (7zip is recommended for extracting PS2 ISOs)
4. Open command prompt from within the `tools\quickbms` folder and run `quickbms.exe ape_escape_inf_bin.bms PDATA\DATA0.BIN DATA1` Move the resulting `DATA1` folder to `bin-input`
5. Copy `DATA0.BIN` from the `PDATA` folder you extracted in the previous step to `bin-input\DATA0`
6. Open command prompt from the `src` folder and run `python txt_inject.py` to translate the text to english based on `jptxt.csv`. This will generate `mm_en_patch.iso` which contains the english patched text.
7. (Optional) Create a patch file from `base.iso` and `mm_en_patch.iso` using XDelta.




