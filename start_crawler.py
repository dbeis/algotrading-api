import sys
from crawler import available_crawlers, start_crawler

# python start_crawler.py [crawler] arg0:val0 ... argN:valN
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        print('No target crawler selected')
        exit()
    
    crawler = args[0]
    if crawler not in available_crawlers:
        print(f'{crawler} is not a valid crawler.\n Please select one from: {list(available_crawlers)}.')
        exit()
    
    params = args[1:]
    config = dict(map(lambda x: x.split(':'), params))

    print(f'Starting crawler {crawler}')
    start_crawler(crawler, config)
