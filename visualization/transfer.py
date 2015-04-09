import json

def cutter():

    abort_group = int(raw_input("the group need aborted: "))
    filename_source = raw_input("source filename: ")
    filename_target = raw_input("target filename: ")

    abort_index = []
    f = file(filename_source, 'r')
    source = f.read()
    target = json.JSONDecoder().decode(source)
    f.close()

    print '-'*50

    nodes = target['nodes']
    for i in range(len(nodes))[::-1]:
        nodes[i]['group'] = int(nodes[i]['group'])
        if nodes[i]['group'] == abort_group:
            abort_index.append(i)
            del(nodes[i])

    print "total nodes: %s" % len(nodes)
    print '-'*50

    links = target['links']
    for i in range(len(links))[::-1]:
        links[i]['source'] = int(links[i]['source'])
        links[i]['target'] = int(links[i]['target'])
        if links[i]['source'] in abort_index or links[i]['target'] in abort_index:
            del(links[i])

    f = file(filename_target, 'w+')
    f.write(json.dumps(target))
    f.close()

if __name__ == "__main__":

    cutter()
