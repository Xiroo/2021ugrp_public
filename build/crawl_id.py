import crawling as crl


def get_keywords(filepath):
    keywords = []
    with open(filepath) as f:
        while True:
            tmp = f.readline().rstrip()
            if not tmp:
                break
            tmp = tmp.split('/')
            kind = tmp[1]
            keyword = tmp[2]
            keywords.append((kind, keyword))
    return keywords


def get_video_list(keywords, max_result=100):

    result = []
    for kind, keyword in keywords:

        if kind == 'user':
            contents = crl.ChannelVideoQuery(
                user=keyword,
                max_result=max_result
                )

        elif kind == 'channel':
            contents = crl.ChannelVideoQuery(
                id=keyword,
                max_result=max_result
                )

        elif kind == 'c':
            contents = crl.ChannelVideoQuery(
                c=keyword,
                max_result=max_result
                )

        elif kind == 'search':
            contents = crl.KeyWordQuery(
                keyword,
                kind=crl.VIDEO
                )

        for content in contents:
            result.append(content)

    return result


def filter_by_length(video_list):
    ids = []
    for video in video_list:
        length = video.length
        if length is None:
            continue

        # Do not download video longer than 4 hours
        sec = crl.to_second(length)
        if sec > 3600 * 4:
            continue

        ids.append(video.id)
    return ids


if __name__ == "__main__":
    keywords = get_keywords(crl.CRL_PATH+'/keyword.txt')
    result = get_video_list(keywords=keywords)
    ids = filter_by_length(result)

    with open("id_list.txt", "w") as f:
        for id in ids:
            f.write(id+'\n')
