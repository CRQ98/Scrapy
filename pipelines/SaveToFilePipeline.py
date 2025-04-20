import pandas as pd
import csv

class SaveToFilePipeline:
    def __init__(self):
        self.items_dict = {
            'EventItem': [],
            'ParticipantItem': []
        }

    def process_item(self, item, spider):
        class_name = item.__class__.__name__
        if class_name in self.items_dict:
            self.items_dict[class_name].append(dict(item))
        return item

    def close_spider(self, spider):
        for class_name, items in self.items_dict.items():
            if items:
                df = pd.DataFrame(items)
                fields = []
                filename= ""

                # 如果你有特定字段顺序
                if class_name == "EventItem":
                    filename="events"
                    fields = [
                        "cols2update", "eventUrl", "name", "description", "category", "status",
                        "ticketsMinPrice", "freeEntry", "startDate", "startHour", "endHour",
                        "coverImageId", "fulladdress", "address", "city", "postalCode",
                        "provinceCode", "countryCode", "lat", "lng", "pageIds", "ownerId",
                        "identifier", "tags", "extraAddress", "locandina"
                    ]
                elif class_name == "ParticipantItem":
                    filename="participants"
                    fields = [
                        "cols2update", "name", "description", "pageType", "profileImageId",
                        "twitterUrl", "facebookUrl", "linkedinUrl", "instagramUrl", "websiteUrl",
                        "pinterestUrl", "youtubeUrl", "redditUrl", "mediumUrl", "tiktokUrl",
                        "spotifyUrl", "bio", "identifier", "tags"
                    ]
                else:
                    fields = df.columns.tolist()
                #fill all col with no value
                for col in fields:
                    if col not in df.columns:
                        df[col] = ''
                #sort
                df = df.sort_values(by='order')
                #output file
                file_name = f"{filename.lower()}.csv"
                df.to_csv(file_name, index=False, quoting=csv.QUOTE_ALL, columns=fields)
        print('END OF SCRAPE')
