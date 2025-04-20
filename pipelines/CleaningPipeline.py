from itemadapter import ItemAdapter

class CleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # 去除字段中的空格
        for key, value in adapter.items():
            if isinstance(value, str):
                adapter[key] = value.strip()
            elif adapter[key] is None or adapter[key] == '' or adapter[key] == []:
                adapter[key] = ''

        return item
