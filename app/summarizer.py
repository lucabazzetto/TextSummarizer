# Import required libraries
import re # Regular expressions for text processing
import nltk # Natural Language Toolkit for NLP tasks
import numpy as np # Numerical computing library
from sklearn.feature_extraction.text import TfidfVectorizer # TF-IDF implementation
from sklearn.metrics.pairwise import cosine_similarity # Similarity calculation

class TextSummarizer:
    def __init__(self):
        """Initialize the summarizer and download required NLTK resources"""
        self._download_nltk_resources()

    def _download_nltk_resources(self):
        """Download necessary NLTK datasets"""
        nltk.download('punkt', quiet=True, raise_on_error=True) # Sentence tokenizer data
        nltk.download('stopwords', quiet=True) # Common English stopwords

    def summarize(self, text, ratio=0.5):
        """
        Main method to generate summary
        Args:
            text: Input text to summarize
            ratio: Proportion of original text to keep (default: 0.5)
        Returns:
            str: Generated summary
        """
        sentences = self._split_sentences(text) # Split text into sentences
        tfidf_matrix = self._create_tfidf_matrix(sentences)  # Create TF-IDF matrix
        sentence_scores = self._calculate_sentence_scores(tfidf_matrix) # Score sentences
        return self._build_summary(sentences, sentence_scores, ratio) # Build final summary

    def _split_sentences(self, text):
        """
        Split text into sentences using regex
        Args:
            text: Input text string
        Returns:
            list: Cleaned list of sentences
        """
        sentences = re.findall(r'[^.!?]+[.!?]', text) # Split on .!? punctuation
        return [s.strip() for s in sentences if s.strip()] # Clean whitespace and empty strings

    def _create_tfidf_matrix(self, sentences):
        """
        Create TF-IDF matrix from sentences
        Args:
            sentences: List of sentences
        Returns:
            sparse matrix: TF-IDF weighted document-term matrix
        """
        stop_words = nltk.corpus.stopwords.words('english') # Get English stopwords
        vectorizer = TfidfVectorizer(stop_words=stop_words) # Initialize vectorizer
        return vectorizer.fit_transform(sentences) # Transform text to TF-IDF features

    def _calculate_sentence_scores(self, tfidf_matrix):
        """
        Calculate sentence importance scores using cosine similarity
        Args:
            tfidf_matrix: TF-IDF matrix from vectorizer
        Returns:
            ndarray: Array of sentence scores
        """
        doc_vector = np.asarray(tfidf_matrix.mean(axis=0)) # Document mean vector
        return cosine_similarity(tfidf_matrix, doc_vector).flatten() # Similarity scores

    def _build_summary(self, sentences, scores, ratio):
        """
        Compile final summary from top sentences
        Args:
            sentences: Original sentence list
            scores: Calculated importance scores
            ratio: Summary length ratio
        Returns:
            str: Joined summary text
        """
        n = max(1, int(len(sentences) * ratio)) # Calculate number of sentences to keep
        top_indices = scores.argsort()[-n:][::-1] # Get indices of top N scores
        return ' '.join([sentences[i] for i in sorted(top_indices)]) # Return sentences in original order, joined with spaces