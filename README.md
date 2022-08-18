# paramount_shows
Television show data from paramountplus

## What is this repository?
The Python script `paramount.py` extracts data from [Paramount Plus's list of television shows](https://www.paramountplus.com/shows/all/), downloads the image for each television show, and finally sends a request to the [OMDb API](https://www.omdbapi.com/).

The **main purpose** of this repository is to get [IMDb](https://www.imdb.com/) ratings for the shows on Paramount Plus's website, as the ratings are NOT displayed and it may be useful information to know when searching for a new television series to watch.

### Paramount website:
![Imgur](https://imgur.com/qKaDigT.jpg)

## Output
### Pictures of each show
![Imgur](https://imgur.com/x97Lhxn.jpg)
### Excel workbook of show-related data
![Imgur](https://imgur.com/ZfQLr34.jpg)

## Interesting Findings/Potential Updates
* With an IMDb rating of 9.3, [Avatar: The Last Airbender](https://www.imdb.com/title/tt0417299/?ref_=nv_sr_srsg_3) is the highest rated show on the website (when accounting for number of IMDb ratings).
* Actor frequency: 
![Imgur](https://imgur.com/WPVQEm1.jpg)
* It would be preferable to store the data in a relational database in order to run queries on the data.
* May move away from using the OMDb API, as I've seen cases in which the JSON response has data that vary from the data on IMDb's website.
* Could get updates about a show being removed or a show being added to the website.
