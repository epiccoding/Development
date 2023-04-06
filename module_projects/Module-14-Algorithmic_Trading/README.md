# Eli's Responses to Questions

[Answer 1](#eli-answer-1) | [Answer 2](#eli-answer-2) | [Answer 3](#eli-answer-3) | [Answer 4](#eli-answer-4) | [Answer 5](#eli-answer-5)

# Machine Learning Trading Bot

In this Challenge, you’ll assume the role of a financial advisor at one of the top five financial advisory firms in the world. Your firm constantly competes with the other major firms to manage and automatically trade assets in a highly dynamic environment. In recent years, your firm has heavily profited by using computer algorithms that can buy and sell faster than human traders.

The speed of these transactions gave your firm a competitive advantage early on. But, people still need to specifically program these systems, which limits their ability to adapt to new data. You’re thus planning to improve the existing algorithmic trading systems and maintain the firm’s competitive advantage in the market. To do so, you’ll enhance the existing trading signals with machine learning algorithms that can adapt to new data.

## Instructions:

Use the starter code file to complete the steps that the instructions outline. The steps for this Challenge are divided into the following sections:

* Establish a Baseline Performance

* Tune the Baseline Trading Algorithm

* Evaluate a New Machine Learning Classifier

* Create an Evaluation Report

#### Establish a Baseline Performance

In this section, you’ll run the provided starter code to establish a baseline performance for the trading algorithm. To do so, complete the following steps.

Open the Jupyter notebook. Restart the kernel, run the provided cells that correspond with the first three steps, and then proceed to step four. 

1. Import the OHLCV dataset into a Pandas DataFrame.

![1.1](Resources/Images/1_1.PNG)

2. Generate trading signals using short- and long-window SMA values. 

![1.2](Resources/Images/1_2.PNG)

3. Split the data into training and testing datasets.

4. Use the `SVC` classifier model from SKLearn's support vector machine (SVM) learning method to fit the training data and make predictions based on the testing data. Review the predictions.

5. Review the classification report associated with the `SVC` model predictions. 

![1.5](Resources/Images/1_5.PNG)

6. Create a predictions DataFrame that contains columns for “Predicted” values, “Actual Returns”, and “Strategy Returns”.

![1.6](Resources/Images/1_6.PNG)

7. Create a cumulative return plot that shows the actual returns vs. the strategy returns. Save a PNG image of this plot. This will serve as a baseline against which to compare the effects of tuning the trading algorithm.

![1.7](Resources/Images/1_7.PNG)

8. Write your conclusions about the performance of the baseline trading algorithm in the `README.md` file that’s associated with your GitHub repository. Support your findings by using the PNG image that you saved in the previous step.

# Eli Answer 1
> You can see that the performance of the Strategy Returns was able to outperform the Actual Returns with confidence starting back in late 2018.  You could see the losses were less than the Actual and returns started to really diverge at the end, in a positive way.

---

#### Tune the Baseline Trading Algorithm

In this section, you’ll tune, or adjust, the model’s input features to find the parameters that result in the best trading outcomes. (You’ll choose the best by comparing the cumulative products of the strategy returns.) To do so, complete the following steps:

1. Tune the training algorithm by adjusting the size of the training dataset. To do so, slice your data into different periods. Rerun the notebook with the updated parameters, and record the results in your `README.md` file. 

# Tuned to 5 months

>![2.1(5m)](Resources/Images/2.1(5m).PNG)
>![2.1](Resources/Images/2_1.PNG)

Answer the following question: What impact resulted from increasing or decreasing the training window?

# Eli Answer 2
> Very interest to see, the strategy return actually underperformed the actual return in the 2019-2020 range where it confidently outperformed it using the 3m time frame.  The Returns leading into 2021 are also appearing to lag behind the Actual Returns in this scenario.

> **Hint** To adjust the size of the training dataset, you can use a different `DateOffset` value&mdash;for example, six months. Be aware that changing the size of the training dataset also affects the size of the testing dataset.

---

2. Tune the trading algorithm by adjusting the SMA input features. Adjust one or both of the windows for the algorithm. Rerun the notebook with the updated parameters, and record the results in your `README.md` file. 

# Short Window = 3 Long Window = 50

>![2.2](Resources/Images/2_2.PNG)
>![2.2(SMA)](Resources/Images/2_2SMA.PNG)

Answer the following question: What impact resulted from increasing or decreasing either or both of the SMA windows?

# Eli Answer 3

> By decreasing the short and long window you can see that the accuracy of the report really suffered, dropping down to .50 where we were averaging around .55/.56 previously.  Performance also appears to lag significantly still.

---

3. Choose the set of parameters that best improved the trading algorithm returns. Save a PNG image of the cumulative product of the actual returns vs. the strategy returns, and document your conclusion in your `README.md` file.

# Eli Answer 4
> Ironically I could not get another combination to work that actually outperformed the Actual Returns aside from the original combination that seemed to really outperform it.

#### Evaluate a New Machine Learning Classifier

In this section, you’ll use the original parameters that the starter code provided. But, you’ll apply them to the performance of a second machine learning model. To do so, complete the following steps:

1. Import a new classifier, such as `AdaBoost`, `DecisionTreeClassifier`, or `LogisticRegression`. (For the full list of classifiers, refer to the [Supervised learning page](https://scikit-learn.org/stable/supervised_learning.html) in the scikit-learn documentation.)

2. Using the original training data as the baseline model, fit another model with the new classifier.

3. Backtest the new model to evaluate its performance. Save a PNG image of the cumulative product of the actual returns vs. the strategy returns for this updated trading algorithm, and write your conclusions in your `README.md` file. 

![3_3](Resources/Images/3_2.PNG)
![3_3Plot](Resources/Images/3_3.PNG)

Answer the following questions: Did this new model perform better or worse than the provided baseline model? Did this new model perform better or worse than your tuned trading algorithm?

# Eli Answer 5

> It would appear that the new model performed slightly better in the long-run but the Actual Returns were slightly more advantageous during the 2019-2020 timeframe and should be acknowledged.  In the future the Actual Returns could end up outpacing the AB Strategy again.

#### Create an Evaluation Report

In the previous sections, you updated your `README.md` file with your conclusions. To accomplish this section, you need to add a summary evaluation report at the end of the `README.md` file. For this report, express your final conclusions and analysis. Support your findings by using the PNG images that you created.
