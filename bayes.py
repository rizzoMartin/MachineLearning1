from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
from nltk import word_tokenize

def bayes(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123, stratify=y)

    print('training data...')
    # Train
    bayes = MultinomialNB().fit(X_train, y_train)

    print('making predictions...')
    y_predicted = bayes.predict(X_test)
    
    print('performance metrics:')
    print('Accuracy score test set: ', accuracy_score(y_test, y_predicted))
    print('Confusion matrix test set: \n', confusion_matrix(y_test, y_predicted)/len(y_test))

def vectorize_tfidf(df):
    print('applying tfidf vectorizer')
    # Define the vectorizer and specify the arguments
    my_pattern = r'\b[^\d\W][^\d\W]+\b'
    vect = TfidfVectorizer(ngram_range=(1,2), max_features=100, token_pattern=my_pattern, stop_words=ENGLISH_STOP_WORDS).fit(df.review)

    # Transform the vectorizer
    X_txt = vect.transform(df.review)
    
    # Transform to a data frame and specify the column names
    X=pd.DataFrame(X_txt.toarray(), columns=vect.get_feature_names())
    y= df.label
    bayes(X, y)

def bd_call():
    engine = create_engine('mysql+mysqlconnector://root:root@localhost/hotel_reviews')
    procedure = 'select_all'

    print('getting data from db...')
    raw_conn = engine.raw_connection()
    cur = raw_conn.cursor()
    cur.callproc(procedure)
    for result in cur.stored_results():
        df = DataFrame(result.fetchall())
    column_names_list = [i[0] for i in result.description]
    raw_conn.close()

    df.columns = column_names_list

    return df

def stemming(df):

    # STEMMING NOW
    porter = PorterStemmer()

    print('creating a list of tokens...')
    # Create a list of tokens
    tokens = [word_tokenize(review) for review in df.review] 

    print('stemming the list...')
    # Stem the list of tokens
    stemmed_tokens = [[porter.stem(word) for word in token] for token in tokens]

    print('joining the words...')
    # Print the first item of the stemmed tokenss
    columns_ready = [' '.join(stemmed) for stemmed in stemmed_tokens]

    df.review = columns_ready

    vectorize_tfidf(df)

df = bd_call()
vectorize_tfidf(df)
stemming(df)