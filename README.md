# online-course-categorize-systems
This ML model is especially designed for Ed-Tech organizations who are confused to categorized their courses according to proper guidance. To solve this major problem, it's here to help you. 

In EdTech startups, sometimes, a content manager who is belong from Non-tech background faces lots of difficulties during organizing a particular courses. There are some courses, that require deep knowledge about that tech stacks to properly organize them in website. For example: There are some differences between Data Science & Generative AI topics, but when it comes to separte them & launce different courses about them, a content manager faces multiple difficulties. In that case, this AI Generated model will help to make that task more easier. 

This is one of the most complicated project related to Pytorch & Generative AI. From scraping data to building multilabel model, it took multi stages complicated codes. 

## Stages to build that project 
1. Identifying problems
2. Indentifying website to scraping
3. Build a web scraping script using selenium & store data
4. Initial trainig before multilabel model building
5. Multilabel classification
6. Onnx Deployment
7. Deploying to Huggingface
8. Build a web application file & deploy to server
9. Conclusion


## Identifying problems

The purpose of this project is :

1. Helping Content Manager to organize their courses.
2. Helping learning enthusisast to find suitable courses for them.
3. Content Label research purposes.


## Identifying website to scraping

To collect dataset & run a web scraping script, I have chosen udemy.com site. Undemy is currently one of the most renowned & biggest online courses sites. Besides, due to proper categoriziation & detailed oriented, I have chosen this site. udemy contains 12 main categories & 80+ sub categories. So, this is gonna be a tough & challenging task at web scraping part. 

## Build a web scraping script using selenium & store data

The challening part to build the most efficient web scraping script was to identify the proper elements that contains our desirable data & interact with the site. So my approach was:

1. Go to udemy.com
2. Navigate main categories
3. Access into sub categories
4. Gather Course Name, Price, Categories, urls
5. Access into a single course
6. Combine all details with course descriptions
7. Repeat the process again & again

Through these steps, I have successfully gathered ##350k+ data for 12 Main categories & 80+ Sub categories of courses. 
