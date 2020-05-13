def transform(self, value, quality, timestamp):
    """
    Transform the incoming value and return a result.

    Arguments:
        self: A reference to the component this binding is configured on.
        value: The incoming value from the binding or the previous transform.
        quality: The quality code of the incoming value.
        timestamp: The timestamp of the incoming value as a java.util.Date
    """

    # [{label, expanded, data, items[]}]
    def add_to_dict(tag, tag_dict):
        if tag[0] not in tag_dict.keys():
            tag_dict[tag[0]] = dict()
        if len(tag) > 1:
            tag_dict[tag[0]] = add_to_dict(tag[1:], tag_dict[tag[0]])
        else:
            tag_dict[tag[0]] = None
        return tag_dict

    def create_tree(tag_dict, path, split='/'):
        tags = list()
        for tag in tag_dict.keys():
            if tag_dict[tag] is not None:
                tags.append({'label': tag,
                             'expanded': False,
                             'data': {'folder': path + split + tag},
                             'items': create_tree(tag_dict[tag], path + split + tag)})
            else:
                tags.append({'label': tag,
                             'data': {'tag': path + split + tag}})
        return tags

    tag_query = system.db.runQuery('SELECT tagpath FROM [Historian].[dbo].[sqlth_te] WHERE [retired] is NULL',
                                   'Historian')
    tag_dict = dict()
    for row in tag_query:
        tag_dict = add_to_dict(row['tagpath'].split('/'), tag_dict)

    tree = create_tree(tag_dict, 'histprov:KNT_IGN_GW01_Historian:/drv:knt-ign-gw01:data:/tag:', split='')

    return tree