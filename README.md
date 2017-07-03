# wikimedia_detox
Simple text classification application based on the [wikipedia detox research](https://meta.wikimedia.org/wiki/Research:Detox/Data_Release).
## How to run
In order to run the app, please download the following files to your local data directory:
 
* [aggression_annotations.tsv](https://ndownloader.figshare.com/files/7394506)
* [attack_annotated_comments.tsv](https://ndownloader.figshare.com/files/7554634)
* [attack_annotations.tsv](https://ndownloader.figshare.com/files/7554637)
* [toxicity_annotations.tsv](https://ndownloader.figshare.com/files/7394539)
 
Assign the path to your data directory to the “local_path_dir” variable at the top of [preprocessing.py](https://github.com/pejmanes/wikimedia_detox/blob/master/preprocessing/preprocessing.py). 

Python3.6 [run.py](https://github.com/pejmanes/wikimedia_detox/blob/master/run.py) will start the application.  
 
This application was built using Python 3.6 and PyQt 5. 

Please refer to [requirement.txt](https://github.com/pejmanes/wikimedia_detox/blob/master/requirements.txt) for dependencies.

### Preprocessing
The score for each comment with regards to the three categories (attack, aggression, and toxicity) is calculated by majority vote, for instance if more than half of the crowdworkers considered the comment to be aggressive, then that comment is labeled aggressive.
The resulting three columns are joined to the comments data to allow for classification based on either label.
 
### Cross-validation
In order to understand how the classifier can generalise, cross-validation is used. The number of folds is given by the user (allowed value is an integer between 2 and 10). The entire data set is used in this process. Depending on the number of cv folds specified, data is split into train and test sets where a classifier is trained on the train set and tested on the test set, making sure all the data is used for training and testing. The average accuracy of the classifier and the 95% confidence interval is then reported along with time taken to complete the task.
 
### Training
After the user is satisfied with the accuracy of the classification based on the input parameters, the model needs to be trained to be able to predict. 
 
### Prediction
After a model has been trained, the “input” text-box can be used to type or paste text, in order to predict its quality in terms of “offensive language” or “not offensive”.
 
### Classifiers
[LogisticRegression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) and [LinearSVC](http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html) are implemented from the Scikit-learn library. LinearSVC yields slightly higher accuracy.
 
### Analyzer
Three options are word, character, and character_wb which is a variation of character based feature extraction where word boundaries are taken into consideration. Due to misspellings and the nature of the language on social media, word-based feature extraction yields inferior results as opposed to character-based feature extraction, and taking word boundaries into account improves the accuracy.
 
### Max features
This parameter limits the number of features. As the number of documents grow, the size of the unique vocabulary (extracted tokens, or character n-grams) grows immensely and could easily get to hundreds of thousands of features, making the process of training a classifier extremely slow. Although the more features are extracted the higher the accuracy tends to be (accepted values: 100 to 100,000).
 
### Ngrams
The minimum and maximum number of ngrams to consider when training a classifier. By increasing the max ngram parameter, the context of the token or character is taken into account. This increases the accuracy while also increasing the cost to train.
