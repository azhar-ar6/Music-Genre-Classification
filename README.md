# Music-Genre-Classification

## Overview

This repository contains a machine learning project for classifying music genres using Spotify data. The project involves preprocessing the data, performing exploratory data analysis (EDA), building and evaluating machine learning models, and visualizing the results. The models include Logistic Regression and Decision Tree Classifier.

## Logistic Regression
A simple linear model used for binary classification tasks. It estimates probabilities using a logistic function.

## Decision Tree Classifier
A non-linear model that splits data into subsets based on feature values. It is visualized to show decision-making paths.

## Dataset

The dataset used for this project is sourced from Kaggle's Spotify Music Genre dataset. 

- **Includes**: Track ID, track name, playlist genre, track popularity, and audio features.
- **Details**: The dataset contains features like danceability, energy, loudness, etc.

## Features

- **Preprocessing**: Data is automatically downloaded, extracted, and cleaned. Missing values are handled, duplicates removed, and categorical variables encoded.
- **Exploratory Data Analysis (EDA)**: Includes genre distribution pie charts, pair plots, correlation heatmaps, box plots, bar plots, histograms, and line plots.
- **Model Building**: Implemented and evaluated models include Logistic Regression and Decision Tree Classifier.
  - **Logistic Regression**: Trained and evaluated for classification accuracy.
  - **Decision Tree Classifier**: Trained, evaluated (accuracy, precision, recall, F1-score), and visualized.

## Technologies

- **Python Libraries**: `numpy`, `pandas`, `seaborn`, `matplotlib`, `plotly`, `sklearn`.
- **Model Visualization**: Using `plot_tree()` for Decision Tree visualization.
- **Model Saving and Loading**: Utilizes `pickle` for model persistence.

## Installation

To set up this project locally, follow these steps:

```bash
git clone https://github.com/yourusername/spotify-genre-classification.git
cd spotify-genre-classification
pip install numpy pandas seaborn matplotlib plotly scikit-learn
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Dataset**: Provided by [Kaggle](https://www.kaggle.com/).
- **Visualization Tools**: Seaborn, Matplotlib, and Plotly.

## Future Work

- **Explore Advanced Models**: Investigate advanced machine learning models and ensemble methods to potentially enhance classification performance.
- **Feature Importance Analysis**: Conduct further analysis to understand feature importance and the decision-making process of the models.
