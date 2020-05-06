### Goals for the project
- Scrape job boards
  - Indeed
  - LinkedIn
  - ZipRecruiter
  - AngelList
  - Google jobs
- Auto populate job board tracking spreadsheet with relevant info
- Auto create cover letter

### Current progress
- Proof of concepts
  - Indeed job search
    - Need to expand query, return from multiple pages
    - Click through postings and return more information [Done]
    - Export data to usable format 
      - Postgres Database? Excel?

#### Notes

- Find job desc id with data-jk or id per DIV

    <div class="jobsearch-SerpJobCard unifiedRow row result clickcard" id="pj_38fd707fced0c98a" data-jk="38fd707fced0c98a" data-empn="6078419695541597" data-ci="344683386">

https://ca.indeed.com/jobs?q=developer&l=Toronto%2C+ON

