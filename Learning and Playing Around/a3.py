#Following Example from online to learn about naive bayes
#Conclusion could not get to work following example and not applicable enough to my project

import string
import math
# Read in a file.
def create_vocab(file):
    # Open specified file and words state array.
    opened_file = open(file, 'r')
    words = []

    # Iterate through the file.
    for line in opened_file:
        if line is not None:
            # Append the values split on the ' ' value.
            # Strip all punctuation, \n and \t's.
            line = line.translate(str.maketrans('','', string.punctuation))
            line = line.strip()
            line = line.replace('\t', '')
            line = line.lower()
            words.append(line.split(' '))

    parse_other = []

    # Put them into one array, removing blank spaces and the labels.
    for i in range(len(words)):
        for j in range(len(words[i])):
            if(words[i][j] != '' and words[i][j] != '1' and words[i][j] != '0'):
                parse_other.append(words[i][j])


    # Alphabetize the words.
    parse_other = sorted(list(set(parse_other)))
    parse_other.append('classlabel')

    # Return the vocab array.
    return parse_other;

def preprocessing(file, vocab):
    opened_file = open(file, 'r')
    indi_words = []
    class_label = []
    pre_array = []
    
    # Create indi_words array, splitting on spaces.
    for line in opened_file:
        if line is not None:
            line = line.translate(str.maketrans('','', string.punctuation))
            line = line.lower()
            line = line.strip('\n')
            indi_words.append(line.split(' '))

    # Pull out individual class labels.
    for i in range(len(indi_words)):
        for j in range(len(indi_words[i])):
            if(indi_words[i][j] == '\t'):
                class_label.append(indi_words[i][j+1])

    # Create the preprocessing array.
    for i in range(len(indi_words)):
        process_array = []
        for j in range(len(vocab)-1):
            if vocab[j] in indi_words[i]:
                process_array.append(1)
            else:
                process_array.append(0)
        pre_array.append(process_array)

    # Attach the class label.
    for i in range(len(class_label)):
        pre_array[i].append(int(class_label[i]))

    return pre_array, class_label

def preproc_print(vocab, preproc, file):
    f = open(file, 'w')
    
    for i in vocab:
        f.write(i + ',')

    for i in range(len(preproc)):
        f.write('\n')
        for j in range(len(preproc[i])):
            if(j != len(preproc[i])-1):
                f.write(str(preproc[i][j]) + ',')
            else:
                 f.write(str(preproc[i][j]))

    f.close()

def split_features(features, labels):
    pos_counter = 0
    neg_counter = 0
    pos_array = []
    neg_array = []

    for i in range(len(labels)):
        if (int(labels[i]) == 1):
            pos_counter += 1
            pos_array.append(features[i])
        elif(int(labels[i]) == 0):
            neg_counter += 1
            neg_array.append(features[i])

    return pos_counter, neg_counter, pos_array, neg_array

def prob_word(counter, word, train_array, value, train_vocab):
    num_exists = 0
    location = 0

    if word in train_vocab:
        location = train_vocab.index(word)

        for i in range(len(train_array)-1):
            if (value == train_array[i][location]):
                num_exists += 1

        total_val = float(num_exists+1) / float(counter+2)
    else:
        total_val = 0

    if(total_val == 0):
            total_val = 0.5

    return total_val

def calc_total_prob(counter, test_array, train_array, labels, train_vocab, test_vocab):
    sum_val = 0

    for i in range(len(test_array)-1):
        word = test_vocab[i]
        sum_val += math.log(prob_word(counter, word, train_array, test_array[i], train_vocab))

    label_prob = prob_label(counter, labels)

    sum_val += math.log(label_prob)

    return sum_val

def prob_label(counter, labels):
    return float(counter) / float(len(labels))

def main():
    results_array_train = []
    result_array_test = []
    some_val_train = 0
    some_val_test = 0
    result_val_train = 0
    result_val_test = 0

    train_vocab = create_vocab(train_set)
    test_vocab = create_vocab(test_set)

    train_features, train_labels_array = preprocessing(train_set, train_vocab)
    test_features, test_labels_array = preprocessing(test_set, test_vocab)

    preproc_print(train_vocab, train_features, preproc_train)
    preproc_print(test_vocab, test_features, preproc_test)

    pos_counter, neg_counter, pos_array, neg_array = split_features(train_features, train_labels_array)

    
    for i in range(len(train_features)-1):
        pos_probability = calc_total_prob(pos_counter, train_features[i], pos_array, train_labels_array, train_vocab, train_vocab)
        neg_probability = calc_total_prob(neg_counter, train_features[i], neg_array, train_labels_array, train_vocab, train_vocab)

        if(pos_probability > neg_probability):
            results_array_train.append(1)
        else:
            results_array_train.append(0)

    total_value_train = len(train_labels_array)

    if(len(results_array_train) == len(train_labels_array)-1):
        for i in range(len(results_array_train)):
            if(int(results_array_train[i]) == int(train_labels_array[i])):
                some_val_train += 1

        result_val_train = float(some_val_train) / float(total_value_train)

        #print("Accuracy: " + str(result_val_train))
    else:
        print("Something went wrong.")


    for i in range(len(test_features)-1):
        pos_probability = calc_total_prob(pos_counter, test_features[i], pos_array, train_labels_array, train_vocab, test_vocab)
        neg_probability = calc_total_prob(neg_counter, test_features[i], neg_array, train_labels_array, train_vocab, test_vocab)

        if(pos_probability > neg_probability):
            result_array_test.append(1)
        else:
            result_array_test.append(0)


    total_value_test = len(test_labels_array)

    if(len(result_array_test) == len(test_labels_array)-1):
        for i in range(len(result_array_test)):
            if(int(result_array_test[i]) == int(test_labels_array[i])):
                some_val_test += 1

        result_val_test = float(some_val_test) / float(total_value_test)

        #print("Accuracy: " + str(result_val_test))
    else:
        print("Something went wrong.")


    f = open(output_file_name, 'w')
    f.write("Training on trainingSet.txt and testing on trainingSet.txt.\n ")
    f.write("ACCURACY: " + str(result_val_train*100) + "%\n ")

    f.write("Training on trainingSet.txt and testing on testSet.txt.\n ")
    f.write("ACCURACY: " + str(result_val_test*100) + "%\n")

    f.close()

main()