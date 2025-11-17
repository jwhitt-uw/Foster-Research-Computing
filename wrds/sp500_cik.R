library("RPostgres")

# If you need to restart the connection. Fill in your username below
wrds <- dbConnect(Postgres(),
                  host = "wrds-pgdata.wharton.upenn.edu",
                  port = 9737,
                  user = "",
                  sslmode = "require",
                  dbname = "wrds"
                  
)

#Pull CIKs for companies listed in the SP500 between 2020 and 2023
q <- "select distinct cik from (
        select distinct a.gvkey,cik,year,spcode
        from execcomp.anncomp a
        LEFT JOIN
        (select distinct gvkey,cik from comp.names) b
        on a.gvkey=b.gvkey
        where year > 2019 and year < 2024
        and spcode='SP') c"

#Submit query to WRDS
dq <- dbSendQuery(wrds,q)
ciks <- dbFetch(dq)

#Write to CSV
write.csv(ciks,'ciks.csv')
