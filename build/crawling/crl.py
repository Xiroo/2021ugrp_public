from .parse import ResultsList, Continuation, elemAtPath
from urllib import parse
import requests
import json

from .variable import ORIGIN, RESULT_PATH, USER_AGENT

VIDEO = 1
CHANNEL = 2
PLAYLIST = 4

context = {}
with open('./crawling/context.txt', 'r') as f:
    context = json.load(f)


class Query:
    def __init__(self, max_result):
        self.results = []
        self.max_result = max_result

    def __getitem__(self, idx):
        if idx > self.max_result:
            raise IndexError()
        while len(self.results) <= idx and self.cont is not None:
            self.expand()
        return self.results[idx]

    def __len__(self):
        return len(self.results)

    def expand(self):
        raise NotImplementedError


class KeyWordQuery(Query):
    def __init__(self, keyword, kind=VIDEO, max_result=100):
        super().__init__(max_result=max_result)

        self.keyword = keyword
        self.kind = kind

        self.query = self.init_query
        self.expand()
        self.query = self.cont_query

    def init_query(self):
        query = {
            "search_query": self.keyword,
        }
        res = requests.get(RESULT_PATH, params=query)
        html = res.text
        s_idx = html.find('var ytInitialData')

        pair_cnt = 1
        idx = s_idx + 21
        while pair_cnt > 0:
            if html[idx] == '{':
                pair_cnt += 1
            elif html[idx] == '}':
                pair_cnt -= 1
            idx += 1

        s_idx += 20
        e_idx = idx

        return json.loads(html[s_idx:e_idx])

    def cont_query(self):
        global context

        queryed_url = RESULT_PATH + '?search_query=' \
            f'{parse.quote(self.keyword)}'

        user_agent = USER_AGENT

        context['client']['originalUrl'] = queryed_url
        context['client']['mainAppWebInfo']['graftUrl'] = queryed_url
        context['clickTracking']['clickTrackingParams'] = self.cont.ct_param

        data = {
            'context': context,
            'continuation': self.cont.token,
        }

        headers = {
            'referer': queryed_url,
            'origin': ORIGIN,
            'content-type': 'application/json',
            'user-agent': user_agent,
        }

        param = {
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        }

        path = ORIGIN + self.cont.api_url

        res = requests.post(
            path,
            json=data,
            params=param,
            headers=headers,
        )

        return json.loads(res.text)

    def expand(self):
        raw = self.query()
        contents_render, cont_item_render = self.extractRenders(raw)
        result = ResultsList(contents_render)

        self.expand_hook(result)
        self.cont = Continuation(cont_item_render['continuationItemRenderer'])

    def extractRenders(self, raw):
        if 'contents' in raw:
            key = '/contents'
            key += '/twoColumnSearchResultsRenderer'
            key += '/primaryContents'
            key += '/sectionListRenderer'
            key += '/contents'
            items = elemAtPath(raw, key)
        elif 'onResponseReceivedCommands' in raw:
            key = '/onResponseReceivedCommands'
            key += '/0'
            key += '/appendContinuationItemsAction'
            key += '/continuationItems'
            items = elemAtPath(raw, key)

        cur_item_render = items[0]
        cont_item_render = items[1]

        contents = cur_item_render['itemSectionRenderer']['contents']

        return (contents, cont_item_render)

    def expand_hook(self, result):
        if self.kind & VIDEO:
            self.results += result.videos
        if self.kind & CHANNEL:
            self.results += result.channels
        if self.kind & PLAYLIST:
            self.results += result.playlists
        return


class ChannelQuery(Query):
    def __init__(self, user, max_result):
        super().__init__(max_result=max_result)
        self.user = user


class ChannelVideoQuery(ChannelQuery):
    def __init__(self, user=None, id=None, c=None, max_result=100):
        super().__init__(user, max_result)
        if user is None and id is None and c is None:
            raise ValueError
        elif user is not None:
            self.api_url = f'/user/{user}/videos'
        elif id is not None:
            self.api_url = f'/channel/{id}/videos'
        elif c is not None:
            self.api_url = f'/c/{c}/videos'

        self.query = self.init_query
        self.expand()
        self.query = self.cont_query

    def init_query(self):
        path = ORIGIN + self.api_url
        res = requests.get(path)
        html = res.text
        s_idx = html.find('var ytInitialData')

        pair_cnt = 1
        idx = s_idx + 21
        while pair_cnt > 0:
            if html[idx] == '{':
                pair_cnt += 1
            elif html[idx] == '}':
                pair_cnt -= 1
            idx += 1

        s_idx += 20
        e_idx = idx
        return json.loads(html[s_idx:e_idx])

    def extractRenders(self, raw):
        if "contents" in raw.keys():
            key = '/contents'
            key += '/twoColumnBrowseResultsRenderer'
            key += '/tabs/1/tabRenderer'
            key += '/content/sectionListRenderer/contents/0'
            key += '/itemSectionRenderer/contents/0/gridRenderer/items'
            items = elemAtPath(raw, key)
        elif 'onResponseReceivedActions' in raw.keys():
            key = '/onResponseReceivedActions/0'
            key += '/appendContinuationItemsAction'
            key += '/continuationItems'
            items = elemAtPath(raw, key)

        if 'continuationItemRenderer' in items[-1]:
            return (items[0:-1], items[-1])
        else:
            return (items, None)

    def cont_query(self):
        global context
        queryed_url = ORIGIN + self.api_url
        user_agent = USER_AGENT

        context['client']['originalUrl'] = queryed_url
        context['client']['mainAppWebInfo']['graftUrl'] = queryed_url
        context['clickTracking']['clickTrackingParams'] = self.cont.ct_param

        data = {
            'context': context,
            'continuation': self.cont.token,
        }

        headers = {
            'referer': queryed_url,
            'origin': ORIGIN,
            'content-type': 'application/json',
            'user-agent': user_agent,
        }

        param = {
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        }

        path = ORIGIN + self.cont.api_url

        res = requests.post(
            path,
            json=data,
            params=param,
            headers=headers,
        )

        return json.loads(res.text)

    def expand(self):
        raw = self.query()
        contents_render, cont_item_render = self.extractRenders(raw)

        result = ResultsList(contents_render)
        self.results += result.videos

        if cont_item_render is None:
            self.cont = None
            return

        self.cont = Continuation(cont_item_render['continuationItemRenderer'])


class ChannelPlayListQuery(ChannelQuery):
    pass


def get_contents(keyword, min_results=10):
    """
        Get information from youtube search results.
        Return more than the number specified in min_results.
    """
    ret = []
    if keyword is not None:
        query = KeyWordQuery(keyword, VIDEO | CHANNEL)

    for idx in range(min_results):
        ret.append(query[idx])
    return ret
