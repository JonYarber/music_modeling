
<a name='top'></a>

# Creating Models with Music Data

> ⚠️ **Important Note**  
> Spotify has shut down access to their audio analysis endpoint.  
> The methods in this repo will no longer work to collect audio feature data.  
> This project should be viewed as an educational resource and a fun exploration, not a reproducible workflow.

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
<a href='#DataInsights'>3. Spotify Audio Data Insights</a>
</li>
<li>
<a href='#Create3DModel'>4. Creating a 3D Audio Model</a>
</li>
<li>
<a href='#Print3DModel'>5. Printing the 3D Audio Model</a>
</li>
<li>
<a href='#CreatePredictiveModel'>6. Creating a Predictive Model</a>
</li>
</ul>
</ol>

## <a name="Background"></a>Background

This project culminates my endeavors with the Spotify API data,
distilled into a comprehensive instruction manual and guide.

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

1.  The audio analysis data is perfect for building a deep learning
    model.
2.  The data makes for some intriguing and stunning visuals.
3.  I might be able to print any said visuals or renderings onto my 3D
    printer at home.

The third point excited me the most. Having access to a quality 3D
printer at home meant I only needed to generate an STL file from any 3D
model I created in Python. Around the time I realized this, my brother
had just gotten married, and his birthday was approaching. I set it is a
goal gift him my first 3D print of the song to which he and his wife had
their first dance: <i>Tennessee Whiskey</i> by Chris Stapleton. The
notebooks <a href='#Create3DModel'>Creating a 3D Audio Model</a> and
<a href='#Print3DModel'>Printing the 3D Audio Model</a> provide detail
on how this was accomplished.

With that project completed, I had a strong code foundation and enough
domain knowledge to undertake the larger, more ambitious project — the
predictive model. The code and results for this model are still in
development, but I hope to share them soon.

## <a name="Notebooks"></a>Notebooks

#### <a name="SettingUptheAPI"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/01SettingUptheAPIConnection.ipynb'> Setting Up the API Connection</a>

Setting up client ID and user keys with Spotify and connecting to the
API in Python using the *Spotipy* library.

#### <a name="UsingtheAPI"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/02UsingtheSpotifyAPI.ipynb'>Using the Spotify API</a>

Using the *Spotipy* library in Python to navigate the Spotify API.

#### <a name="DataInsights"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/03SpotifyAudioDataInsights.ipynb'> Spotify Audio Data Insights</a>

A review of the audio features and attributes available in the Spotify
API and how to retrieve them.

#### <a name="Create3DModel"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/04Creatinga3DAudioModel.ipynb'>Creating a 3D Audio Model</a>

Creating a 3D rendering using a song’s timbre from the audio analysis
data.

#### <a name="Print3DModel"></a><a href='https://nbviewer.org/github/JonYarber/music_modeling/blob/main/python/05Printingthe3DAudioModel.ipynb'> Printing the 3D Audio Model</a>

The conclusion for 3D portion of the project. Putting it all together
and creating a 3D print with the data.

#### <a name="CreatePredictiveModel"></a><a href = "https://https://github.com/JonYarber/music_modeling/blob/main/python/06BuildingthePredictiveModel.ipynb">Building the Predictive Model</a> 

**In Progress**

This notebook outlines how I built the predictive model for finding
songs similar to a given song.

<a href='#top'>Back to top</a>
