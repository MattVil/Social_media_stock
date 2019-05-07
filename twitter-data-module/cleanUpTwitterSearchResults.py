import csv
import preprocessor as p

companiesTracked = ["Tesla", "Google", "Apple", "CVS Health", "Verizon", "Facebook", "Amazon", "General Motors",
                    "Chevron", "J.P. Morgan Chase"]


def recordTweetRegardingTesla(csvLine):
    with open ("tweetsRegardingTesla.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingGoogle(csvLine):
    with open ("tweetsRegardingGoogle.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingApple(csvLine):
    with open ("tweetsRegardingApple.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingCVS_Health(csvLine):
    with open ("tweetsRegardingCVS_Health.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingVerizon(csvLine):
    with open ("tweetsRegardingVerizon.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingFacebook(csvLine):
    with open ("tweetsRegardingFacebook.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingAmazon(csvLine):
    with open ("tweetsRegardingAmazon.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingGm(csvLine):
    with open ("tweetsRegardingGm.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)

def recordTweetRegardingChevron(csvLine):
    with open ("tweetsRegardingChevron.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)
        
def recordTweetRegardingChase(csvLine):
    with open ("tweetsRegardingChase.csv", 'a') as currentCompanyFile:
        csvWriter = csv.writer(currentCompanyFile)
        csvWriter.writerow(csvLine)


p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY)

rawTweetFile = open("rawTweetFile.csv", 'r')
csvReader = csv.reader(rawTweetFile)

for line in csvReader:
    # line[5] is the place where the tweet's raw text lives
        # here we'll remove hashtags, @ symbols, URLs, emojis, and smileys
    line[5] = line[5].replace('#', '')
    line[5] = line[5].replace('@', '')
    # uses tweet-preprocessor library to remove URL's, emojis, and smileys
    line[5] = p.clean(line[5])

    # this if-else structure makes sure tweets are parsed into correct company file
    if line[0] == companiesTracked[0]:
        del line[0]
        recordTweetRegardingTesla(line)

    elif line[0] == companiesTracked[1]:
        del line[0]
        recordTweetRegardingGoogle(line)

    elif line[0] == companiesTracked[2]:
        del line[0]
        recordTweetRegardingApple(line)

    elif line[0] == companiesTracked[3]:
        del line[0]
        recordTweetRegardingCVS_Health(line)

    elif line[0] == companiesTracked[4]:
        del line[0]
        recordTweetRegardingVerizon(line)

    elif line[0] == companiesTracked[5]:
        del line[0]
        recordTweetRegardingFacebook(line)

    elif line[0] == companiesTracked[6]:
        del line[0]
        recordTweetRegardingAmazon(line)

    elif line[0] == companiesTracked[7]:
        del line[0]
        recordTweetRegardingGm(line)

    elif line[0] == companiesTracked[8]:
        del line[0]
        recordTweetRegardingChevron(line)

    elif line[0] == companiesTracked[9]:
        del line[0]
        recordTweetRegardingChase(line)

    else:
        pass