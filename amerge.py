"""
amerge.py, Automatic Merge of WeBWorK scores into Canvas gradebooks. 
Requires: Python 3, pandas (version 0.25.3 known to work, likely to work with others) 
----
Original author: Eric Canton, while teaching Math 412 Winter 2020 at the University of Michigan
Licensed under GNU GPL v3, free (as in gratis, and freedom) to distribute. 
Please see <https://www.gnu.org/licenses/gpl-3.0.html> for full info. 
Written from scratch. Any similarity to other software (especially copyrighted) is indicental
to the functionality, which is elementary. 
-----------------------------------------------------------------------------------------------
This script automatically takes the 'total' column from a WeBWorK assignment and
inputs those scores into the appropriate student record of a Canvas gradebook; SIS Login ID 
column on Canvas gradebooks is currently used to identify students. 

The calling method is:

   $ python amerge.py [webwork_scores.csv] [canvas_gradbook.csv] [webwork number]

Here, [webwork number] should be a single integer, e.g. calling

   $ python amerge.py webwork_scores.csv canvas_gradebook.csv 4 

will update the WeBWorK 4 column in canvas_gradebook.csv with the 'total' column of webwork_scores.csv. The
column titles of canvas_gradebook.csv are searched/matched, so the assignment must already exist in Canvas. 
-----------------------------------------------------------------------------------------------
"""

import sys
import pandas as pd
import re

## Check that the correct number of arguments have been passed
## Note: amerge.py is sys.argv[0], so we expect *FOUR* args: ['amerge.py', webwork_scores.csv, canvas_gradebook.csv, ww_number]
if len(sys.argv) != 4:
    print("There should be exactly three arguments passed to amerge.py, in this order:\n 1. WeBWorK CSV file\n 2. Canvas gradebook CSV file\n 3. an integer, indicating which WeBWorK to be updated.")

else:
    ## Import the csv files containing webwork scores, canvas gradebook
    webwork_df = pd.read_csv(sys.argv[1], index_col=1, header=6)
    canvas_df = pd.read_csv(sys.argv[2])

    ## Find the name of the column in canvas_df corresponding to the webwork number passed as sys.argv[3]
    ## --> This regular expression could be changed to update other columns, or to use other naming conventions. 
    ## ----> Currently matches (N = sys.argv[3]): WeBWorK N, Webwork N, WeBwork N, WebWork N, WebworK N, WeBWork N, WeBworK N, WebWorK N
    webwork_name = list(filter(re.compile("We[Bb][Ww]or[Kk] {} \([0-9].*\)".format(sys.argv[3])).match, list(canvas_df.columns.values)))[0]

    ## Make a new dataframe, containing the SIS Login ID (e.g., umich uniqname) as index and the webwork_name found above as only other column
    #
    ## The reason we need this: for pd.DataFrame.update step, easiest/smoothest to have uniqname as index. 
    ## Canvas wants that column to *not* be used as index/first column for CSV. 
    tmp_canvas_df = canvas_df.filter(["SIS Login ID", webwork_name], axis=1).set_index("SIS Login ID")

    ## Extract 'total' column from webwork_df as a pd.Series, then change its name so pd.DataFrame.update(..) will work correctly
    export = webwork_df['total']
    export.name = webwork_name
    tmp_canvas_df.update(export)

    ## copy the modified column back to canvas_df
    canvas_df.update(tmp_canvas_df.reset_index()[webwork_name])
    
    ## write canvas_df back to the disk. 
    with open(sys.argv[2], mode="w", newline="") as outfile:
        canvas_df.to_csv(path_or_buf=outfile, sep=',', index=False) # index=False so a new column with indices is not added to front.
