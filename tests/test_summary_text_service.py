import numpy as np

from nltk.corpus import stopwords


def test_read_text(summary_text_service):
    text = "I just returned from the greatest summer vacation. It was so fantastic, I never wanted it to end."
    result = summary_text_service.read_text(text)
    assert result == [['I', 'just', 'returned', 'from', 'the', 'greatest', 'summer', 'vacation'],
                      ['It', 'was', 'so', 'fantastic,', 'I', 'never', 'wanted', 'it', 'to', 'end.']]


def test_build_similarity_matrix(summary_text_service):
    text = "I just returned from the greatest summer vacation. It was so fantastic, I never wanted it to end."
    stop_words = stopwords.words('english')
    sentences = summary_text_service.read_text(text)
    result = summary_text_service.build_similarity_matrix(sentences=sentences,
                                                          stop_words=stop_words)
    assert np.array_equal(result, np.zeros((2, 2)))


def test_generate_summary(summary_text_service):
    text = (
        "I just returned from the greatest summer vacation. "
        "It was so fantastic, I never wanted it to end. "
        "I spent eight days in Paris, France. "
        "My best friends, Henry and Steve, went with me. " 
        "We had a beautiful hotel room in the Latin Quarter, and it wasn’t even expensive. "
        "We had a balcony with a wonderful view. "
        "We visited many famous tourist places. My favorite was the Louvre, a well-known museum. "
        "I was always interested in art, so that was a special treat for me. " 
        "The museum is so huge, you could spend weeks there. " 
        "Henry got tired walking around the museum and said “Enough! I need to take a break and rest.” "
        "We took lots of breaks and sat in cafes along the river Seine. " 
        "The French food we ate was delicious. " 
        "The wines were tasty, too. Steve’s favorite part of the vacation was the hotel breakfast. " 
        "He said he would be happy if he could eat croissants like those forever. " 
        "We had so much fun that we’re already talking about our next vacation! "
    )
    result = summary_text_service.generate_summary(text=text, max_sentences=2)

    assert result == "Steve’s favorite part of the vacation was the hotel breakfast. " \
                     "My favorite was the Louvre, a well-known museum"
