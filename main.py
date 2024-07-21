from arg_parser import ArgParser
from normalizer import Normalizer


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    normalizer = Normalizer(args.input)
    normalizer.normalize_songs(args.target_level, args.sample_rate)


if __name__ == '__main__':
    main()
