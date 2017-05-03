
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

# telegram
from telepot.delegate import per_chat_id, create_open, pave_event_space
import telepot
import re
import os
import requests
import tempfile
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

try:
    from Queue import Queue
except ImportError:
    from queue import Queue





def khane(request):
        return render(request, 'user_profile/home.html')

def service(request):
        return render(request, 'user_profile/service.html')


def faq(request):
        return render(request, 'user_profile/faq.html')

def aboutus(request):
        return render(request, 'user_profile/aboutus.html')

def barname(request):
        return render(request, 'user_profile/barname.html')

def nini(request):
        return render(request, 'user_profile/nini.html')



# test
def test(request):
        return render(request, 'user_profile/500.html')



def handler404(request):
    response = render_to_response('user_profile/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('user_profile/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



# telegrambot
class MessageCounter(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):

        bot = telepot.DelegatorBot('333028480:AAG2EAmXyBfGqV4XYyD7iD7EEZnd6zvil78', [
            pave_event_space()(
                per_chat_id(), create_open, MessageCounter, timeout=10),
        ])
        bot.message_loop()  # take updates from queue

        print(msg)
        chat_id = msg['chat']['id']

        if 'text' in msg:
            if re.search(r'hello', msg['text'], re.MULTILINE):
                bot.sendMessage(chat_id, 'hello word', reply_to_message_id=msg['message_id'])
