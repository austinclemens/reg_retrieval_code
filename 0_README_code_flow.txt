This is to remind me of the program flow for assembling the completed btscs data set.

First, run 1_rule_downloader.py.  This program depends on a spreadsheet of RINs that was created manually by compiling data from reginfo.  It is called rules.csv.

This will output a document called final_fixed that contains basic information about each rule.  Place this on the desktop and run 2_get_doc_nums.  This will associate the RIN of each rule with a doc num and outputs the file rins_2.

Rins_2 contains doc numbers.  Run 3_get_page_numbers to download the appropriate files from the federal register and associate page lengths with each rule.  This outputs the file rins_3.

Run 4_get_comment_totals to run searches at regulations.gov that check for the number of comments in each rule's docket.  At this point, rules are ready to be split and have ideal points associated with them.  The final document is called rins_final_presplit.