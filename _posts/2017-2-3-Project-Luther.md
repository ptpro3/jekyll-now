---
layout: post
title: Metis Project 2
---
## Analyzing Data for Movie Sequels
Can we predict the success of a movie sequel based on the performance of previous films in the franchise? I set out to answer this question for our second project at Metis.  
  
I gathered the set of all films listed under movie franchises on boxofficemojo.com. My goal was to predict the success of a movie sequel (i.e., domestic gross in USD) based on the overall performance of other sequels, and especially based on previous films in that particular franchise. I applied a Linear Regression model to find the expected gross domestic earnings of a movie sequel.  
  
  
### Step 1 - Data retrieval
I started with the "Franchises" list on Boxofficemojo.com. Within each franchise page, I scraped each movie's information and enter it into a Python dictionary. If it's already in the dictionary, the entry will be overwritten, except with a different Franchise name. But note below that the url for "Franchises" list was sorted Ascending, so this conveniently rolls "subfranchises" into their "parent" franchise. E.g., _Fantastic Beasts_ and the _Harry Potter_ movies have their own separate Franchises, but they will all be tagged as the _JKRowling_ franchise.
  
Also, because I was comparing sequels to their predecessors, I focused on Domestic Gross, but adjusted for ticket price inflation over time.  
  
See my [Project Notebook](https://github.com/ptpro3/ptpro3.github.io/blob/master/Projects/Project2/Project2_Prashant.ipynb) for my webscraping code using the BeautifulSoup tool.  
  
  
### Step 2 - Cleaning up and preparing data for regression analysis
The bulk of my time spent on this project was this step, processing the data prior to analysis. It's easy to underestimate the amount of time needed to understand the nuances and anomalies in the dataset and account for them before building an analysis model - even for a relatively straightforward list of movies.  
  
In this case, I decided that the first film in each franchise would not be an observation that I input into the model. Instead, the data for the first film would be included as features for modeling into subsequent sequel films.  I therefore grouped the films by Franchise and appended the first film's data, as well as average earnings data for the franchise, to the sequel films within that franchise.

#### Final set of features created for modeling
- The Average Adjusted Gross of all previous films in the franchise  
- The Adjusted Gross of the very first film in the franchise  
- The Release Date of the previous film in the franchise  
- The Release Date of the very first film in the franchise  
- The Series Number of the film in that franchise  
- The number of Theaters in which the film showed  

#### Missing data
The Number of Theaters in which the film showed was not always available; in this case, I used the average number of theaters from the rest of the films in the franchise.  

#### Sequels released in 2017 
- _Underworld: Blood Wars_ on Jan 6  
- _xXx: The Return of Xander Cage_ on Jan 20  
- _Resident Evil: The Final Chapter_ on Jan 27  

I decided to drop these films from my training dataset; because of their recent release date, their gross earnings will not yet be representative of final earnings for a typical sequel film. However, since number of theaters released and previous average gross information was available, I saved this information to try a Gross earnings prediction later on.
  
  
### Step 3 - Regression Model
Here's a correlation pairplot (thanks seaborn) of my features and target variable (`AdjGross`) to visualize correlations:  
  
![AdjGross Pairplot]({{site.baseurl}}/Projects/Project2/reports/figures/project2_pairplot.png)
  
In the pairplot we can see that `AdjGross` may have some correlation with the variables, particularly `Theaters` and `PrevAvgGross`. However, it looks like a polynomial model, or natural log / some other transformation will be required before fitting a linear model.  
  
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
  
The results returned a very small p-value (order of 1e-9), suggesting that the data was indeed heteroskedastic. For this reason I applied the box-cox transformation to the feature columns, and used Log(`AdjGross`) as the target value. These changes improved the adjusted R-squared to 0.825, and reduced the skew. Finally, I applied the Elastic Net regularization process to the model for optimization of coefficients. My final model produced a Mean Squared Error of 0.545.  
  
To see what kind of predictions this model would provide, I ran it on the 3 new sequels in 2017.

#### 2017 Sequels - Predictions:
- _Underworld: Blood Wars_ on Jan 6  
  + Predicted Gross $3.6M  
  + Actual as of 2/1 $16.6M  
- _xXx: The Return of Xander Cage_ on Jan 20  
  + Predicted Gross $752M  
  + Actual as of 2/1 $35.8M  
- _Resident Evil: The Final Chapter_ on Jan 27  
  + Predicted Gross $150M  
  + Actual as of 2/1 $29.8M  
  
  
### Thoughts
The above results, I would say, mostly do not seem reasonable. My next steps on the model for this project would be to pinpoint what's causing the extreme values in the above prediction. Looking back at the statsmodels output for summary statistics on my model is a great starting point.  
  
Even if I can improve on this model given the data I have, it's important to consider other factors that could contribute to a sequel films success, such as the number of key actors from the previous films that return for the sequel, and the budget of the film itself. Although it's impossible to know exactly how any particular film will do in the future, I'm confident that with more time spent on this model I'll be able to improve my predictions.
