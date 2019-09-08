https://www.recalls.gov/rrfda.aspx
https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/udis-classic-hamburger-buns-recalled-due-potential-presence-foreign-material

insert into recallInfo(code, issueDate, brandName, 
companyName, productDescription, recallReason, url) 
VALUES("ABCDEFGHIJK", 1567896362, "MDH", "House Of Spices India",
 "MDH SAMBAR MASALA", "Salmonella", 
 "https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/house-spices-india-issues-recall-mdh-sambar-masala-due-salmonella-contamination");


id INTEGER primary key autoincrement, 
code varchar(15), issueDate INTEGER, 
brandName text, companyName text, 
productDescription text, recallReason text,
url text