import codecs
import re
import operator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

num_regex = re.compile('^[+-]?[0-9]+\.?[0-9]*$')


def is_number(token):
    return bool(num_regex.match(token))


def create_vocab(source, vocab_size=0, out_path=None):
    total_words, unique_words = 0, 0
    word_freqs = {}

    fin = codecs.open(source, 'r', 'utf-8')
    for line in fin:
        words = line.split()
        for w in words:
            if not is_number(w):
                try:
                    word_freqs[w] += 1
                except KeyError:
                    unique_words += 1
                    word_freqs[w] = 1
                total_words += 1

    logger.info('%i total words, %i unique words' % (total_words, unique_words))
    sorted_word_freqs = sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)

    vocab = {'<pad>': 0, '<unk>': 1, '<num>': 2}
    index = len(vocab)
    for word, _ in sorted_word_freqs:
        vocab[word] = index
        index += 1
        if vocab_size > 0 and index > vocab_size + 2:
            break

    # Write (vocab, frequence) to a txt file
    if out_path:
        vocab_file = codecs.open(out_path, mode='w', encoding='utf8')
        sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1))
        for word, index in sorted_vocab:
            vocab_file.write(word + '\t' + str(word_freqs.get(word, 0)) + '\n')
        vocab_file.close()

    return vocab


def load_vocab(file_path):
    vocab = {}
    index = 0
    fin = codecs.open(file_path, "r", "utf-8")
    for line in fin:
        item = line.strip().split("\t")
        if len(item) != 2:
            continue
        vocab[item[0]] = index
        index += 1
    return vocab


def read_dataset(source, vocab, max_seq_len=0):
    num_hit, unk_hit, total = 0., 0., 0.
    maxlen_x = 0
    data_x = []

    fin = codecs.open(source, 'r', 'utf-8')
    for line in fin:
        words = line.strip().split()
        if max_seq_len > 0 and len(words) > max_seq_len:
            continue

        indices = []
        for word in words:
            if is_number(word):
                indices.append(vocab['<num>'])
                num_hit += 1
            elif word in vocab:
                indices.append(vocab[word])
            else:
                indices.append(vocab['<unk>'])
                unk_hit += 1
            total += 1

        data_x.append(indices)
        if maxlen_x < len(indices):
            maxlen_x = len(indices)

    logger.info('<num> hit rate: %.2f%%, <unk> hit rate: %.2f%%' % (100 * num_hit / total, 100 * unk_hit / total))
    return data_x, maxlen_x

