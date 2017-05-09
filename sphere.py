#!/usr/bin/python

import sys
import logging
import argparse

logger = logging.getLogger(__name__)

materials = '''MATERIAL "White" rgb 1.0000 1.0000 1.0000  amb 0.2000 0.2000 0.2000  emis 1.0000 1.0000 1.0000  spec 0.5000 0.5000 0.5000  shi 10 trans 0.0000
MATERIAL "Black" rgb 0.0000 0.0000 0.0000  amb 0.2000 0.2000 0.2000  emis 0.0000 0.0000 0.0000  spec 0.5000 0.5000 0.5000  shi 10 trans 0.0000
'''

def parse_cmdline():
    parser = argparse.ArgumentParser(description='''
        This script will replace the materials in an AC3D file to contain a black and white chessboard pattern.'''
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")
    parser.add_argument('infile', help="Input AC3D file")
    parser.add_argument('outfile', help="Output AC3D file")
    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args


def main():
    global materials
    args = parse_cmdline()

    with open(args.infile) as f:
        with open(args.outfile, 'w') as of:
            faces = []
            state = 0 # 1 means inside SURFace node, 0 means everything else
            poly = { 'mat': '', 'refs': 0, 'vertices': [] }
            for l in f:
                if 'MATERIAL' in l:
                    of.write(materials)
                    materials = '' # really dodgy way of making sure this is only printed once
                    continue
                if 'OBJECT' in l:
                    state = 0
                    faces = []
                if 'SURF ' in l or 'kids' in l:
                    state = 1
                    if poly['refs']: # we've processed a SURFace previously
                        for f in faces:
                            # Find number of common vertices between surfaces
                            intersect = len(set(poly['vertices']) & set(f['vertices']))
                            if intersect > 2: # A chessboard-compatible object should not have two faces with more than two common vertices
                                logger.error("3D Object is incompatible because it has faces that share more than one line. Common vertices: %s", intersect)
                                exit(1)
                            elif intersect == 2: # two common vertices, these are neighbours and should have different colours
                                logger.debug('neighbour found')
                                if f['mat'] == poly['mat']:
                                    logger.debug('material swapped')
                                    poly['mat'] = int(not f['mat'])
                                logger.debug(f)
                                logger.debug(poly)
                            elif intersect == 1: # one common vertex, these are joined at one corner and should have the same colour
                                logger.debug('opposite found')
                                if f['mat'] != poly['mat']:
                                    logger.debug('material swapped')
                                    poly['mat'] == f['mat']
                                logger.debug(f)
                                logger.debug(poly)
                        # Write out SURFace node
                        of.write("SURF 0X10\n")
                        of.write("mat {0}\n".format(poly['mat']))
                        of.write("refs {0}\n".format(poly['refs']))
                        for v in poly['vertices']:
                            of.write("{0} 0 0\n".format(v))
                        faces.append(poly) # save for comparison later
                    poly = { 'mat': '', 'refs': 0, 'vertices': [] } # wipe out SURFace data that was written
                    if 'kids' in l: # this seems to indicate the end of an OBJECT node
                        state = 0
                if state == 0: # non-SURF mode
                    of.write(l)
                elif state == 1: # SURF mode
                    t = l.split() # Tokenise line
                    if t[0] == 'mat': poly['mat'] = int(t[1])
                    elif t[0] == 'refs': poly['refs'] = int(t[1])
                    elif t[0] == 'SURF': continue
                    else: poly['vertices'].append(int(t[0]))

    sys.exit(0)


# call main()
if __name__ == '__main__':
    main()
