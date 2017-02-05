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
The Number of Theaters in which the film showed was not always available; in this case, I used the average number of theaters from the rest of the films in the franchise.
#### Questionable data
As of this writing, three "sequel" films had released in 2017:
- -Underworld: Blood Wars- on Jan 6
- -xXx: The Return of Xander Cage- on Jan 20
- -Resident Evil: The Final Chapter- on Jan 27
I decided to drop these films from my training dataset; because of their recent release date, their gross earnings will not yet be representative of final earnings for a typical sequel film. However, since # of theaters released and previous average gross information was available, I saved this information to try a Gross earnings prediction later on.

### Step 3 - Regression Model
Here's a pairplot of my features and target variable ("AdjGross") to visualize correlations:  
  
![AdjGross Pairplot]({{site.baseurl}}/Projects/Project2/reports/figures/project2_pairplot.png)
  
In the pairplot we can see that 'AdjGross' may have some correlation with the variables, particularly 'Theaters' and 'PrevAvgGross'. However, it looks like a polynomial model, or natural log / some other transformation will be required before fitting a linear model.  
  
My first run of a linear regression model, using the statsmodels toolkit in Python, returned an adjusted R-squared value of 0.548. Adding 2nd degree polynomial complexity to the regression gave a slightly improved adjusted R-squared of 0.626, and a reasonably random distribution of residuals:  
  
![Polynomial Residual Plot]({{site.baseurl}}/Projects/Project2/reports/figures/poly_resid.png)
  
However, the other tests provided by statsmodels suggested issues with my model, including skew and kurtosis. I ran a heteroskedasticity test to check for spread of the data:
```
polymodel = sm.OLS(y, polyX)
polyfit = polymodel.fit()
hetnames = ['Lagrange multiplier statistic', 'p-val', 'f-val', 'f p-val']
hettest = sm.stats.diagnostic.het_breushpagan(fit.resid, fit.model.exog)
zip(hetnames,hettest)
```
The results returned a very small p-value (order of 1e-9), suggesting that the data was indeed heteroskedastic. For this reason I applied the box-cox transformation to the feature columns, and used Log('AdjGross') as the target value. These changes improved the adjusted R-squared to 0.825, and reduced the skew. Finally, I applied the Elastic Net regularization process to the model for optimization of coefficients. My final model produced a Mean Squared Error of 0.545.  
  
To see what kind of predictions this model would provide, I ran it on the 3 new sequels in 2017.
- -Underworld: Blood Wars- on Jan 6
- -xXx: The Return of Xander Cage- on Jan 20
- -Resident Evil: The Final Chapter- on Jan 27

The results, I would say, mostly do not seem reasonable:
- -Underworld: Blood Wars- on Jan 6
-- Predicted
-- test
- -xXx: The Return of Xander Cage- on Jan 20
- -Resident Evil: The Final Chapter- on Jan 27






