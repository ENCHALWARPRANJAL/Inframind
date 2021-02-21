from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
sentence="Very nice product"
class vaderSentiment:
    def sentiment_analyzer_scores(self,sentence):
        score = analyser.polarity_scores(sentence)
        return score
      