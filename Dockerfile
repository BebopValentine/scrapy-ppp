FROM python:3.6
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD scrapy crawl light_novel