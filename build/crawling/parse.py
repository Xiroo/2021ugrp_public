def elemAtPath(dic, path):
    path = path.split('/')[1:]
    for key in path:
        if key.isdigit():
            key = int(key)
        dic = dic[key]
    return dic


class Contents:
    def __init__(self, info):
        self.info = info

    def _getFromInfo(self, key):
        try:
            return elemAtPath(self.info, key)
        except(KeyError):
            return None


class Video(Contents):
    def __init__(self, info):
        super().__init__(info)
        self.id = self._getId()
        self.title = self._getTitle()
        self.thumb_url = self._getThumbnail()
        self.channel_id = self._getChannel()
        self.length = self._getLength()

    def __str__(self):
        return f'{self.id}, {self.title}, {self.length}, {self.thumb_url}'

    def _getId(self):
        return self.info['videoId']

    def _getTitle(self):
        return self.info['title']['runs'][0]['text']

    def _getThumbnail(self):
        key = '/thumbnail/thumbnails/0/url'
        return self._getFromInfo(key)

    def _getChannel(self):
        key = '/longBylineText/runs/0'
        key += '/navigationEndpoint/commandMetadata/webCommandMetadata'
        key += '/url'
        url = self._getFromInfo(key)
        if url is None:
            return None
        else:
            return url.split('/')[-1]

    def _getLength(self):
        key = "/thumbnailOverlays/0"
        key += "/thumbnailOverlayTimeStatusRenderer"
        key += "/text/simpleText"
        return self._getFromInfo(key)


class Channel(Contents):
    def __init__(self, info):
        super().__init__(info)
        self.id = self._getId()
        self.title = self._getTitle()
        self.thumb_url = self._getThumbnail()
        self.url = self._getUrl()
        self.api_url = self._getApiUrl()

    def __str__(self):
        return f'{self.id}, {self.title}, {self.url}'

    def _getId(self):
        key = '/channelId'
        return self._getFromInfo(key)

    def _getTitle(self):
        key = '/title/simpleText'
        return self._getFromInfo(key)

    def _getThumbnail(self):
        key = '/thumbnail/thumbnails/0/url'
        return self._getFromInfo(key)

    def _getUrl(self):
        key = '/navigationEndpoint/commandMetadata'
        key += '/webCommandMetadata/url'
        return self._getFromInfo(key)

    def _getApiUrl(self):
        key = '/navigationEndpoint/commandMetadata'
        key += '/webCommandMetadata/apiUrl'
        return self._getFromInfo(key)


class Continuation(Contents):
    def __init__(self, info):
        super().__init__(info)
        self.token = self._getToken()
        self.ct_param = self._getCtParam()
        self.api_url = self._getApiUrl()

    def _getToken(self):
        key = '/continuationEndpoint'
        key += '/continuationCommand'
        key += '/token'
        return self._getFromInfo(key)

    def _getApiUrl(self):
        key = '/continuationEndpoint'
        key += '/commandMetadata'
        key += '/webCommandMetadata'
        key += '/apiUrl'
        return self._getFromInfo(key)

    def _getCtParam(self):
        key = '/continuationEndpoint'
        key += '/clickTrackingParams'
        return self._getFromInfo(key)


class Playlist(Contents):
    def __init__(self, info):
        super().__init__(info)
        pass

    def parse(self):
        pass


class ResultsList:
    def __init__(self, renders=None):
        self.channels = []
        self.playlists = []
        self.videos = []
        if renders is not None:
            for render in renders:
                self.append(render)

    def append(self, raw):
        if 'videoRenderer' in raw.keys():
            self.videos.append(Video(raw['videoRenderer']))
        elif 'channelRenderer' in raw.keys():
            self.channels.append(Channel(raw['channelRenderer']))
        elif 'gridVideoRenderer' in raw.keys():
            self.videos.append(Video(raw['gridVideoRenderer']))

    def __len__(self):
        return len(self.videos)

    def __iadd__(self, other):
        self.channels += other.channels
        self.playlists += other.playlists
        self.videos += other.videos
        self.cont = other.cont
        return self
