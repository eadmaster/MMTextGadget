
import os
from mmtxtlib import *

if __name__ == '__main__':
    # Setup bin-input folder
    if not os.path.exists(BIN_INT_PATH):
        os.makedirs(BIN_INT_PATH)

    if not os.path.exists(BIN_INPUT_DATA0_PATH):
        os.makedirs(BIN_INPUT_DATA0_PATH)

    if not os.path.exists(BIN_INPUT_DATA1_PATH):
        os.makedirs(BIN_INPUT_DATA1_PATH)

    if not os.path.exists(BIN_INPUT_ISO_PATH):
        os.makedirs(BIN_INPUT_ISO_PATH)

    # Setup bin-int folder
    if not os.path.exists(BIN_INT_PATH):
        os.makedirs(BIN_INT_PATH)

    # Setup bin-output folder
    if not os.path.exists(BIN_OUTPUT_PATH):
        os.makedirs(BIN_OUTPUT_PATH)

    # Setup tools folder
    if not os.path.exists(TOOLS_PATH):
        os.makedirs(TOOLS_PATH)