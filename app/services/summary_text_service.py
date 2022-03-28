import numpy as np
import networkx as nx
import logging

from typing import List

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance

from app.schemas.document import DocumentBase
from app.services.db.document_repo import DocumentRepository
from config import system_config


logger = logging.getLogger(__name__)


class SummaryTextService:

    def __init__(self, doc_repo: DocumentRepository):
        self.doc_repo = doc_repo
        self.max_sentences = system_config.max_sentences

    async def create_document(self, text: str) -> DocumentBase:
        summary = self.generate_summary(text=text)
        document = await self.doc_repo.add(summary=summary)
        return document

    def generate_summary(self, text) -> str:
        stop_words = stopwords.words('english')

        # Step 1 - Read text anc split it
        sentences = self.read_text(text=text)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        logger.info(f"Indexes of top ranked_sentence order are: {ranked_sentence}")

        summarize_text = [" ".join(ranked_sentence[i][1]) for i in range(self.max_sentences)]

        # Step 5 - Ofcourse, output the summarization text
        return ". ".join(summarize_text)

    def build_similarity_matrix(self, sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix

    @staticmethod
    def read_text(text: str) -> List[List[str]]:
        sentences = [sentence.replace("[^a-zA-Z]", " ").split(" ") for sentence in text.split(". ")]
        return sentences

    @staticmethod
    def sentence_similarity(sent1, sent2, stop_words=None):
        if not stop_words:
            stop_words = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in stop_words:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in stop_words:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)

