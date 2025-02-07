#%% md
# # Importing libraries
#%%
import os
import sys

import optuna
import pandas as pd
from bertopic import BERTopic
from git_root import git_root
from hdbscan import HDBSCAN
from octis.evaluation_metrics.coherence_metrics import Coherence
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from optuna.samplers import TPESampler
from sentence_transformers import SentenceTransformer
from umap import UMAP

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
#documents = [document.lower() for document in documents]
#%%
def keep_text_only(text):
    return re.sub(r'[^A-Za-z ]', '', text)

#documents = [keep_text_only(document) for document in documents]
#%%
print(len(documents))
#%% md
# # Topic Modelling
#%%
embedding_model = SentenceTransformer('thenlper/gte-small', trust_remote_code=True)

embeddings = embedding_model.encode(documents)
#%%
def objective(trial):
    umap_parameters = {
        'n_neighbors': trial.suggest_int('n_neighbors', 2, 100),
        'n_components': 5,
        'min_dist': trial.suggest_float('min_dist', 0.1, 1),
        'metric': 'cosine',
        'random_state': 42
    }

    umap_model = UMAP(**umap_parameters)

    hdbscan_parameters = {
        'min_cluster_size': trial.suggest_int('min_cluster_size', 5, 100),
        'min_samples': trial.suggest_int('min_samples', 5, 100),
    }

    hdbscan_model = HDBSCAN(**hdbscan_parameters)

    bertopic_parameters = {
        'top_n_words': 25,
        'n_gram_range': (2, 5),
        'umap_model': umap_model,
        'hdbscan_model': hdbscan_model
    }

    topic_model = BERTopic(**bertopic_parameters)
    topics, probs = topic_model.fit_transform(documents, embeddings)

    def remove_empty_topics(topic_words, top_n_words):
        result = []
        for words in topic_words:
            if words != ['']*top_n_words:
                result.append(words)
        return result

    documents_df = pd.DataFrame({"Document": documents,
                            "ID": range(len(documents)),
                            "Topic": topics})
    documents_per_topic = documents_df.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
    cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)

    # Extract vectorizer and analyzer from BERTopic
    vectorizer = topic_model.vectorizer_model
    analyzer = vectorizer.build_analyzer()

    # Extract features for Topic Coherence evaluation
    words = vectorizer.get_feature_names_out()
    tokens = [analyzer(doc) for doc in cleaned_docs]

    topics_dict = topic_model.get_topics()
    topic_words = [[word for word, _ in words] for words in topics_dict.values()]
    topic_term_matrix = topic_model.c_tf_idf_.toarray()

    remove_empty_topics(topic_words, 25)
    num_topics = len(topic_words)
    trial.set_user_attr('num_topics', num_topics)
    print(num_topics)

    octis_topics = {'topics': topic_words, 'topic-document-matrix': topic_term_matrix}

    coherence = Coherence(texts = tokens, measure='c_npmi')
    diversity = TopicDiversity(topk=25)

    if num_topics < 10:
        raise optuna.TrialPruned()
    elif num_topics > 50:
        raise optuna.TrialPruned()

    diversity_score = diversity.score(octis_topics)
    coherence_score = coherence.score(octis_topics)

    return coherence_score, diversity_score
#%%
sampler = TPESampler(seed=42, constant_liar=True)
storage_url = f"sqlite:////{my_git_root}/topic_model_studies.db"
study = optuna.create_study(directions=['maximize', 'maximize'], sampler=sampler, study_name='bertopic_double_optimization_v1', storage=storage_url, load_if_exists=True)
study.optimize(objective, n_trials=1000000, catch=(IndexError,))