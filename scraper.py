from selenium import webdriver
from time import sleep


def login(username, 
          password,
          webdriverlocation="C:\\Users\DanielRead\Downloads\chromedriver_win32\chromedriver"):
    
    driver = webdriver.Chrome(webdriverlocation)
    driver.maximize_window()
    
    driver.get('https://www.linkedin.com')
    
    username_field = driver.find_element_by_name('session_key')
    username_field.send_keys(username)
    
    password_field = driver.find_element_by_name('session_key')
    password_field = driver.find_element_by_name('session_password')
    password_field.send_keys(password)
    
    login_btn = driver.find_element_by_class_name('sign-in-form__submit-button')
    login_btn.click()
    sleep(2)
    return driver
    

def searchFromHomePage(term, driver):
    try:
        searchbar = driver.find_element_by_class_name('search-global-typeahead__input')
    except:
        print("Could not find the relevant element. Are we on the right page?")
        
    searchbar.send_keys(term)
    searchbar.send_keys(webdriver.common.keys.Keys.RETURN)
    sleep(5)

    filtergrp = driver.find_element_by_class_name('search-reusables__filters-bar-grouping')
    showposts = filtergrp.find_element_by_xpath("//*[text()='Posts']")
    showposts.click()
    sleep(10)
    
    results = driver.find_element_by_class_name("pb2").text
    print("There are " + results)
    resultsTotal = int(results.split(" ")[0])
    driver.results = resultsTotal
    

def scrapeText(driver, number=0):
    targetResults = 0
    if int(number) > driver.results:
        print("There were only " + str(driver.reults) + ", so we'll try and scrape those")
        targetResults = driver.results
    elif number == 0:
        targetResults = driver.results
    else:
        targetResults = int(number)
    
    resultsTried = 0
    resultsObtained = 0
    
    posts = []
    
    driver.postlist = []
    
    page = 0
    mainWindow = driver.current_window_handle
    harvesting = True
    
    while harvesting:
        searchresultlist = driver.find_element_by_class_name('reusable-search__entity-results-list')
        page += 1
        print("Scraping page " + str(page))
        for post in searchresultlist.find_elements_by_class_name('reusable-search__result-container'):
            ## Select next post in search list and open in new tab:
            post.find_element_by_class_name('entity-result__content-inner-container').click()
            newWindow = ''
            resultsTried += 1
            
            postdata = { "post": resultsTried }
            driver.postdata = postdata
    
            sleep(5)
            
            for handle in driver.window_handles:
                if handle != mainWindow:
                    newWindow = handle
            driver.switch_to.window(newWindow)
            
            ## Search post page for content and add to postdata.
            ## Start with the name and job headline of the poster:
            
            ## Link to post:
            postdata['url'] = driver.current_url
            
            ## Author details:
            
            try:
                postdata['author'] = driver.find_element_by_class_name('feed-shared-actor__name').text
            except:
                postdata['author'] = 'null'
                
            try:
                postdata['headline'] = driver.find_element_by_class_name('feed-shared-actor__description')
            except:
                postdata['headline'] = 'null'
                
            try:
                postdata['authorprofile'] = driver.find_element_by_class_name('feed-shared-actor__container-link').get_attribute('href')
            except:
                postdata['authorprofile'] = 'null'
                
            ## Get the main content text:
            try:
                postdata["body"] = driver.find_element_by_class_name('feed-shared-text').text
            except:
                postdata["body"] = "null"

            ## Is there an image attached?
            try:
                imagecontainer = driver.find_element_by_class_name('feed-shared-image__container')
                try:
                    postdata['imageurl'] = imagecontainer.find_element_by_class_name('feed-shared-image__image').get_attribute('src')
                except:
                    postdata['imageurl'] = 'null'
                    
                try:
                    postdata['imagedescription'] = imagecontainer.find_element_by_class_name('feed-shared-image__image').get_attribute('alt')
                except:
                    postdata['imagedescription'] = 'null'
                                   
            except:
                postdata['imageurl'] = 'null'
                postdata['imagedescription'] = 'null'
                                
            ## Is there an article?
            try:
                articlecontainer = driver.find_element_by_class_name('feed-shared-article')
                try:
                    postdata['articleimageurl'] = articlecontainer.find_element_by_class_name('feed-shared-article__image').get_attribute('src')
                except:
                    postdata['articleimageurl'] = 'null'
                                   
                try:
                    postdata['articleurl'] = articlecontainer.find_element_by_class_name('feed-shared-article__image-link').get_attribute('href')
                except:
                    postdata['articleurl'] = 'null'
                
                try:
                    postdata['articletitle'] = articlecontainer.find_element_by_class_name('feed-shared-article__title').text
                except:
                    postdata['articletitle'] = 'null'   
                    
                try:
                    postdata['articlesubtitle'] = articlecontainer.find_element_by_class_name('feed-shared-article__subtitle').text
                except:
                    postdata['articlesubtitle'] = 'null' 
                
            except:
                postdata['articleimageurl'] = 'null'
                postdata['articleurl'] = 'null'                          
                postdata['articletitle'] = 'null'   
                postdata['articlesubtitle'] = 'null' 
                
            
            driver.postlist.append(postdata)
            resultsObtained += 1            

            if driver.current_window_handle != mainWindow:
                driver.close()
                
            driver.switch_to.window(mainWindow)
            
            if resultsTried >= targetResults:
                harvesting = False
                
                
        driver.find_element_by_class_name('artdeco-pagination__button--next').click()
        sleep(5)
    
    return posts

    
if __name__ == "__main__":
    session = login("danmread5@gmail.com", "Hello567")
    searchFromHomePage("value", session)
    posts = scrapeText(session)