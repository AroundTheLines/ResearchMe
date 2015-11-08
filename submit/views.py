from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

import datetime as dt
import json, sys
from apiclient.discovery import build
import urllib2

from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint
import re
import binascii

import requests
import json
from wget import download

from .models import Resume, RunningTotal
from pip.cmdoptions import editable

def home(request):
    return render(request, 'submit/home.html', {})

def apply(request):
    return render(request, 'submit/submit.html', {})

def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    return render(request, 'submit/view_resume.html', {"resume":resume})

def review(request):
    dict = []
    for item in Resume.objects.order_by("-rank", "-sub_date", "last_name", "first_name"):
        person = {}
        person["id"] = item.id
        person["first_name"] = item.first_name
        person["last_name"] = item.last_name
        person["sub_date"] = item.sub_date
        person["rank"] = item.rank
        dict.append(person)
    return render(request, 'submit/review.html', {"resumes":dict})

def buildSentReq(text, api_key):
    return 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?text=' + text + '&apikey=' + api_key

class _HTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'br') and not self.hide_output:
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p':
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r'\s+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = unichr(name2codepoint[name])
            self._buf.append(c)

    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._buf.append(unichr(n))

    def get_text(self):
        return re.sub(r' +', ' ', ''.join(self._buf))

def process(request):
    if len(RunningTotal.objects.all()) == 0:RunningTotal(current_top=1).save()
    try:
        resDict = {}
        for elem in request.POST.keys():
            resDict[elem] = request.POST[elem]
        res = Resume()
        res.first_name = resDict[u"first_name"]
        res.last_name = resDict[u"last_name"]
        res.city = resDict[u"city"]
        res.cover_letter = resDict[u"cover_letter"]
        res.skills = resDict[u"skills"]
        res.experience = resDict[u"experience"]
        res.sub_date = timezone.now()
        
        magic_list = {"michael":3}
        score = 0
        
        search_term = resDict["first_name"] + " " + resDict["last_name"] + " " + resDict["city"]
        
        search_engine_id = '000189178235351906276:4wq155moutq'
        api_key = 'AIzaSyBk4Ad294hf10qqnbexaDDC6fZehy5qmOM'
        service = build('customsearch', 'v1', developerKey=api_key)
        collection = service.cse()
    
        sites = 10
        
        request = collection.list(q=search_term,
            num=sites,
            start=1,
            cx=search_engine_id
        )
        response = request.execute()
        json_data = json.dumps(response, sort_keys=True, indent=2)
        
        parsed_file = json.loads(json_data)
        full_resume = ("\n".join(resDict.values())).lower()
        for i in range(sites):
            if "linkedin" not in parsed_file["items"][i]["link"]:
                web_file = urllib2.urlopen(parsed_file["items"][i]["link"])
                print("\"" + parsed_file["items"][i]["link"] + "\" crawled...")
                raw_web_data = web_file.read()
                parser = _HTMLToText()
                try:
                    parser.feed(binascii.b2a_qp(raw_web_data))
                    parser.close()
                except HTMLParseError:
                    pass
                web_data = parser.get_text().lower()
                for word in magic_list.keys():
                    count = web_data.count(word)
                    if count > 0:
                        score += magic_list[word] * 2 * count
            else:sites -= 1
        for word in magic_list.keys():
            rCount = full_resume.count(word)
            if rCount > 0:score += magic_list[word] * rCount
        reqSent = requests.post(buildSentReq(resDict["cover_letter"], '7b54e31e-f0bb-4b91-9ccf-bea208ecf4b4'))
        jsonSent = json.loads(reqSent.content)
        score = score / sites
        res.score = score
        res.save()
        res.sentiment_rank = round(10 * jsonSent['aggregate']['score'], 1)
        if score > float(RunningTotal.objects.all()[0].current_top):
            temp = RunningTotal.objects.all()[0]
            temp.current_top = str(score)
            temp.save()
        for item in Resume.objects.all():
            item.rank = round(10 * float(item.score) / float(RunningTotal.objects.all()[0].current_top),1)
            item.save()
        res.rank = round(10 * float(res.score) / float(RunningTotal.objects.all()[0].current_top),1)
        res.save()
    except:
        raise
    else:return HttpResponseRedirect('./')