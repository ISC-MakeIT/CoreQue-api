import unittest
from model import *
import requests
from bs4 import BeautifulSoup
import re 
# testこーど実行するときpipenv run testを実行するとテストできる



class ModelTest(unittest.TestCase):
    def test_hoge(self):
        def get_url_hand_over(baseURLa:str)->list:
            """ 
            this fanction is get baseURL 
            and return itemURL list 
            """
            pass

        def get_nutrition_put(url:str):
            
        #  connect and organize html
            res = requests.get(url)
            if res.status_code != 200:
                return false
            soup = BeautifulSoup(res.content, 'html.parser')
    
    
            def return_num_nutrition()->list:
            #     養素の数字だけ返す
                
                nutrition = []
                td = soup.find_all('td')
                data = td[1].text

                nutrition = []
                a = re.sub(r"[g|kcal]",  ",",  data)
                b = re.split(r'（|）|kcal |、',  a)
                c = b.split(',' '')
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
                         
                         
                         
                         
            return return_num_nutrition()
            return return_name()
    
    
    
    
    
    
    
        #     def create_image_id(url:str)str->:
        #         '''
        #         urlを受け取って写真をS3に保管して
        #         保管した位置？ID変数を変える。
        #         '''
        #         pass
            
        #     def put():
        #          return print(data)
        #     put()

        
        
    URL = 'https://www.sej.co.jp/products/a/item/041671/'
    s = get_nutrition_put(URL)
    print(s)




        # self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()