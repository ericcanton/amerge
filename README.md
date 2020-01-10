#amerge.py, Automatic Merge of WeBWorK scores into Canvas gradebooks. 
Requires: Python 3, pandas (version 0.25.3 known to work, likely to work with others) 

Original author: Eric Canton, while teaching Math 412 Winter 2020 at the University of Michigan
Licensed under GNU GPL v3, free (as in gratis, and freedom) to distribute. 
Please see <https://www.gnu.org/licenses/gpl-3.0.html> for full info. 
Written from scratch. Any similarity to other software (especially copyrighted) is indicental
to the functionality, which is elementary. 

---

This script automatically takes the 'total' column from a WeBWorK assignment and
inputs those scores into the appropriate student record of a Canvas gradebook; SIS Login ID 
column on Canvas gradebooks is currently used to identify students. 

The calling method is:

   $ python amerge.py [webwork_scores.csv] [canvas_gradbook.csv] [webwork number]

Here, [webwork number] should be a single integer, e.g. calling

   $ python amerge.py webwork_scores.csv canvas_gradebook.csv 4 

will update the WeBWorK 4 column in canvas_gradebook.csv with the 'total' column of webwork_scores.csv. The
column titles of canvas_gradebook.csv are searched/matched, so the assignment must already exist in Canvas. 
