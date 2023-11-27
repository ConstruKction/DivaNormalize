from arg_parser import ArgParser
from audio_processor import AudioProcessor


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    audio_processor = AudioProcessor(args.input)
    audio_processor.find_oggs()
    audio_processor.process_oggs(args.lufs, args.true_peak, args.loudness_range, args.sample_rate)


if __name__ == '__main__':
    main()
