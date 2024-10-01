
<!--Set environment and load needed functions-->

# Creating Models with Music Data

## Summary

This project offers comprehensive instructions for setting up the
Spotify API, utilizing it in Python, and identifying various musical
attributes for analysis, visualization, and model creation.

## Table of Contents

<ol type="I">
<li>
<a href='#Background'>Background</a>
</li>
<li>
<a href='#Notebooks'>Notebooks</a>
</li>
<ul>
<li>
<a href='#SettingUptheAPI'>1. Setting Up the API Connection</a>
</li>
<li>
<a href='#UsingtheAPI'>2. Using the Spotify API</a>
</li>
<li>
<a href='#UnderstandingtheData'>3. Understanding the Data</a>
</li>
<li>
<a href='#Create3DModel'>4. Creating a 3D Music Model</a>
</li>
<li>
<a href='#Create3DPrint'>5. Creating a 3D Print</a>
</li>
<li>
<a href='#CreatePredictiveModel'>6. Creating a Predictive Model</a>
</li>
</ul>
</ol>

## <a name="Background"></a>Background

This project represents the culmination of several ambitions, distilled
into a comprehensive instruction manual detailing my journey through
these endeavors.

My initial experience with the Spotify API occurred during a summer
project in my Master’s program at Mizzou, where we analyzed Spotify’s
audio features to explore the evolution of music over the past five
decades. Using this data, we provided context for these changes using
data insights. The highlight of this project was a machine learning
model we developed that could predict with a reasonable amount of
certainty which decade a song was released, with a margin of error of
just one to two years.

This first project laid the groundwork for what was to be an ambitious
capstone endeavor. Spotify provides an audio analysis for tracks on its
platform. We recognized the potential of the audio analysis and aimed to
create a machine learning algorithm capable of “listening” to a song and
suggesting similar tracks for recommendations. Unfortunately, we were
ultimately forced to abandon this project as it was deemed too ambitious
for a senior capstone and did not align with the program’s criteria for
a final project.

Despite this setback, my desire for such a utility never waned. As a
selective music listener, I crave a system that can generate a list of
songs similar to those I love. Years later, I finally found some free
time to revisit this project. After refreshing my knowledge and
conducting some new research, I discovered three key insights:

1.  The audio analysis data provides me exactly with what I need to
    create a convolutional neural network (CNN).
2.  The data makes for some very intriguing and stunning visuals.
3.  I may be able to print any 3D renderings on a 3D printer.

The third point excited me the most. Having access to a quality 3D
printer at home meant I only needed to generate an STL file from any 3D
model I created in Python. Around the time I realized this, my brother
had just gotten married, and his birthday was approaching. I set it is a
goal gift him my first 3D print of the song to which he and his wife had
their first dance: “Tennessee Whiskey” by Chris Stapleton. The notebooks
<a href='#Create3DModel'>Creating a 3D Model</a> and
<a href='#Create3DPrint'>Creating a 3D Print</a> provide detail on how
this was accomplished.

With that project completed, I had a strong code foundation and enough
domain knowledge to undertake the larger, more ambitious project — the
predictive model. While the code and results for this model are still in
development, I hope to share them soon.

## <a name="Notebooks"></a>Notebooks

#### <a name="SettingUptheAPI"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/1)%20Setting%20Up%20the%20API%20Connection.ipynb'>1. Setting Up the API Connection</a>

Setting up keys with Spotify and connecting to the API in Python using
the *Spotipy* library.

#### <a name="UsingtheAPI"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/2)%20Using%20the%20Spotify%20API.ipynb'>2. Using the Spotify API</a>

Using the *Spotipy* library and navigating the Spotify API.

#### <a name="Understanding the Data"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/3.%20Understanding%20the%20Data.ipynb'>3. Understanding the Data</a>

A review of the audio features and attributes available in the API and
how to retrieve them.

#### <a name="Create3DModel"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/4.%20Creating%20a%203D%20Music%20Model.ipynb'>4. Creating a 3D Music Model</a>

Creating a 3D rendering using a song’s timbre from the audio analysis.

#### <a name="Create3DPrint"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/5.%20Creating%20a%203D%20Print.ipynb'>5. Creating a 3D Print</a>

The conclusion for 3D portion of the project. Putting it all together
and creating a 3D print with the data.

#### <a name="CreatePredictiveModel"></a>6. Creating a Predictive Model

**!!Coming Soon!!**

This notebook outlines how I built the predictive model for finding
songs similar to a given song.
