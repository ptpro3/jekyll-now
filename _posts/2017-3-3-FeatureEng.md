---
layout: post
title: Creative Feature Engineering - Apartment Listings Popularity
---
This dataset is part of a [Kaggle competition](https://www.kaggle.com/c/two-sigma-connect-rental-listing-inquiries) hosted in conjunction with [renthop.com](https://www.renthop.com). The apartment listings are from their site, and the goal was to predict the popularity of a particular listing (High, Medium, or Low) based on a variety of features.  
  
Since each listing had an associated manager_id (See data summary in Line 3 in the Notebook), I wanted to see the impact of the listing manager on popularity. Using the provided data, I created an additional feature called "manager skill" which gave a score to each manager, based on a weighted count of high, medium, and low popularity listings (See Line 70). An important caveat was to split the data into training and test set BEFORE this weighted count, to avoid the leaking test set data into the calculated "manager skill".  
  
Results from the Random Forest analysis confirmed that "manager skill" was the strongest predictor of apartment listing popularity (See chart in Line 122).  
  
**See my iPython Notebook for my analysis:**  
[AptListingsAnalysis.ipynb](https://github.com/ptpro3/ptpro3.github.io/blob/master/Projects/AptListingsAnalysis.ipynb)
