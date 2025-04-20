# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParticipantItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    order = scrapy.Field()
    cols2update = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    pageType = scrapy.Field()
    profileImageId = scrapy.Field()
    twitterUrl = scrapy.Field()
    facebookUrl = scrapy.Field()
    linkedinUrl = scrapy.Field()
    instagramUrl = scrapy.Field()
    websiteUrl = scrapy.Field()
    pinterestUrl = scrapy.Field()
    youtubeUrl = scrapy.Field()
    redditUrl = scrapy.Field()
    mediumUrl = scrapy.Field()
    tiktokUrl = scrapy.Field()
    spotifyUrl = scrapy.Field()
    bio = scrapy.Field()
    identifier = scrapy.Field()
    tags = scrapy.Field()

class EventItem(scrapy.Item):
    order = scrapy.Field()
    cols2update = scrapy.Field()
    eventUrl = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    ticketsMinPrice = scrapy.Field()
    freeEntry = scrapy.Field()
    startDate = scrapy.Field()
    startHour = scrapy.Field()
    endHour = scrapy.Field()
    coverImageId = scrapy.Field()
    fulladdress = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    postalCode = scrapy.Field()
    provinceCode = scrapy.Field()
    countryCode = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    pageIds = scrapy.Field()
    ownerId = scrapy.Field()
    identifier = scrapy.Field()
    tags = scrapy.Field()
    extraAddress = scrapy.Field()
    locandina = scrapy.Field()

