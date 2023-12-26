import argparse
import os
from sys import exit

from collections import defaultdict
from heapq import heappush, heappop
from huffmantree import HuffTree

def get_codes_from_tree(tree: HuffTree, cod: str, code_map: dict) -> dict:
    if tree.root.is_leaf():
        code_map[tree.root._value] = cod
        return
    get_codes_from_tree(tree.root._left, cod + '0', code_map)
    get_codes_from_tree(tree.root._right, cod + '1', code_map)


def get_tree_from_codes(code_map: dict) -> HuffTree:

    root = HuffTree('', None, None)
    for key, val in code_map.items():
        curr = root
        for char in val:
            if char == '0':
                if curr.root._left is None:
                    curr.root._left = HuffTree('', None, None)
                curr = curr.root._left
            else:
                if curr.root._right is None:
                    curr.root._right = HuffTree('', None, None)
                curr = curr.root._right
        curr.root._value = key
        curr.root._leaf = True
    return root

def encode(code_map: dict, to_encode: str) -> str:
    encoded = ''
    for char in to_encode:
        encoded += code_map[char]

    msg_len = len(encoded)
    integer = int(encoded, 2)
    compressed = integer.to_bytes((integer.bit_length() + 7) // 8, byteorder='big')
    return msg_len, compressed


def decode(code_map: dict, encoded: str) -> str:

    tree = get_tree_from_codes(code_map)
    curr = tree
    decoded = ''
    for char in encoded:
        if char == '0':
            curr = curr.root._left
        else:
            curr = curr.root._right
        if curr.root.is_leaf():
            decoded += curr.root._value
            curr = tree
    return decoded


def find_freq(filename: str) -> dict:

    freq_dict = defaultdict(int)
    with open(filename, 'rb') as f:
        data = f.readlines()
        for line in data:
            for char in line:
                freq_dict[chr(char)] += 1

    return freq_dict


def build_tree(freq_dict: dict) -> HuffTree:

    heap = []
    for key, val in freq_dict.items():
        heappush(heap, HuffTree(key, val))

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        heappush(heap, HuffTree(left.weight() + right.weight(), left, right))

    return heap[0]



def compress(filename: str, output: str) -> None:

    """
    Compresses the file
    """

    f_dict = find_freq(filename) #find the frequency of each character in the file
    final_tree = build_tree(f_dict) #build the huffman tree
    code_map = {}
    get_codes_from_tree(final_tree, '', code_map) #get the codes from the tree

    msg_len, encoded = encode(code_map, open(filename, 'r').read()) #encode the file
    output = output + '.compressed'
    with open(output, 'wb') as f:
        f_dict = dict(f_dict)
        f.write(str(f_dict).encode())
        f.write(b'\n')
        f.write(str(msg_len).encode())
        f.write(b'\n')
        f.write(encoded)


def decompress(filename: str, output: str) -> None:

    """
    Decompresses the file
    """
    #open the compressed file and create huffman tree and decode the file

    with open(filename, 'rb') as f:
        f_dict = eval(f.readline())
        msg_len = int(f.readline())
        compressed_text = f.read()
        tree = build_tree(f_dict)
        codes = {}
        get_codes_from_tree(tree, '', codes)
        compressed = str(bin(int(compressed_text.hex(), 16))).replace('0b', '')
        decompressed = decode(codes, compressed)
        with open(output, 'w') as f:
            f.write(decompressed)


if __name__ == "__main__":

    #parse the arguments
    parser = argparse.ArgumentParser(description="KMPress for compressing files")
    parser.add_argument('file', type=str, help="File to Compress")
    parser.add_argument('-d','--decompress', dest='decompress', action='store_true', help="Decompress File")
    parser.add_argument('-c','--compress', dest='compress', action='store_true', help="Compress File")
    parser.add_argument('output', type=str, help="Output File")

    args = parser.parse_args()
    if not args.file:
        parser.print_help()
        exit(1)

    filename = args.file
    #check if file exists and for what operation
    if not os.path.isfile(filename):
        print("File does not exist")
        exit(1)

    if args.decompress and args.compress:
        print("Choose either compress or decompress")
        exit(1)
    
    if not args.output:
        print("Please specify output file")
        exit(1)

    if args.decompress:
        decompress(args.file, args.output)
    else:
        compress(args.file, args.output)