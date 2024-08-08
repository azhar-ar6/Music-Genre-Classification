# -*- coding: utf-8 -*-
"""Music_Genre_Classification

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13jQpV0vI6UzjEZHCfZdafqS7ugdikTX4
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'spotify-music-genre:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F5510533%2F9127313%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240808%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240808T010337Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D104d707981f421dc2307899c89c80a5b9c9f812be13f1b820d05167ac6f23fab8273a68a286e595073810ed6a7e9fa90ae05b8416443b32b4e612396493feca7f7ffc0ebb2192ecfd3b73409d62913cdcb80a6b8413d9234a30ad566bc395b440cb2db31ed1ed2e7269429fc0e8a723824de88b03732035bd325368513a8794f2f06ba0ace6c8cd9068bd7f0579f96ed30ef41a03f7b7e29cc95c8a304b7fa30289d0b58a5bccf781dc66c0e7866f3ef1a11b69276ab016866e791349b36ff23486215052ccbacc00e6a245034ddf36ef8ab8ea9ebca93962bb001dbb04491fc5868851a1c55fb7d41f940028429aed7c9380f9e4a47176b48c26e85e18674e0'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""# Importing Libraries and Packages"""

# Import libraries for data manipulation and visualization.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

"""# Loading the dataset"""

# Load dataset

df = pd.read_csv('/kaggle/input/spotify-music-genre/spotify_songs.csv')

"""# Data Preprocessing"""

# Display dataset info

df.info()

# Display first few rows

df.head()

# Descriptive statistics of numeric columns

df.describe()

# Check for missing values

df.isnull().sum()

print(f"Percentage of songs with no data: {round(5/32833,4)}%")

# Replace infinite values with NaN

df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Fill missing values with 'unknown'

dfClean = df.fillna('unknown')

# Check for duplicate track IDs

dfClean.duplicated('track_id').sum()

# Remove duplicate track IDs

dfClean.drop_duplicates('track_id', inplace=True)

# Check DataFrame shape after cleaning

dfClean.shape

# Check for missing values in cleaned DataFrame

dfClean.isnull().sum()

"""# Exploratory Data Analysis"""

# Pie chart of genre distribution

