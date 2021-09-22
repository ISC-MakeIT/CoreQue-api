import requests 
import unittest
import re
from model import *
from bs4 import BeautifulSoup
# testこーど実行するときpipenv run testを実行するとテストできる



class ModelTest(unittest.TestCase):
    def test_hoge(self):
        def get_url_hand_over(baseURL:str)->list:
            """ This fanction is get baseURL and return itemURL list. 
            """
            result =[]
            res = requests.get(baseURL)
            if res.status_code != 200:
                return false
            soup = BeautifulSoup(res.content, 'html.parser')
            tentative = soup.find_all('figure')
            number_of_times = len(tentative) -1
            for i in range(number_of_times): 
                tentative = soup.find_all('figure')[i]
                link = tentative.find("a")
                url = link.get('href')
                result.append(url)
            return result

        def get_nutrition_put(url:str):
            
        #  connect and organize html
            res = requests.get('https://www.sej.co.jp/{}'.format(url))
            if res.status_code != 200:
                return false
            soup = BeautifulSoup(res.content, 'html.parser')
    
    
            def return_num_nutrition()->list:
            #     養素の数字だけ返す
                
                
                td = soup.find_all('td')
                data = td[1].text

                nutrition = []
                a = re.sub(r"[g|kcal]",  ",",  data)
                b = re.split(r'（|）|kcal |、',  a)
                d = ','.join(b)
                c = d.split(',' '')
                strandint = list(filter(None, c))
                for i in strandint:
                    Coordinate = i.find("：")+1
                    onlyNum =i[Coordinate:]
                    nutrition.append(onlyNum)
                return nutrition
    
            def return_name()->str:
                name = soup.find("h1")
                Hood_name = name.text
                return Hood_name

            return return_name(), return_num_nutrition()
            
    
        #     def create_image_id(url:str)str->:
        #         '''
        #         urlを受け取って写真をS3に保管して
        #         保管した位置？ID変数を変える。
        #         '''
        #         pass
            
        #     def put():
        #          return print(data)
        #     put()
    

        URL = 'https://www.sej.co.jp/products/a/sandwich/1/l100/'
        urls = get_url_hand_over(URL)
        result = {}
        for url in urls:
            name, nutrition = get_nutrition_put(url)
            result[name] = nutrition
        print(result)
        # サンドイッチのやつとかカテゴリ別ごとに全部取れるようになったのであとはawsと写真です
 
        
        

            

        # self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()