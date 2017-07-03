# coding: utf-8


import sys
import os.path
import time

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QDialog
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from GUI.mainwidow import Ui_MainWindow
from classification import classify


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_maninWindow = Ui_MainWindow()
        self.ui_maninWindow.setupUi(self)
        self.show()
        self.initUI()
        self.clf = None

    def initUI(self):
        self.ui_maninWindow.trainButton.clicked.connect(self.trainButtonClicked)
        self.ui_maninWindow.predictButton.clicked.connect(self.predictButtonClicked)
        self.ui_maninWindow.clearButton.clicked.connect(self.clearButtonClicked)
        self.ui_maninWindow.crossvalidateButton.clicked.connect(self.crossvalidateButtonClicked)

    def clearButtonClicked(self):
        self.ui_maninWindow.outputTextEdit.clear()

    def writeToOutput(self, text):
        self.ui_maninWindow.outputTextEdit.append(text)

    def get_dataset(self):
        dataset = self.ui_maninWindow.datasetListWidget.selectedItems()
        if dataset:
            return dataset[0].text()

    def get_max_features(self):
        try:
            max_features = int(self.ui_maninWindow.maxFeatLineEdit.text())
            if max_features < 100 or max_features > 100000:
                self.wrongValueMessage()
            else:
                return max_features
        except ValueError:
            self.wrongValueMessage()

    def get_mingram(self):
        try:
            min_gram = int(self.ui_maninWindow.minGramLineEdit.text())
            if min_gram < 1 or min_gram > 9:
                self.wrongValueMessage()
            else:
                return min_gram
        except ValueError:
            self.wrongValueMessage()

    def get_maxgram(self):
        try:
            max_gram = int(self.ui_maninWindow.maxGramLineEdit.text())
            if max_gram < 2 or max_gram > 10:
                self.wrongValueMessage()
            else:
                return max_gram
        except ValueError:
            self.wrongValueMessage()

    def get_cv_folds(self):
        try:
            cv_folds = int(self.ui_maninWindow.cv_foldsLineEdit.text())
            if cv_folds < 2 or cv_folds > 10:
                self.wrongValueMessage()
            else:
                return cv_folds
        except ValueError:
            self.wrongValueMessage()

    def get_clf_choice(self):
        clf = self.ui_maninWindow.classifierListWidget.selectedItems()
        if clf:
            return clf[0].text()

    def get_analyzer(self):
        analyzer = self.ui_maninWindow.analyzerListWidget.selectedItems()
        if analyzer:
            return analyzer[0].text()

    def get_input_text(self):
        input_text = self.ui_maninWindow.inputTextEdit.toPlainText()
        return input_text

    def wrongValueMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Please make sure to insert a valid integer!")
        msg.setWindowTitle("wrong value")
        msg.exec_()

    def valueMissingMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Please make sure you have selected a value for all parameters!")
        msg.setWindowTitle("value missing")
        msg.exec_()

    def noClassifierMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Please train a classifier first!")
        msg.setWindowTitle("classifier missing")
        msg.exec_()

    def parameters_valid(self):
        if self.get_clf_choice() and self.get_analyzer() and self.get_dataset() and self.get_max_features() \
                and self.get_maxgram() and self.get_mingram() and self.get_cv_folds():
            return True
        else:
            self.valueMissingMessage()

    def predictButtonClicked(self):
        if self.clf is None:
            self.noClassifierMessage()
        else:
            prediction = self.clf.predict(self.get_input_text().split('\n'))
            if prediction[0]:
                self.writeToOutput("Offensive material!")
            else:
                self.writeToOutput("Not offensive!")

    def crossvalidateButtonClicked(self):
        if self.parameters_valid():
            mingram = self.get_mingram()
            maxgram = self.get_maxgram()
            if mingram > maxgram:
                self.wrongValueMessage()
            else:
                start_time = time.time()
                clf = self.get_clf_choice()
                analyzer = self.get_analyzer()
                dataset = self.get_dataset()
                max_features = self.get_max_features()
                cv_folds = self.get_cv_folds()
                model = classify.CLassifier()
                scores = model.cross_validate(dataset, max_features, analyzer, mingram, maxgram, cv_folds, clf)
                avg_acc = "Average accuracy: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2)
                duration = time.time() - start_time
                m, s = divmod(duration, 60)
                h, m = divmod(m, 60)
                self.writeToOutput("Cross validation performed in %02d:%02d:%02d." % (h, m, s))
                self.writeToOutput(avg_acc)

    def trainButtonClicked(self):
        if self.parameters_valid():
            mingram = self.get_mingram()
            maxgram = self.get_maxgram()
            if mingram > maxgram:
                self.wrongValueMessage()
            else:
                start_time = time.time()
                clf = self.get_clf_choice()
                analyzer = self.get_analyzer()
                dataset = self.get_dataset()
                max_features = self.get_max_features()
                model = classify.CLassifier()
                self.clf = model.train(dataset, max_features, analyzer, mingram, maxgram, clf)
                duration = time.time() - start_time
                m, s = divmod(duration, 60)
                h, m = divmod(m, 60)
                self.writeToOutput("Classifier trained in %02d:%02d:%02d." % (h, m, s))
                self.writeToOutput("Now you can use it for prediction!")

