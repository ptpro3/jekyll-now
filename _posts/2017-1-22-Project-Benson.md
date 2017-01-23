---
layout: post
title: Project Benson
---
## Analyzing New York MTA subway turnstile data
The fictional group, WomenTechWomenYes (WTWY), wants to leverage data to optimize recruitment efforts at subway stations for an upcoming event. In this project my team used publicly available MTA turnstile data to recommend the best way to deploy recruitment/promotion teams.

### Initial Assumptions
- For total turnstile traffic we considered a sum of entries and exits.
- We assumed the gala is being held early in June; thus we used subway data for the 4 weeks of May, 2016.
- We decided to focus the target demographi on women working in the tech industry.
- We further assumed the target demographic will use subway stations near their place of residence; we were not considering major commuter stations as commuters would probably be less likely to attend a Gala in the city.

### Demographics Data
To locate areas with a high density of women residents who work in tech industries, we used public data from the American Community Survey at [Census.gov](http://factfinder.census.gov).
![Census screenshot](https://github.com/ptpro3/ptpro3.github.io/blob/master/images/census_dataV2.png)
For a detailed view of population density we used data count by Census tract, a small subdivision used for Census data, for each of the 5 boroughs/counties of New York City. The Census website has the ability to create a "heatmap" using the requested data, but this functionality was unavailable at the time of this posting; I'm planning to try again and update this page in the future.  

We joined the population data to a list of subway stations, using their corresponding Census tract location from data on ArcGIS.
```
stations = pd.read_csv('subway_station_tracts.csv')
stem_women = pd.read_csv('stem_women.csv')
df = pd.merge(stations, stem_women, on='BoroCT2010')
```
Here is the list of stations with resident count for women in tech occupations > 100.
![Census screenshot](https://github.com/ptpro3/ptpro3.github.io/blob/master/images/stations_gt_100.png)

### Station Traffic Data
Finding the cumulative station traffic for the month required joining the four weeks of turnstile data and aggregating multiple turnstile machines for each station. In order to deal with turnstile counters with mismatched values or counter resets, we added T/F flags to the datasets at machine/counter changes. After aggregation, we still had some negative values and unexpectedly large values due to further counter value errors. We ignored these values by choosing station counts between 0 and 10,000 per 4 hour timeblock.

### Locations to Focus Flyering / Promotion Efforts
**Top Stations by Female Residents in Tech**
1. Roosevelt Island - Main St  
2. 86th St  
3. 72nd St  
4. 28th St  
5. 23rd St  

**Top Stations by Traffic Volume in May**
1. 34th St - Penn Station  
2. Grand Central - 42nd St  
3. 34th St - Herald Sq  
4. 23rd St  
5. 86th St  

From these two lists, it's cear that **86th St** and **23rd St** are great places to focus promotion efforts.

### Outlier
It's worth noting that Roosevelt Island, located in the East River across from Manhattan's Lenox Hill and Midtown East neighborhoods, registered by far the most women residents in tech, at 354. So even though the Roosevelt Island MTA station is not a high traffic stop, it may be worth sending recruitment teams to this area. Upon further reading I learned that this residential neighborhood, close to Manhattan but quieter and cheaper, is actually the location of a major tech initiative - the Cornell Tech campus, opening in summer 2017. Clearly this area will only be increasing in importance for the New York tech scene in coming months.
