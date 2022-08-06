ham_list = []

with open('/Users/ajz/Documents/local-git/allhams/EN.dat') as en:
    for line in en:
        fields = line.split(sep='|')
#        print(fields)
#        quit()
        #4 16 17 18
        call_city_state_zip = fields[4:5] + fields[16:19]
        ham_list.append(call_city_state_zip)
        if __name__ == '__main__':
            print("%s,%s,%s,%s" % (fields[4], fields[16], fields[17], fields[18]))
