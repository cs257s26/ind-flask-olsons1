# README

--------COPY COMMANDS--------
Creating database tables, run this:
If that doesn't work, you can run each \copy for each individual year individually by itself.

for y in 2000 2001 2002 2003 2004 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2020 2021 2022 2023 2024 2025; do
psql -d DATABASE_NAME -c "\copy year_${y} FROM '/Accounts/ACCOUNT_NAME/project-ind/csv/year_${y}.csv' DELIMITER ',' CSV"
done

EXAMPLE: 
for y in 2000 2001 2002 2003 2004 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2020 2021 2022 2023 2024 2025; do
psql -d olsons3 -c "\copy year_${y} FROM '/Accounts/olsons3/project-ind/csv/year_${y}.csv' DELIMITER ',' CSV"
done 

Replace the first olsons3 with your database name. The second olsons3 is whatever account name is. In my case, they are the same.
--------------------------------------------------------------------------------------------------------------------------------

Process:
I chose to include only the bird's name in the first column (I stripped the scientific name off to make it cleaner and easier to use), and then the columns that included the corresponding stop number, going from 1-17. In create_table.sql, I made 3 tables. This is because there are certain gaps in the data where the bird data wasn't recorded for a certain year. So, that is why there are three tables with ranges from 2020..2025, 2008..2018, and then 2000..2004, due to the various missing years. bird_name is TEXT because it is a string, and all of the stops are INT because they are all integers. The primary key is bird_name, because it is used to identify the bird that is associated with the integer values of the next 17 adjacent columns to bird_name. 

How each query represents a user story:

counts_per_stop_for_bird(conn, year, bird_name)
"As a researcher, I want to see how many of a given species were observed at each stop in a specific year so I can inspect spatial distribution along the route."
-The function looks up the single row for bird_name in table year_NUMBER, uses the unnest function on the 17 stop columns to make them into an ordered set of (stop_num, count), sets empty values to 0 and returns the per-stop counts in order from 1-17.
-The researcher could then use the results and with the distances between the stops (not given in our dataset, just theoretical), compute the spatial distribution of a certain species of bird.

total_sightings_per_bird(conn, year)
"As a birdwatcher, I want a ranked list of species by total sightings in a given year so I can identify the most- and least-observed species that season."
-for each row in table year_NUMBER, it computes a per-row total by converting/trimming each stop column to integer (setting empty values to 0) and then returns one row per species with descending maximum per-row total ordered descending by the total count. Duplicate rows are handled, if for some reason found.
-The birdwatcher could use this function to figure out which birds are most typically seen and which ones aren't most typically seen in the Carleton Arb historically.