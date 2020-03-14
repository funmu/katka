# README.md

Small collection of custom script to process the Sparksip Sponsors list to create 

## Files and Folders

 * [SparkSIP Convertor](xformSparkSip.js) uses nodejs for conversion of input JSON to HTML

 * [Inputs](./inputs) Folder
 * [Outputs](./output) Folder
 * [Templates Folder](./templates)


## Steps
Steps to get the projects

1. Get sponsorships from Business owners - run a Google Forms inquiry (Feb)
2. Export the JSON view from sruvey results (data as array using "Add-ons / Export Sheet Data")
3. Ensure some key fields are present - Title, email, etc.
4. Store this exported JSON file in the inputs folder
5. run "make output" to generate the output
6. zip up the output files and send it to Sparksip Organizers

### Sparksip JSON to HTML files
 Convert the input SPARKSIP JSON files to HTML to post on the sparksip.org website

 Concluded that I Cannot do this conversion easily after spending 45 minutes on it.


 Run the converter code as follows to generate the required output html
 ```
 mkdir -p output/2017
 node xformSparksip.js ./inputs/input-projects-for-2017.json 

 pushd output/2017/
 zip ../projects-2017.zip *
 popd
 
 ```

