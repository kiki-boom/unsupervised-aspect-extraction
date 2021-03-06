import codecs
import logging
import argparse
import jieba

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", type=str,
                    help="input file path", required=True)
parser.add_argument("-o", "--output_dir", type=str,
                    default="../preprocessed_data", help="output dir path")
parser.add_argument("--stop_words", type=str,
                    help="stop words file path")
args = parser.parse_args()


def parse_sentence(line, stop=None):
    text_token = jieba.lcut(line)
    if stop is not None:
        text_token = [i for i in text_token if i not in stop]
    return text_token


def preprocess_train():
    stop_words = None
    if args.stop_words:
        stop_words = [word.strip() for word in open(args.stop_words)]

    f = codecs.open(args.input_file, 'r', 'utf-8')
    out = codecs.open(args.output_dir + '/train.txt', 'w', 'utf-8')

    for line in f:
        tokens = parse_sentence(line.strip(), stop_words)
        if len(tokens) > 0:
            out.write(' '.join(tokens)+'\n')


if __name__ == "__main__":
    logger('Preprocessing raw review sentences ...')
    preprocess_train()
