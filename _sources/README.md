# user-survey-analysis
I wrote a script to clean the data (remove emails, use boolean values to denote if someone selected it or not) and grab the location data, and ignore some rows.
This script can be re-run any time we export data.

See resulting csv 'cleaned.csv' https://github.com/crkn-rcdr/user-survey-analysis/blob/main/cleaned.csv

Then this tool: https://deepnote.com is like chat GPT but for Jupyter notebooks.

I used it to cluster the other interests and other identifiers columns to get an idea of what to replace them with in a seperate notebook, then I ran this notebook to actually do the replacing/analysis:
https://deepnote.com/workspace/test-a092-13c907c4-9de1-4de5-8373-b00517621d65/project/User-Survey-Analysis-78bfc222-b866-4a43-b8a8-c2a8d5467ce5/notebook/Analysis-022286145a4f4103b4e2f4af0d9e09b9

Then I exported the notebook file and set up a jupyter books github pages site here showing the analysis so we can have it forever or have a sequence of pages by date etc:
https://crkn-rcdr.github.io/user-survey-analysis/notebooks.html

I think if you all have time you should take the cleaned CSV and do some of your own analysis using deepnote! 

Deploy instructions: https://jupyterbook.org/en/stable/start/publish.html
