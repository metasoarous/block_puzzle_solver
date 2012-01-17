
# Set up db
library(RSQLite)
dbd <- dbDriver("SQLite")

# This function does the whole shebang, setting up the connection, sending the 
# query, and then fetching records. The query defaults to select all fields except
# for the coordinates from every position record, and fetches all records. This
# can be customized directly though the query option, or constrcuted through the
# columns and where options, while the fetch number can be customized with n=...)
dbrecords <- function(run_name, query=NULL, where=NULL, n=-1,
                  columns="id, parent_id, depth, solutions, time")
{
  dbcon <- dbConnect(dbd, paste('output_data/', run_name, '/position_tree.db', sep=""))
  querystr <- paste("select", columns, "from positions")
  if (! is.null(where)) {querystr <- paste(querystr, "where", where)}
  if (! is.null(query)) {querystr <- query}
  dbquery <- dbSendQuery(dbcon, querystr)
  fetch(dbquery, n)
}

