# scopus-for-sloan

Please clone this repo and run your search functions under the same folder.

**This repo only implements a small subset of Scopus APIs and their features.** If you have extra requirements that are not considered, please visit [Scopus API Interface Specification](https://dev.elsevier.com/api_docs.html) for details and write new functions accordingly.

## Important Notes

1. Run your searches via university network or otherwise the access will be denied by Scopus. VPN doesn't work but you can run it on remote lab. Just make sure the lab connection stays on before your search finishes.
2. Make sure you have enough keys and save them in "keys.csv" in the same folder. There's a sample file in this repo for you to run some tests.
3. Each API offers an explanation for the data fields in its response, e.g. [Scopus Search Views](https://dev.elsevier.com/sc_search_views.html). You can refer to their documentations for interpretation.
4. A folder named "results" is generated each time if there isn't one.

## Others

1. The "***elsapy***" folder contains some of the scripts written by Elsevier's engineers. I removed a lot of files and features that I never used. The original module is [ElsevierDev/elsapy](https://github.com/ElsevierDev/elsapy). But remember that the ***elsapy*** functions are only designed for one-time search, so you have to write outer functions to wrap them, in order to search all your queries at once, which is what I did in the "scopus.py" script in "scopus" folder.
2. The scripts in the "scopus" folder are written by myself, which offer less functions but enough for our demand by now. One thing you might need to notice is that I didn't consider the time interval between searches, because it's been working fine so far without it.
3. I normally use my own versions for abstract and author retrieval, and Elsevier's versions for author search and Scopus search.
4. Abstract retrieval function was designed to retrieve the abstracts of all the papers of certain authors, so you need to provide the **author id** instead of **paper id**. If you only need to get the abstract of one specific paper, don't use this function and just write a simple request function.
5. Because of the reason above, abstract retrieval is much different from author retrieval since it consists of two steps: 1. search papers by author id and 2. retrieve abstracts from links you get from step 1. So I wrote different functions in 2 different modules and they accept different parameters.
6. There are some logging operations that I only used to track the status, and ***elsapy*** also has its logs. A new folder named "logs" will be generated each time you run the scripts. They might not make sense to you, so if you find them confusing just delete them.
7. A temp file named "dumps.json" will be created and overwritten each time you start a search using ***elsapy***'s functions. It becomes useless after the search finishes, you can leave it be or delete it.
8. The scripts still contain some redundant operations that might be confusing but they should not affect the main functions. I'll try to come up with better solutions later. If you have any questions about this current version just let me know.
