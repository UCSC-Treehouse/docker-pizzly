#!/usr/bin/env python2.7
import argparse
import subprocess

def get_insert_size(abundance):
    cmd = ['python',
           '/opt/pizzly-0.37.3/scripts/get_fragment_length.py',
           abundance]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    return int(stdout.strip())

def run_pizzly(fusion, insert_size):
    cmd = ['pizzly',
           '-k', 31,
           '--gtf', '/opt/pipeline/data/gencode.v23.annotation.gtf.gz',
           '--cache', '/opt/pipeline/data/index.cache.txt',
           '--align-score', 2,
           '--insert-size', insert_size,
           '--fasta', '/opt/pipeline/data/gencode.v23.transcripts.fixed.fa.gz',
           '--output', 'OUTPUT',
           fusion]

    subprocess.check_call([str(x) for x in cmd])

    cmd = ['python',
          '/opt/pizzly-0.37.3/scripts/flatten_json.py',
           'OUTPUT.json']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()

    with open('pizzly-fusion.final', 'w') as f:
        f.write(stdout)


def main():
    parser = argparse.ArgumentParser(description=main.__doc__)

    parser.add_argument('-f', '--fusion',
                        help='Kallisto fusion.txt file',
                        required=True)

    parser.add_argument('-a', '--abundance',
                        help='Kallisto abundance.h5 file',
                        required=False)

    parser.add_argument('-i', '--insert-size',
                        help='Insert size. Default is 400.',
                        dest='insert_size',
                        default=400)

    args = parser.parse_args()

    insert_size = args.insert_size
    if args.abundance:
        print 'WARNING: Inferring insert size from abundance file!'
        insert_size = get_insert_size(args.abundance)

    run_pizzly(args.fusion, insert_size)


if __name__ == '__main__':
    main()