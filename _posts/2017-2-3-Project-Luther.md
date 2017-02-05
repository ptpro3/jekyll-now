---
layout: post
title: Project Luther
---
## Analyzing Data for Movie Sequels
Can we predict the success of a movie sequel based on the performance of previous films in the franchise? I set out to answer this question for our second project at Metis.  
  
I gathered the set of all films listed under movie franchises on boxofficemojo.com. My goal was to predict the success of a movie sequel (i.e., domestic gross in USD) based on the overall performance of other sequels, and especially based on previous films in that particular franchise. I applied a Linear Regression model to find the expected gross domestic earnings of a movie sequel.  
  
### Step 1 - Data retrieval
I started with the "Franchises" list on Boxofficemojo.com. Within each franchise page, I scraped each movie's information and enter it into a Python dictionary. If it's already in the dictionary, the entry will be overwritten, except with a different Franchise name. But note below that the url for "Franchises" list was sorted Ascending, so this conveniently rolls "subfranchises" into their "parent" franchise.  
E.g., "Fantastic Beasts" and the "Harry Potter" movies have their own separate Franchises, but they will all be tagged as the "JKRowling" franchise, i.e. "./chart/?id=jkrowling.htm"  
Also, because I was comparing sequels to their predecessors, I focused on Domestic Gross, but adjusted for ticket price inflation over time.  
See my [Project Notebook](https://github.com/ptpro3/ptpro3.github.io/blob/master/Projects/Project2/Project2_Prashant.ipynb) for my webscraping code using the BeautifulSoup tool.  

### Step 2 - Cleaning up and preparing data for regression analysis
The bulk of my time spent on this project was this step, processing the data prior to analysis. It's easy to underestimate the amount of time needed to understand the nuances and anomalies in the dataset and account for them before building an analysis model - even for a relatively straightforward list of movies.  
In this case, I decided that the first film in each franchise would not be an observation that I input into the model. Instead, the data for the first film would be included as features for modeling into subsequent sequel films.  I therefore grouped the films by Franchise and appended the first film's data, as well as average earnings data for the franchise, to the sequel films within that franchise. Here is the final set of features that I created for modeling:
- The Average Adjusted Gross of all previous films in the franchise
- The Adjusted Gross of the very first film in the franchise
- The Release Date of the previous film in the franchise
- The Release Date of the very first film in the franchise
- The Series Number of the film in that franchise
- The number of Theaters in which the film showed

#### Missing data

Number of Theaters in which the film showed
-- Where this number was unavailable, replaced '-' with 0; the 0 will later be replaced with the mean number of theaters for the other films in the same franchise. I chose the average as a reasonable estimate.


For the regression model, I decided to keep data for films released through 2016, but drop the 3 films released this year; because of their recent release date, their gross earnings will not yet be representative.





