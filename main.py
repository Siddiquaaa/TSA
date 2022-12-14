import streamlit as st
import tweepy 
from textblob import TextBlob
from textblob import Word
import pandas as pd
from wordcloud import WordCloud
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

tsafav = Image.open("tsaf.ico")
st.set_page_config(
     page_title="Twitter Sentiment Analysis",
     page_icon=tsafav,
	 layout = "wide")


#---------------------------------------------------------------------------

consumer_key = 'e8P53GlkhDJNtc8d9w1qb5oOb'
consumer_secret = 'fysNKDmd4k46cczfryOu5chh1nBCMSTsORHSVNAv4qJigvvnVF'

access_token = '1451182626165825538-YfvuMGo1whpq1dm7xxG1bRHM1ADQgA'
access_token_secret = 'g8MbdXpexp484RTar317BM4EZCCXER9Zzw7c7HyS5XE0l'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#-------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .main{
        background-color: #1d9bf0;
    }
	.sidebar .sidebar-content {
    background-color: white;
	}
    </style>
    """,
    unsafe_allow_html=True
)

def main():


	st.title("Twitter Sentiment Analysis")


	tasks=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Task",tasks)

	

	if choice=="Tweet Analyzer":


		raw_text = st.text_area("Enter the exact twitter handle of the Personality (without @)")

		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])


		if st.button("Analyze"):

			
			if Analyzer_choice == "Show Recent Tweets":

				st.success("Fetching last 5 Tweets")

				
				def Show_Recent_Tweets(raw_text):

					# Extract 100 tweets from the twitter user
					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:5]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			elif Analyzer_choice=="Generate WordCloud":

				st.success("Generating Word Cloud")

				def gen_wordcloud():

					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					# Create a dataframe with a column called Tweets
					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
					# word cloud visualization
					allWords = ' '.join([twts for twts in df['Tweets']])
					wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
					plt.imshow(wordCloud, interpolation="bilinear")
					plt.axis('off')
					plt.savefig('WC.jpg')
					img= Image.open("WC.jpg") 
					return img

				img=gen_wordcloud()

				st.image(img)



			else:



				
				def Plot_Analysis():

					st.success("Generating Visualisation for Sentiment Analysis")

					


					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

					
					# Create a function to clean the tweets
					def cleanTxt(text):
						text = re.sub('@[A-Za-z0???9]+', '', text) #Removing @mentions
						text = re.sub('#', '', text) # Removing '#' hash tag
						text = re.sub('RT[\s]+', '', text) # Removing RT
						text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
						text = Word(text)
						text.lemmatize() #lemmatization
						return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)

					# Create a function to get the subjectivity
					def getSubjectivity(text):
						return TextBlob(text).sentiment.subjectivity

					# Create a function to get the polarity
					def getPolarity(text):
						return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)

					def getAnalysis(score):
						if score < 0:
							return 'Negative'
						elif score == 0:
							return 'Neutral'
						else:
							return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()

				

	

	else:

	

		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")


		def get_data(user_name):

			posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")

			df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

			def cleanTxt(text):
				text = re.sub('@[A-Za-z0???9]+', '', text) #Removing @mentions
				text = re.sub('#', '', text) # Removing '#' hash tag
				text = re.sub('RT[\s]+', '', text) # Removing RT
				text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
				text = Word(text)
				text.lemmatize() #lemmatization
				return text

			# Clean the tweets
			df['Tweets'] = df['Tweets'].apply(cleanTxt)


			def getSubjectivity(text):
				return TextBlob(text).sentiment.subjectivity

						# Create a function to get the polarity
			def getPolarity(text):
				return TextBlob(text).sentiment.polarity


						# Create two new columns 'Subjectivity' & 'Polarity'
			df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
			df['Polarity'] = df['Tweets'].apply(getPolarity)

			def getAnalysis(score):
				if score < 0:
					return 'Negative'

				elif score == 0:
					return 'Neutral'


				else:
					return 'Positive'

		
						    
			df['Analysis'] = df['Polarity'].apply(getAnalysis)
			return df

		if st.button("Show Data"):

			st.success("Fetching Last 100 Tweets")

			df=get_data(user_name)

			st.write(df)





	st.caption('A collaborative work of UMAIMA SIDDIQUA and SYEDA FATIMA ALI')


if __name__ == "__main__":
	main()