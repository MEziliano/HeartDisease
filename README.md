<h1 align="center">Heart Disease :mending_heart::drop_of_blood::stethoscope:</h1>


![GitHub last commit](https://img.shields.io/github/last-commit/MEziliano/HeartDisease?style=for-the-badge) 
![GitHub code size](https://img.shields.io/github/languages/code-size/MEziliano/HeartDisease?style=for-the-badge)
![Badge em Desenvolvimento](https://img.shields.io/badge/Status%20-Finished!-brightgreen?style=for-the-badge) 
![BadgeLincese](https://img.shields.io/github/license/MEziliano/HeartDisease?style=for-the-badge) 
![GitHub top language](https://img.shields.io/github/languages/top/MEziliano/HeartDisease?style=for-the-badge) 

</br>
Project about heart disease detection with Python and Machine Learning <br>

<h2> Introduction </h2>

WHO announced that cardiovascular diseases is the top one killer over the world. There are seventeen million people died from it every year, especially heart disease. Prevention is better than cure. If we can evaluate the risk of every patient who probably has heart disease, that is, not only patients but also everyone can do something earlier to keep illness away.

This dataset is a real data including important features of patients. 

 <details><summary>Data Dictionary</summary>
<p>

| Column  | Description |
| ------------- | ------------- |
| Age      | age in years|
| sex      | (1 = male; 0 = female)|
| cp       | Chest pain type   (0-3)| 
| trestbps | resting blood pressure (in **mm Hg** on admission to the hospital)|
| chol     | serum cholestoral in **mg/dl**|
| fbs      | (fasting blood sugar & gt; 120 mg/dl) (1 = true; 0 = false)|
| restcg   | resting electrocardiographic results|
| thalach  | maximum heart rate achieved| 
| exang    | exercise induced angina (1 = yes; 0 = no)|
| oldpeak  | ST depression induced by exercise relative to rest|
| slope    | the slope of the peak exercise ST segment|
| ca       | number of major vessels (0-3) colored by flourosopy|
| thal     | 3 = normal; 6 = fixed defect; 7 = reversable defect.|
</p>
</details>
  
<h2> Exploratory Data Analysis — EDA </h2>

At the EDA part it was necessary check how the data were spread and use a few concepts of inferencial statistics to make some decisions for the next step. 

<h3> Data Construction</h3>

After the EDA, was necessary divide some continnous columns in discrete columns and how them behavior with the target. Columns like: chol, trestbps and others has pass for this step of Data Construction. 


<h2> Machine Learning </h2>

Last but not least, the chosen of the best model of the Machine Learning was based in metrics like Accuracy, Precision, Recall and F1.But the most important metric to watch up is the recall rate. Beacause, it the fraction of relevant instances that were retrieved considerer the After check the best model of a set the models, including linear models and non linear models, the chosen one was the Neural Networks. Which pass for a boosting and a hyperparameter tuning to get a better performance.   


<h2> Used in the project! </h2>
<div>
<a href="https://www.kaggle.com/chingchunyeh/heart-disease-report/data"><img align="center" src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white"></a>
<a href="https://colab.research.google.com/drive/1Mlj9hkHyPX7AiYvmwCotn0UeSJNAImuL"><img align="center" src="https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252" alt="Open In Colab"/></a> 
<img align="center" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" target="_blank">
<img align="center" src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" target="_blank"> 

<h3> Check also this comments</h3>
<a href="https://medium.com/@murilosez06/a-week-inside-a-data-science-project-eabcfd2a2c56" target="_blank"><img align="center" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" target="_blank"></a>
<a href="https://www.notion.so/muriloeziliano/Classification-d621168874bf435780c6b63196e4c8cd" target="_blank"><img align="center" src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white"></a>
<!--<img align="center" src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" target="_blank">
<img align="center" src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" target="_blank">
[![GitHub issues](https://img.shields.io/github/issues/MEziliano/regressao-internacao_SUS?style=for-the-badge)](https://github.com/MEziliano/regressao-internacao_SUS/issues) -->
</div>
