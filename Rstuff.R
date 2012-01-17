
# Set up db
library(RSQLite)
dbd <- dbDriver("SQLite")

# This function does the whole shebang, setting up the connection, sending the 
# query, and then fetching records. The query defaults to select all fields from
# position, and fetch defaults to fetching all records.
dbrecords <- function(run_name, query="select * from positions", n=-1) {
  dbcon <- dbConnect(dbd, paste('output_data/', run_name, '/position_tree.db', sep=""))
  dbquery <- dbSendQuery(dbcon, query)
  fetch(dbquery, n)
}

