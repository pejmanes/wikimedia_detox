# coding: utf-8

import pandas as pd
import os

local_data_path = "/Users/Pejman/PycharmProjects/wikimedia_detox/data/"

comments_path = os.path.join(local_data_path, "attack_annotated_comments.tsv")
attack_annotations_path = os.path.join(local_data_path, "attack_annotations.tsv")
aggression_annotations_path = os.path.join(local_data_path, "aggression_annotations.tsv")
toxicity_annotations_path = os.path.join(local_data_path, "toxicity_annotations.tsv")


def read_csv(in_file):
    f = open(in_file, 'rb')
    df = pd.read_csv(f, delimiter='\t')
    return df


def get_df():
    """read csv files and add columns for attack, toxicity, adn aggression then output data frame"""
    comments_df = read_csv(comments_path)
    attack_df = read_csv(attack_annotations_path)
    aggression_df = read_csv(aggression_annotations_path)
    toxicity_df = read_csv(toxicity_annotations_path)

    # labels a comment as toxic based on majority vote, creates toxicity labels as data frame
    toxicity_labels = pd.DataFrame({'toxicity': toxicity_df.groupby('rev_id')['toxicity'].mean() > 0.5})\
        .reset_index()
    # toxicity labels data frame is joined back to the comments data frame
    comments_df = pd.merge(comments_df, toxicity_labels, on='rev_id')

    # labels a comment as aggressive based on majority vote, creates aggression labels as data frame
    aggression_labels = pd.DataFrame({'aggression': aggression_df.groupby('rev_id')['aggression'].mean() > 0.5})\
        .reset_index()
    # aggression labels data frame is joined back to the comments data frame
    comments_df = pd.merge(comments_df, aggression_labels, on='rev_id')

    # labels a comment as an attack based on majority vote, creates attack labels as data frame
    attack_labels = pd.DataFrame({'attack': attack_df.groupby('rev_id')['attack'].mean() > 0.5})\
        .reset_index()
    # attack labels data frame is joined back to the comments data frame
    comments_df = pd.merge(comments_df, attack_labels, on='rev_id')

    # removing new line and tab character place holders
    comments_df['comment'] = comments_df['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", " "))
    comments_df['comment'] = comments_df['comment'].apply(lambda x: x.replace("TAB_TOKEN", " "))
    return comments_df


def extract_harm_comments():
    """extract all the comments that have been marked (majority vote) as either
    aggressive, toxic or attack; for term extraction"""
    harmful_comments_path = "/Users/Pejman/PycharmProjects/wikimedia_detox/data/harm_comments.txt"
    df = get_df()
    # due to large size and limitations of third party term extractor,
    # not all comments can be used for term extraction
    df = df.query('attack and toxicity and aggression')
    df = df.sample(frac=0.5)

    f = open(harmful_comments_path, 'w')
    for _, row in df.iterrows():
        f.write(row.comment)
        f.write('\n')
    f.close()
