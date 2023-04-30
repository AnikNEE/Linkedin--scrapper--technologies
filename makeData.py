import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

def uniqueArray(array):
    hashMap = {}
    for word in array:
        if word not in hashMap:
            hashMap[word] = True
    return list(hashMap.keys())
    

# Fired once for each successfully processed job
def addTextToFile(text):
    descriptionFile = open("description.txt", "a")
    allText = uniqueArray(text.split())
    for text in allText:
        try:
            descriptionFile.write(text + "\n")
        except:
            pass
        


def on_data(data: EventData):
    addTextToFile(data.description)
    # data.title, data.company, data.company_link, data.date, data.link, data.insights,
    print('[ON_DATA]', data.description,data.insights,
          len(data.description))


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path="C:\\Users\\anikr\\Downloads\\driver\\chromedriver.exe",  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
    chrome_options=None,  # Custom Chrome options here
    headless=False,  # Overrides headless mode only if chrome_options is None
    max_workers=2,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)    
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
         query='Software',
        options=QueryOptions(
            locations=['United States'],
            apply_link=False,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
            skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=2000,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME, TypeFilters.CONTRACT],
            )
            )
         
    ),
    # Query(
    #     query='Software',
    #     options=QueryOptions(
    #         locations=['India', "india"],
    #         apply_link=False,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
    #         skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
    #         page_offset=0,  # How many pages to skip
    #         limit=5,
    #         filters=QueryFilters(
    #             company_jobs_url='https://www.linkedin.com/jobs/search/?f_C=1441%2C17876832%2C791962%2C2374003%2C18950635%2C16140%2C10440912&geoId=92000000',  # Filter by companies.                
    #             relevance=RelevanceFilters.RECENT,
    #             time=TimeFilters.MONTH,
    #             type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
    #             on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
    #             experience=[ExperienceLevelFilters.MID_SENIOR]
    #         )
    #     )
    # ),
]

scraper.run(queries)