# README.md

## Tools

### Azuqua
 Try out Azuqua to build up convesion tools.

 Concluded that I Cannot do this conversion easily after spending 45 minutes on it.

 ## JSON to HTML conversion using nodejs
 * [SparkSIP Convertor](xformSparkSip.js)

 Run the converter code as follows to generate the required output html
 ```
 mkdir -p output/2017
 node xformSparksip.js ./inputs/input-projects-for-2017.json 

 pushd output/2017/
 zip ../projects-2017.zip *
 popd
 
 ```

