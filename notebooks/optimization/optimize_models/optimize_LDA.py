#%% md
# # # Importing libraries
#%%

import os
import sys

import optuna
import pandas as pd
import sklearn
from git_root import git_root
from octis.evaluation_metrics.coherence_metrics import Coherence
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from optuna.samplers import TPESampler
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

print(sklearn.__version__)

sklearn.set_config(skip_parameter_validation=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
my_git_root = git_root()
sys.path.append(my_git_root)
from src import *
#%% md
# # Loading the data
#%%
df_chunked_path = f'{my_git_root}/final_notebooks/data/chunked_documents_final.csv'
df_chunked = pd.read_csv(df_chunked_path)
#%%
df_chunked
#%%
documents = df_chunked['text'].to_list()
documents = [document.lower() for document in documents]
#%%
def keep_text_only(text):
    return re.sub(r'[^A-Za-z ]', '', text)

documents = [keep_text_only(document) for document in documents]
#%%
vectorizer = CountVectorizer(ngram_range=(2, 5))
doc_term_matrix = vectorizer.fit_transform(documents)
#%% md
# # Optimization
#%%
def objective(trial):

    lda_parameters = {
        'n_components': trial.suggest_int('n_components', 10, 50),
        'doc_topic_prior': trial.suggest_float('doc_topic_prior', 0.1, 10),
        'topic_word_prior': trial.suggest_float('topic_word_prior', 0.1, 10),
        'learning_method': 'online',
        'random_state': 42,
    }

    lda = LatentDirichletAllocation(**lda_parameters)  # n_components = number of topics
    lda = lda.fit(doc_term_matrix)

    topic_document_matrix = lda.transform(doc_term_matrix)
    topic_word_matrix = lda.components_
    vocabulary = vectorizer.get_feature_names_out()

    n_top_words = 25
    topic_descriptors = []
    for topic_idx, topic_weights in enumerate(topic_word_matrix):
        # Get indices of the top n words for this topic
        top_word_indices = topic_weights.argsort()[-n_top_words:][::-1]
        # Map indices to tokens
        top_words = [vocabulary[i] for i in top_word_indices]
        topic_descriptors.append(top_words)


    octis_topics = {
        'topics': topic_descriptors,
        'topic-document-matrix': topic_document_matrix,
    }

    # Tokenize the documents into n-grams
    tokenized_documents = vectorizer.inverse_transform(doc_term_matrix)

    coherence = Coherence(texts = tokenized_documents, measure='c_npmi')
    diversity = TopicDiversity(topk=25)

    coherence_score = coherence.score(octis_topics)
    diversity_score = diversity.score(octis_topics)

    return coherence_score, diversity_score
#%%
sampler = TPESampler(seed=42, constant_liar=True)
storage_url = f"sqlite:////{my_git_root}/topic_model_studies.db"
study = optuna.create_study(directions=['maximize', 'maximize'], sampler=sampler, study_name='LDA_double_optimization_v1', storage=storage_url, load_if_exists=True)
study.optimize(objective, n_trials=1000000, catch=(IndexError,), n_jobs=3)