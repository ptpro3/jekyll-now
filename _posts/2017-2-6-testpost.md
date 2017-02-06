---
layout: post
title: Project Luther
---
## Analyzing New York MTA subway turnstile data
The fictional group, WomenTechWomenYes (WTWY), wants to leverage data to optimize recruitment efforts at subway stations for an upcoming event. In this project my team used publicly available MTA turnstile data, as well as city demographic data, to recommend the best way to deploy recruitment / promotion teams.

### Initial Assumptions
- For total turnstile traffic, we considered a sum of entries and exits.
- We assumed the gala is being held early in June; thus we used subway data for the 4 weeks of May, 2016.
- We decided to focus the target demographic on women working in the tech industry.
- We further assumed the target demographic will use subway stations near their place of residence; we were not considering major commuter stations as commuters would probably be less likely to attend a gala in the city.

In this case, I decided that the first film in each franchise would not be an observation that I input into the model. Instead, the data for the first film would be included as features for modeling into subsequent sequel films.  I therefore grouped the films by Franchise and appended the first film's data, as well as average earnings data for the franchise, to the sequel films within that franchise. Here is the final set of features that I created for modeling:  
- The Average Adjusted Gross of all previous films in the franchise  
- The Adjusted Gross of the very first film in the franchise  
- The Release Date of the previous film in the franchise  
- The Release Date of the very first film in the franchise  
- The Series Number of the film in that franchise  
- The number of Theaters in which the film showed 
