# -*- coding: utf-8 -*-
import json
import re
from typing import List
import regex
from bs4 import BeautifulSoup
from claim_extractor import Claim, Configuration
from claim_extractor.extractors import FactCheckingSiteExtractor, caching

class NewtralFactCheckingSiteExtractor(FactCheckingSiteExtractor):

    def __init__(self, configuration: Configuration):
        super().__init__(configuration)


    def retrieve_listing_page_urls(self) -> List[str]:
        return ["https://www.newtral.es/zona-verificacion/fact-check/"]

    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
        return -1

    def retrieve_urls(self, parsed_listing_page: BeautifulSoup, listing_page_url: str, number_of_pages: int) \
            -> List[str]:
        query_url = "https://www.newtral.es/wp-json/wp/v2/posts?per_page=100&offset=0&categories=1" + \
                    "&exclude=80729%2C79970%2C78262%2C78455%2C77275%2C77315%2C77161%2C76907%2C76298" + \
                    "%2C75434%2C74706%2C74103%2C74062&_locale=user"

        urls = []

        json_output = caching.get(query_url.format(offset=0), headers=self.headers, timeout=5)
        offset = 0

        while json_output.strip() != "[]":
            pages = json.loads(json_output)
            for page in pages:
                #links
                urls.append(page['link'])
            offset += 100
            json_output = caching.get(query_url.format(offset=offset), headers=self.headers, timeout=5)
           
            
        return urls
    
    def extract_claim_and_review(self, parsed_claim_review_page: BeautifulSoup, url: str) -> List[Claim]:
        claim = Claim()
        claim.set_url(url)
        claim.set_source("newtral")
         #title, claim and autor claim
        title = parsed_claim_review_page.find("meta", attrs={'property': 'og:title'})['content']
        title = title.strip().split("|")[0]
        claim.set_title(title)
        entry_content = parsed_claim_review_page.find("div", attrs={'class': 'entry-content'})
        #print (title)
        dospunto = re.search(r'(: «)', title)
        dospunt = re.search(r'(: “)', title)  
        
        if dospunto:
            claim_a = title.split(":")
            auteur = claim_a[0].strip()
            claim.author = auteur
            claim_text = claim_a[1].strip("« »")
            claim.claim = claim_text
            #print (claim_a)

        elif dospunt:
            claim_b = title.split(":")
            auteur = claim_b[0].strip()
            # print ("auteur:" , auteur)
            claim.author = auteur
            claim_text = claim_b[1].strip(": “ ”")
            # print ("claim :", claim)
            claim.claim = claim_text
        else:
            pass
        #multiple title or claim
        claim_mult = entry_content.findAll('h2')

        if claim_mult :
            claim_al = [i.text.strip() for i in claim_mult]
            dospunt = re.search(r'(: “)', claim_al) 
            dospunto = re.search(r'(: «)', claim_al) 
            if dospunt:
                claim_b = title.split(":")
                auteur = claim_b[0].strip()
                # print ("auteur:" , auteur)
                claim.author = auteur
                claim_text = claim_b[1].strip(": “ ”")
                # print ("claim :", claim)
                claim.claim = claim_text 
            elif dospunto:
                claim_a = title.split(":")
                auteur = claim_a[0].strip()
                claim.author = auteur
                claim_text = claim_a[1].strip("« »")
                claim.claim = claim_text
                #print (claim_a)
            else :
                claim.set_title(claim_al)

                #tags
        tags = parsed_claim_review_page.find_all("meta", attrs={'property': 'article:tag'})
        tag_list = []
        for tag in tags:
            tag_text = tag['content']
            tag_list.append(tag_text)
        claim.set_tags(",".join(tag_list))
        
            #date pubished
        published = parsed_claim_review_page.find("meta", attrs={'property': 'article:published_time'})[
            'content']
        claim.date_published = published.strip()

        
        #autor article
        author_span = parsed_claim_review_page.find("span", attrs={'class': 'c-article__author'})
        author_a = author_span.find("a")
        author_url = author_a['href']
        author_text = author_a.text
        author_text = re.sub('Por', '', author_text).strip()
        claim.author_url = author_url
        claim.review_author = author_text

        # Recuperation du texte de l'article

        entry_text = ""
        body_t = entry_content.find_all('p')
        body = [text.text.strip() for text in body_t]
        entry_text += " ".join(body) + "\n"
        claim.body = entry_text

        # Recuperation des liens dans le texte de l'article
        links = [link['href'] for link in entry_content.find_all('a', href=True)]
        claim.referred_links = links


            #Veracite
        intro = parsed_claim_review_page.find("div", attrs={'class': 'c-article__intro'})

        veracities = ["ENGAÑOSA","ENGAÑOSO","FALSO","FALSA","FALSOS","VERDADERO","VERDAD A MEDIAS"]
        def common(a, b):
            c = [value for value in a if value in b]
            return c

        if intro :
            intro_p = " ".join(str(v) for v in intro)
            #print(type(body_t))
            rating_text_list = intro_p.upper()
            rating_text = [i.strip() for i in common(veracities,rating_text_list)]
            claim.alternate_name = rating_text
        

        else :
            body_a = " ".join(str(v) for v in body)
            #print(type(body_t))
            rating_text_list = body_a.upper()
            rating_text = [i.strip() for i in common(veracities,rating_text_list)]
            claim.alternate_name = rating_text


        return [claim]

