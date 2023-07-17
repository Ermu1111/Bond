import requests
from lxml import etree
import json
import csv


class bond():
    url = 'https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN'
    form_data = {
        'pageNo': 1,
        'pageSize': 15,
        'isin': '',
        'bondCode': '',
        'issueEnty': '',
        'bondType': 100001,
        'couponType': '',
        'issueYear': 2023,
        'rtngShrt': '',

    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Cookie': 'apache=4a63b086221745dd13be58c2f7de0338; _ulta_id.ECM-Prod.ccc4=a6c3da5adcdc68f1; _ulta_ses.ECM-Prod.ccc4=d832ce7b1db5944c; lss=fd9e664ef34511dcdc4a51a4e8d84abc; isLogin=0; _ulta_id.CM-Prod.ccc4=947e4d6c1ecc47ef; _ulta_ses.CM-Prod.ccc4=3929fc0beb5d704c; AlteonP10=BMC6UCw/F6zlwVIqjDs+fw$$',
        'Host': 'iftp.chinamoney.com.cn',
        'Origin': 'https://iftp.chinamoney.com.cn',
        'Referer': 'https://iftp.chinamoney.com.cn/english/bdInfo/'
    }

    def __init__(self):
        self.f = open('bond.csv', mode='a+', newline='')
        csv_header = ["bondDefinedCode", "bondName", "bondCode", "issueStartDate",
                      "issueEndDate", "bondTypeCode", "bondType",
                      "entyFullName", "entyDefinedCode",
                      "debtRtng", "isin", "inptTp"]
        self.writer = csv.DictWriter(self.f, csv_header)
        self.writer.writeheader()

    def bond(self):
        res = requests.post(self.url, data=self.form_data, headers=self.headers)
        txt_lst = [i for i in json.loads(res.text)['data']['resultList']]
        self.page_total = json.loads(res.text)['data']['pageTotal']
        return txt_lst

    def save(self, lst):
        self.writer.writerows(lst)

    def main(self):
        txt = self.bond()
        self.save(txt)
        while self.page_total > self.form_data['pageNo']:
            self.form_data['pageNo'] += 1
            txt = self.bond()
            self.save(txt)
        self.f.close()


if __name__ == '__main__':
    bond = bond()
    bond.main()
