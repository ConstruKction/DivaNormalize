from arg_parser import ArgParser
from normalizer import Normalizer


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    normalizer = Normalizer(args.input, args.two_pass)
    normalizer.normalize_songs(args.lufs, args.true_peak, args.loudness_range, args.sample_rate)


if __name__ == '__main__':
    main()
