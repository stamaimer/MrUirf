import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start_url = "http://m.facebook.com"
user_email= "wendyfrank@126.com"
user_pass = "wendyfrank"
names = {}
persons = {}
graph = {"nodes": [], "links": []}

def login(driver):

    driver.get(start_url)
    driver.find_element_by_name('email').send_keys(user_email)
    driver.find_element_by_name('pass').send_keys(user_pass)
    driver.find_element_by_name('login').click()

    print "logged in."

def set_start_peer(driver, start_peer):
    global presons
    global names
    global graph

    name = start_peer['name']
    link = start_peer['link']
    names[name.lower()] = '0'
    graph['nodes'].append({'group':'0', 'name':name})
    persons['0'] = {'group':'0', 'name':name, 'index':'0', 'father_index':'0', 
                    'link': link}

def exec_peer(driver, person):

    driver.get(person['link'])
    first_cover_xpath = '/html/body/div/div/div[2]/div/div/div[2]'
    first_friends_xpath_template ='/html/body/div/div/div[2]/div/div/div[2]/div[%s]/table/tbody/tr/td[2]/a'
    more_cover_xpath = '/html/body/div/div/div[2]/div/div/div[1]'
    more_friends_xpath_template = 'html/body/div/div/div[2]/div/div/div[1]/div[%s]/table/tbody/tr/td[2]/a'

    # get_friend_list
    driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[1]/div[4]/a[2]').click()

    # get first friend page
    scan_friends(driver, first_cover_xpath, first_friends_xpath_template, person)

    # get more
    while True:
        try:
            more_button = driver.find_element_by_id('m_more_friends')
            more_button.find_element_by_tag_name('a').click()
            scan_friends(driver,more_cover_xpath,more_friends_xpath_template,person)
        except:
            break

def scan_friends(driver, cover_xpath, friend_xpath_template, father):
    global names
    global persons
    global graph

    cover = driver.find_element_by_xpath(cover_xpath)
    page_friends = cover.find_elements_by_tag_name('table')

    for i in range(1, len(page_friends)+1):

        friend = driver.find_element_by_xpath(friend_xpath_template % i)
        name = friend.get_attribute('innerHTML').lower()
        if name == persons[father['father_index']]['name'].lower():
            pass
        elif name in names.keys():
            link1, link2 = {}, {}
            link1['source'] = father['index']
            link1['target'] = names[name]
            link2['source'] = names[name]
            link2['target'] = father['index']
            graph['links'].append(link1)
            graph['links'].append(link2)
        else:
            person = {}
            person['name'] = friend.get_attribute('innerHTML')
            person['link'] = friend.get_attribute('href')
            person['group']= str(int(father['group'])+1)
            person['index']= str(len(graph['nodes']))
            person['father_index'] = father['index']
            persons[person['index']] = person

            names[name] = person['index']

            node = {}
            link1, link2 = {}, {}
            node['group'] = person['group']
            node['name']  = person['name']
            link1['source'] = father['index']
            link1['target'] = person['index']
            link2['source'] = person['index']
            link2['target'] = father['index']
            graph['nodes'].append(node)
            graph['links'].append(link1)
            graph['links'].append(link2)

def default_start():
    name='Aoi Teshima'
    link="http://m.facebook.com/profile.php?id=100003739153500&fref=fr_tab&refid=17"
    return {'name':name, 'link':link}

def gen_network(depth = 2, start_peer = default_start()):
    global persons

    driver = webdriver.Firefox()        # open browser
    login(driver)                       # login
    set_start_peer(driver, start_peer)  # set the seed user

    for group in range(depth):
        group_list = [persons[k] for k in persons.keys() if persons[k]['group'] == str(group)]
        group_len  = len(group_list)
        for i in range(group_len):

            print "-" * 50
            print "pro    : %d / %d" % (i+1, group_len)
            print "name   : %s" % group_list[i]['name']
            print "link   : %s" % group_list[i]['link']
            print "group  : %s" % group_list[i]['group']
            print "index  : %s" % group_list[i]['index']
            print "father : %s" % persons[group_list[i]['father_index']]['name']

            try:
                exec_peer(driver, group_list[i])
            except:
                pass

            print "finished."

    driver.close()
    return graph

if __name__ == "__main__":
    name = u'\u738b\u5e05'
    link = "https://m.facebook.com/stamaimer?refid=46&sld=eyJzZWFyY2hfc2lkIjoiNTNlYmZiMDQ4YTExNTM2N2E1OWJmMzE3N2U0NmJiOTciLCJxdWVyeSI6InN0YW1haW1lciIsInNlYXJjaF90eXBlIjoiU2VhcmNoIiwic2VxdWVuY2VfaWQiOjg4NDMyNTE3NSwicGFnZV9udW1iZXIiOjEsImZpbHRlcl90eXBlIjoiU2VhcmNoIiwiZW50X2lkIjoxMDAwMDUwODAxNzM2NDYsInBvc2l0aW9uIjowLCJyZXN1bHRfdHlwZSI6MjA0OH0%3D&fref=search"

    f_network = gen_network(2, {'name':name, 'link':link})
    f = file('graph2.json', 'w+')
    json.dump(f_network, f)
    f.close()

#    f_network = gen_network(3, {'name':name, 'link':link})
#    f = file('graph3.json', 'w+')
#    json.dump(f_network, f)
#    f.close()
