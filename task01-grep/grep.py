#!/usr/bin/env python3
import sys
import re
import argparse


def main(args_str):
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str, )
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    args = parser.parse_args(args_str)
    if not args.files:
        from_terminal(args)
    else:
        from_file(args)


def from_terminal(args):
    k = 0
    for line in sys.stdin.readlines():
        line = line.rstrip('\n')
        if args.regex:
            if re.search(args.needle, line):
                k = k + 1
                if not args.count:
                    print(line)
        else:
            if line.find(args.needle) != -1:
                k = k + 1
                if not args.count:
                    print(line)
    if args.count:
        print(k)
        k = 0


def from_file(args):
    k = 0
    for files in args.files:
        with open(files, 'r') as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                if args.regex:
                    if re.search(args.needle, line):
                        k = k + 1
                        if not args.count:
                            if len(args.files) != 1:
                                print(files, ':', line, sep='')
                            else:
                                print(line)
                else:
                    if line.find(args.needle) != -1:
                        k = k + 1
                        if not args.count:
                            if len(args.files) != 1:
                                print(files, ':', line, sep='')
                            else:
                                print(line)
        if args.count:
            if len(args.files) != 1:
                print(files, ':', k, sep='')
            else:
                print(k)
            k = 0


if __name__ == '__main__':
    main(sys.argv[1:])
    
