# SF-MOHCD-GMS-Scraper

When I worked at the SF LGBT Center, we needed to mass upload our clients' info into the Grants Management System of the Mayor's Office of Housing and Community Development web portal, but each person is given a unique ID number within the system that you need to include with the rest of the data for upload but which for some reason prior to my employment the Center had not been keeping track of. While it's fairly trivial to generate a random alphanumeric sequence to assign as an ID (and the excel tracker that this program was originally paired with does so if the individual is not already in GMS), doing so without checking first if the individual already exists in the system would lead to the proliferation of duplicate profiles. Therefore, I wrote this scraper to look through every single individual in the GMS database and check if anyone we were trying to upload showed up there already.

In order to make the possibility of mis-identifying/conflating two profiles with the same name, in addition to the ID number the scraper also pulls the date of birth (and with one or two extra lines, can also grab the SSN) of each person. Finally, it dumps the data it's gathered on every person in GMS into a massive Excel document called "foo.xlsx" where it can be compared against the extant list of participants. In the associated Excel tracker, this is done automatically.

This was my first real use of the TkInter GUI builder module, as I usually just work in the terminal window but none of my co-workers would have been comfortable doing the same.

Unfortunately I was not able to take the Excel tracker with me when I left the LGBT Center due to the personal information contained on it, so this program will have to stand alone for the time being.
