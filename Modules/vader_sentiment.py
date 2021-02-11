from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
sentence="Very nice product"
class vaderSentiment:
    def sentiment_analyzer_scores(self,sentence):
        score = analyser.polarity_scores(sentence)
        return score
        #print("{:-<40} {}".format(sentence, str(score)))
#def main():
  #  obj=vaderSentiment() 
   # obj.sentiment_analyzer_scores(sentence)
#if __name__=="__main__":
  #  main()