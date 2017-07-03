# wikimedia_detox
Simple text classification application based on the [wikipedia detox research](https://meta.wikimedia.org/wiki/Research:Detox/Data_Release)
## How to run
In order to run the app, please download the following files to your local data directory:
 
* [aggression_annotations.tsv](https://ndownloader.figshare.com/files/7394506)
* [attack_annotated_comments.tsv](https://ndownloader.figshare.com/files/7554634)
* [attack_annotations.tsv](https://ndownloader.figshare.com/files/7554637)
* [toxicity_annotations.tsv](https://ndownloader.figshare.com/files/7394539)
 
Assign the path to your data directory to the “local_path_dir” variable at the top of [preprocessing.py](https://github.com/pejmanes/wikimedia_detox/blob/master/preprocessing/preprocessing.py). 

Python3.6 [run](https://github.com/pejmanes/wikimedia_detox/blob/master/run.py) will start the application.  
 
This application was built using Python 3.6 and PyQt 5. 

Please refer to [requirement.txt](https://github.com/pejmanes/wikimedia_detox/blob/master/requirements.txt) for dependencies.
