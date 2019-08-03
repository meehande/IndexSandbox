def join_url_paths(base_path, *sub_paths):
    base_path = base_path.strip('/')
    sub_paths = [p.strip('/') for p in sub_paths]
    return '/'.join([base_path] + sub_paths)


def get_parent_url(query_url):
    """
    :param query_url: 'https://web.tmxmoney.com/indices.php?section=tsx&index=^TSX#indexInfo'
    :return: 'https://web.tmxmoney.com
    """
    return '/'.join(query_url.split('/')[0:-1])
