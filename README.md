# Chevron Vehicle Prediction

Welcome! This project was developed during the Spring 2025 Rice Datathon in collaboration with Chevron. Our main goal is to predict future vehicle trends — such as the types of vehicles (gas sedans, electric vans, diesel trucks), the fuel technologies they will use, and how many of them we might see on the road in the coming years.

    ⚠️ Note: This project is still in production. Some features or scripts may not work perfectly just yet.

## Project Overview

We worked with a dataset containing around 41,000 records, mostly composed of categorical features like fuel type, vehicle category, and fuel technology. From the start, our aim was to predict not only the vehicle and fuel types but also estimate the population size of each vehicle type in the future.

During our initial data exploration, we encountered a significant number of missing values. Rather than dropping rows (which could lead to major data loss), we implemented imputation techniques to fill in the blanks. Additionally, since most features were categorical, we used label encoding to convert them into numerical values suitable for machine learning models.

We also discovered that the data exhibited non-linear patterns, confirmed through visualizations like box plots and KDE plots, as well as correlation testing. Traditional correlation methods (which favor linear relationships) didn’t reveal strong associations, so we shifted toward a non-linear modeling approach. This involved applying logarithmic transformations to our features to better handle scaling and improve model performance. It also helped reduce redundancy and tackle overfitting issues we encountered early on.
Modeling Process

To find the most effective models, we used PyCaret, which allowed us to quickly test and compare a variety of machine learning algorithms. The best performers were Random Forest models, achieving 98% R² in our regression task and 89% accuracy in classification.

We built a streamlined modeling pipeline that included imputation, scaling (using RobustScaler, which is resilient to outliers), and training. This not only sped up our workflow but also improved reproducibility and consistency in results.
Results and Current Work

So far, our models have performed well in training:

    Regression: 98% R² score

    Classification: 89% accuracy

We are now working on fine-tuning the models and extending their capabilities to make time-based predictions, such as estimating vehicle category trends 6 months or several years into the future. We're also exploring ways to display and share these results interactively.

# Technology
- Python
- Numpy
- Matplotlib
- Seaborn
- MissingNo
- Scikit-Learn
- Pyspark
- DBT
- Kaggle API