genre_count = dfClean['playlist_genre'].value_counts()
plt.figure(figsize=(8,8))
plt.pie(genre_count, labels=genre_count.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title("Genre Distribution in Playlists")
plt.show()

"""- **Dominant Genres**: Rap, Pop, and EDM are the most prominent genres in the playlists, suggesting that these styles have       substantial appeal among users.

- **Significant Presence**: Latin and Rock genres also have notable shares, reflecting their continuing influence and popularity.

- **Balanced Distribution**: The genre distribution is relatively balanced, with no single genre overwhelmingly dominating the playlists, indicating a diverse range of musical preferences.
"""

# Pair plot of selected variables

warnings.filterwarnings("ignore", category=FutureWarning)
variable_relationship = dfClean[['track_popularity', 'danceability', 'energy', 'loudness', 'valence']]
sns.pairplot(variable_relationship)
plt.show()

"""- **Energy and Loudness**: There is a positive correlation between energy and loudness. This suggests that songs with higher energy levels tend to be louder.

- **Danceability and Energy**: There is a positive correlation between danceability and energy. This means that more danceable songs tend to have higher energy levels.
"""

# Correlation matrix heatmap

numeric_columns = dfClean.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_columns.corr()
plt.figure(figsize=(12,8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.show()

"""The correlation matrix heatmap shows the relationships between different audio features of a song. Here are some major interpretations:

- Strong negative correlation between **energy** and **acousticness**: Songs with high energy tend to have low acousticness, and vice versa. This is expected, as acousticness is a measure of how acoustic a song sounds, while energy is a measure of how intense it is.

- Strong positive correlation between **loudness** and **energy**: The correlation heatmap shows that loudness and energy have a positive correlation of 0.68. This means that songs with higher energy levels tend to be louder, and vice versa.
"""

# Box plot of track popularity by genre

plt.figure(figsize=(14,8))
sns.boxplot(x='playlist_genre', y='track_popularity', data=dfClean)
plt.title("Box Plot of Track Popularity by Playlist Genre")
plt.xlabel('Playlist Genre')
plt.ylabel('Track Popularity')
plt.show()

"""- Pop music has the highest median popularity, followed by rap and latin.
- Rock and EDM genres have a wider range of track popularity, with some tracks being very popular and others less so.
"""

# Bar plot of average track popularity by genre

average_popularity_by_genre = dfClean.groupby('playlist_genre')['track_popularity'].mean().reset_index()
plt.figure(figsize=(12,6))
sns.barplot(x='playlist_genre', y='track_popularity', data=average_popularity_by_genre, palette='plasma')
plt.title('Average Track Popularity by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Track Popularity')
plt.show()

"""- Pop music has the highest average track popularity, followed by rap and latin music.
- Rock, R&B, and EDM music have a lower average track popularity.
"""

# Pair plot of 'energy', 'danceability', and 'valence' by genre

sns.pairplot(dfClean[['energy', 'danceability', 'valence', 'playlist_genre']], hue='playlist_genre', palette='viridis')
plt.show()

"""- **Energy vs. Danceability**: There appears to be a positive correlation between energy and danceability across most genres. This means that tracks that are high in energy tend to also be high in danceability, and vice versa. This makes sense, as high-energy music is typically more suited for dancing.

- **Energy vs. Valence**: The relationship between energy and valence is more varied across genres. Pop, rock, and EDM genres appear to have a mix of high-energy tracks that can be either positive or negative. Latin music tends to have high-energy tracks that are also positive. R&B music tends to have lower energy tracks, but these tracks can range in valence.
"""

# Histogram of numeric columns

numeric_cols = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 'duration_ms', 'track_popularity']
plt.figure(figsize=(14, 10))
for i, col in enumerate(numeric_cols, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df[col], kde=True, bins=20, color='skyblue')
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

"""- **Danceability**: The distribution is slightly skewed to the right, with more tracks having a higher danceability score. This suggests most music in the dataset leans towards being more suitable for dancing.
- **Energy**: Similar to danceability, energy is also skewed to the right, indicating there are more energetic tracks than less energetic ones.
- **Loudness**: The loudness distribution appears more symmetrical, with an equal number of tracks having a higher or lower loudness level.
- **Valence**: This distribution is also somewhat symmetrical, with a slight bias towards more positive valence scores. There are still a good amount of tracks with a negative valence, though.
- **Tempo**: The tempo distribution is skewed to the right, with a concentration of tracks having a lower tempo. There are still some tracks with a higher tempo, but they are less frequent.
- **Duration_ms**: The distribution of track durations is skewed to the right. There are more tracks with a shorter duration than tracks with a longer duration.
- **Track Popularity**: This distribution is skewed to the right, with more tracks having a lower popularity score. There are a smaller number of tracks with a very high popularity.
"""

# Violin plot of energy distribution by genre

plt.figure(figsize=(12, 8))
sns.violinplot(x='playlist_genre', y='energy', data=dfClean, palette='pastel')
plt.title('Distribution of Energy by Genre')
plt.xlabel('Playlist Genre')
plt.ylabel('Energy')
plt.show()

"""- Rock and edm tend to be more energetic.
- R&B songs are usually the least energetic.
"""

# Line plots of music trends based on various attributes

dfcpy = df.copy()
dfcpy['track_album_release_date'] = pd.to_datetime(dfcpy['track_album_release_date'], format='mixed')
dfcpy['year'] =pd.DatetimeIndex(dfcpy.track_album_release_date).year

attributes = {
    'acousticness': 'Music Trends Based on Acousticness',
    'danceability': 'Music Trends Based on Danceability',
    'loudness': 'Music Trends Based on Loudness',
    'energy': 'Music Trends Based on Energy'
}
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
axes = axes.flatten()
for i, (attr, title) in enumerate(attributes.items()):
    sns.lineplot(x='year', y=attr, data=dfcpy, ax=axes[i])
    axes[i].set_title(title)
    axes[i].set_xlabel('Year')
    axes[i].set_ylabel(attr.capitalize())
plt.tight_layout()
plt.show()

"""**Acousticness**: The line plot for acousticness suggests a slight decrease in acousticness over time. This means that music may be trending towards being less acoustic (more electronic) in recent years.

**Danceability**: The line plot for danceability shows a possible increase in danceability over time. This suggests that music may be trending towards being more danceable in recent years.

**Loudness**: The line plot for loudness has high fluctuations till 1990. Later, it consistently increased over time with minute fluctuations.

**Energy**: The trend for energy is fluctuating between 0.6 - 0.8 consistently.

# Feature Engineering
"""

# Label encode categorical columns

from sklearn.preprocessing import LabelEncoder

categorical_columns = dfClean.select_dtypes(include=['object']).columns
le = LabelEncoder()
for col in categorical_columns:
    dfClean[col] = le.fit_transform(dfClean[col])

"""Label Encoding is used to convert categorical labels into numerical values. This is important because most machine learning algorithms require numerical inputs."""

#dependent variable

y=dfClean['playlist_genre']
y

#independent variable

X=dfClean.drop(columns=['playlist_genre'],axis=1)
X.head()

"""# Train-Test Split"""

# Split data into training and test sets (0.3 -> 30% test dataset & 0.7 -> 70% training dataset)

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.70,test_size=0.30,random_state=10)

"""Data is split into training (70%) and testing (30%) sets. Training set (X_train, y_train) is used to build the model. Testing set (X_test, y_test) is used to evaluate the model's performance."""

X_train

"""# Feature Scaling"""

# Feature Scaling

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train_s = sc.fit_transform(X_train)
X_test_s = sc.transform(X_test)

"""- 'StandardScaler' standardizes features by removing the mean and scaling to unit variance.
- 'fit_transform' computes the necessary statistics from the training data and applies the transformation.
- 'transform' applies the same transformation to the test data, ensuring consistency between training and testing datasets.

# Logistic Regression
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Model Builing
model = LogisticRegression(max_iter=1000)
model.fit(X_train_s, y_train)

# Model Training
Y_pred = model.predict(X_test_s)

# Model Evaluation
accuracy = accuracy_score(y_test, Y_pred)
print("Accuracy:", accuracy)

"""- The accuracy of the Logistic Regression model is approximately 0.554 (or 55.4%). This value indicates the proportion of correctly classified instances out of the total instances in the test dataset.

- Logistic Regression assumes linear relationships between features and the target, which may not be suitable for datasets with non-linear relationships or complex interactions.

- So, Decision Trees can handle non-linear relationships and feature interactions better, and provide a visual representation of the decision-making process. This might lead to improved accuracy compared to Logistic Regression.

# Decision Tree Classifier

- **Model Building**
"""

from sklearn.tree import DecisionTreeClassifier  # Import the DecisionTreeClassifier class
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Create a decision tree classifier
dt_model = DecisionTreeClassifier(max_depth=8, random_state=0)  # Set random_state for reproducibility

"""- **Model Training**"""

# Train the model on the training set

dt_model.fit(X_train, y_train)

from IPython.display import clear_output
clear_output(wait=True)

"""- **Model Testing**"""

# Make predictions on the testing set

y_pred = dt_model.predict(X_test)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Evaluate model performance

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

"""- **Compute Confusion Matrix**"""

from sklearn.tree import plot_tree  # Import plot_tree

# Creating a confusion matrix:
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

"""- **Plotting Decision Tree**"""

# Visualize the decision tree:

dt_model.classes_ = dt_model.classes_.astype(str)
fig, ax = plt.subplots(figsize=(30, 20))

plot_tree(
    dt_model,
    filled=True,
    feature_names=X_train.columns,
    class_names=dt_model.classes_,
    fontsize = 10
)

plt.title("Decision Tree Visualization", fontsize=14, y=1.05)
plt.show()

"""- The Decision Tree Classifier demonstrates outstanding performance with an accuracy of approximately 99.7%. This high accuracy, alongside Precision (99.7%), Recall (99.7%), and F1-score (99.7%), signifies that the model is highly effective in correctly classifying the majority of instances.

- The Precision and Recall values being very close to 1 indicate that the model is both precise and comprehensive in its classifications, effectively minimizing false positives and false negatives. The F1-score, which balances both metrics, further supports the model's consistent and reliable performance.

- The visualization of the Decision Tree enhances interpretability by showing how the model makes decisions based on features. This visualization helps in understanding feature importance and the decision-making process.

- So, with the superior performance of the Decision Tree Classifier compared to Logistic Regression, the Decision Tree Classifier has the ability to handle complex, non-linear relationships likely contributing to its high accuracy. Future explorations could involve testing other advanced models or ensemble methods to potentially achieve even better results or confirm the robustness of these findings.
"""

import pickle

# Assuming `dt_model` is your trained Decision Tree model
with open('decision_tree_model.pkl', 'wb') as file:
    pickle.dump(dt_model, file)

import pickle

# Load the model from the file
with open('decision_tree_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Now you can use `loaded_model` to make predictions or evaluate

