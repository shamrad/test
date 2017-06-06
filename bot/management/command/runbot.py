from datetime import datetime, timedelta, sys

import asyncio
from mimetypes import init

import telepot
from aiohttp import web
from django.core.management import BaseCommand
from telepot.delegate import pave_event_space, per_chat_id, create_open,  include_callback_query_chat_id
from bot.models import TeleUser,Word
from bot.form import TeleUserForm, WordForm
from telepot.namedtuple import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import Q
import random
from telepot.aio.loop import OrderedWebhook
TOKEN='333028480:AAG2EAmXyBfGqV4XYyD7iD7EEZnd6zvil78'


class Start(telepot.helper.ChatHandler):
    def __init__(self ,*args, **kwargs):
        super(Start, self).__init__(*args, **kwargs)
        self._id = 0
        self._answer = None
        self._answer_id=None
        self._score=0
        self._message_ind=None
        self._delete=0
        self._message_ind_delet=None

# state = 1  start
# state = 2  sabte loghat
# state = 3  sabte mani
# state = 4  liste loghat ha
# state = 5  moror



    def on_chat_message(self, msg):
        from_id = msg['from']['id']
        # self._sender.sendMessage(from_id)
        user=TeleUser.objects.filter(user_id=from_id)
        if user:
            a = TeleUser.objects.get(user_id=from_id)
            key1 = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='ثبت لغت جدید ✍🏻'), KeyboardButton(text='مرور لغت ها 🔎')],
                          [KeyboardButton(text='لیست لغت های ثبت شده📝'), KeyboardButton(text='معرفی به دوستان❣️')]],
                resize_keyboard=True, one_time_keyboard=True)
            if msg['text']=='/back':
                a.state = 1
                a.save()
                self.sender.sendMessage('یکی از گزینه های زیر را انتخاب کنید', reply_markup=key1)

            else:

                if a.state==1:
                    if msg['text']=='ثبت لغت جدید ✍🏻':
                        a.state =2
                        a.save()
                        self.sender.sendMessage('لغت مورد نظر را وارد کنید. /back',reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    elif msg['text']=='مرور لغت ها 🔎':
                        wordscount = Word.objects.filter(teleuser=a).count()
                        review= Word.objects.filter(teleuser=a).filter(
                            Q(next_review_time__lte=datetime.now()) | Q(next_review_time=None)).count()
                        memory=wordscount-review

                        key2=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text=' مرور لغت ها', callback_data='shoro')],[InlineKeyboardButton(text='بازگشت به منوی اصلی', callback_data='end')
                         ]])

                        text='📉 \n شما  {count}  لغت ثبت کرده اید✒️ \n \n {review} لغت برای مرور دارید!💡\n \n  و موفق به حفظ  {mem}  لغت شده اید.📌\n \n .'.format(mem=memory,count=wordscount,review=review)
                        send=self.sender.sendMessage(text,reply_markup=key2)
                        self._id=msg['from']['id']

                        self._message_ind=telepot.message_identifier(send)

                    elif msg['text']=='لیست لغت های ثبت شده📝':
                        list=Word.objects.filter(teleuser=a.pk)
                        n=0
                        for i in list:
                            n=n+1
                            text = '{count}- {word} '.format(count=n,word=i.word)
                            key= InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='جزییات مرور 🔎', callback_data=str(i.pk))]])
                            self.sender.sendMessage(text,reply_markup=key)

                        a.state=4
                        a.save()
                    elif msg['text']=='معرفی به دوستان❣️':
                        self.sender.sendMessage('معرفی کن دیگه')

                    else:
                        self.sender.sendMessage('یکی از گزینه های زیر را انتخاب کنید', reply_markup=key1)
                        a.state=1
                        a.save()

                elif a.state==2:
                    form = WordForm(data={
                        'word': msg['text'],
                        'teleuser': a.pk,
                    })
                    if form.is_valid():
                        form.save()
                        self.sender.sendMessage('معنی این لغت را وارد کنید', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        a.state=3
                        a.save()
                    else:
                        self.sender.sendMessage(form.errors)

                elif a.state == 3:
                    word = Word.objects.filter(teleuser=a).last()
                    if word.meaning:
                        text='معنی این لغت را قبلا ثبت کرده اید: {mani}'.format(mani=word.meaning)
                        self.sender.sendMessage(text, reply_markup=key1)
                    else:
                        word.meaning=msg['text']
                        word.save()
                        a.state=2
                        a.save()
                        self.sender.sendMessage('لغت ثبت شد، برای ادامه لغت بعدی را ثبت کنید یا /back به منوی اصلی')
                elif a.state==5:
                    a.state = 1
                    a.save()
                    self.close()

                else:
                    self.sender.sendMessage('یکی از گزینه های زیر را انتخاب کنید', reply_markup=key1)
                    a.state=1
                    a.save()



        else:

            form = TeleUserForm(data={
                # 'user_name': msg['from']['username'],
                'user_id': from_id,
                # 'first_name': msg['from']['first_name'],
                'state': 1,
            })
            if form.is_valid():
                form.save()
                key1 = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text='ثبت لغت جدید')]],
                    resize_keyboard=True)
                self.sender.sendMessage('برای ثبت لغت جدید دکمه ثبت را انتخاب کنید',reply_markup=key1)
            else:
                self.sender.sendMessage(form.errors)


    def _show_next_question(self,msg):

        chat_id=telepot.glance(msg, flavor='callback_query')

        a = TeleUser.objects.get(user_id=msg['from']['id'])
        words=Word.objects.filter(teleuser=a).filter(Q(next_review_time__lte=datetime.now())|Q(next_review_time=None)).order_by('-next_review_time').last()
        if words:
            choice=Word.objects.filter(teleuser=a).exclude(pk=words.pk).order_by('?').all()[:3]
            list=[]
            for i in choice:
                list.append(i)
            answer=words.pk
            list.append(words)
            random.shuffle(list)
            question = '{word} ❓ \n\n' \
                       '1️⃣- {one} \n\n' \
                       '2️⃣- {two} \n\n' \
                       '3️⃣- {three} \n\n' \
                       '4️⃣- {four} \n\n'.format(word=words.word,one=list[0].meaning,two=list[1].meaning,three=list[2].meaning,four=list[3].meaning)

            key3 = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=str(1), callback_data=str(list[0].pk)),InlineKeyboardButton(text=str(2), callback_data=str(list[1].pk)),
                InlineKeyboardButton(text=str(3), callback_data=str(list[3].pk)),InlineKeyboardButton(text=str(4), callback_data=str(list[2].pk))
                ]])

            new=bot.editMessageText(msg_identifier=self._message_ind,text=question,reply_markup=key3)

            self._message_ind=telepot.message_identifier(new)

        else:
            self.sender.sendMessage('هیچ لغتی برای مرور موجود نیست')

        return answer


    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        a = TeleUser.objects.get(user_id=msg['from']['id'])
        if a.state==4:
            if query_data=='delete':
                deleteword=Word.objects.get(pk=self._delete).delete()
                bot.editMessageReplyMarkup(msg_identifier=self._message_ind_delet,reply_markup=None)
                bot.answerCallbackQuery(query_id, text=' لغط خذف شد ')

            else:
                edit=Word.objects.get(pk=query_data)
                text='کلمه : {word}\n\n معنی : {means}\n\n ✅تعداد پاسخ صحیح : {sahih}\n \n ❌تعداد پاسخ غلط : {ghalat}\n \n ⏳زمان تکرار بعدی : {time}\n ..'.format(word=edit.word,
                                                         means=edit.meaning,sahih=edit.correct_answer,
                                                         ghalat=edit.wrong_answer,time=edit.next_review_time)

                key = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='حذف این لغت', callback_data='delete')]])
                detail=self.sender.sendMessage(text,reply_markup=key)
                if self._message_ind_delet:
                    bot.editMessageReplyMarkup(msg_identifier=self._message_ind_delet,reply_markup=None)
                    self._message_ind_delet=telepot.message_identifier(detail)
                else:
                    self._message_ind_delet = telepot.message_identifier(detail)
                self._delete=edit.pk


        else:
            if query_data == 'shoro':
                count=Word.objects.filter(teleuser=a).count()
                if count>3:
                    bot.answerCallbackQuery(query_id, text='برای هر سوال 60 ثانیه وقت دارید')
                    a.state=5
                    a.save()
                    self._answer = self._show_next_question(msg=msg)
                else:
                    self.sender.sendMessage('برای شروع فرایند مرور باید حداقل 4 کلمه وارد کنید \n یکی از گزینه های زیر را انتخاب کنید ')
                    a.state=1
                    a.save()

            elif query_data == 'end':
                a.state=1
                a.save()
                key1 = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text='ثبت لغت جدید ✍🏻'), KeyboardButton(text='مرور لغت ها 🔎')],
                              [KeyboardButton(text='لیست لغت های ثبت شده📝'),
                               KeyboardButton(text='معرفی به دوستان❣️')]],
                    resize_keyboard=True, one_time_keyboard=True)
                self.sender.sendMessage('برای ادامه یکی از گزینه ها را انتخاب کنید', reply_markup=key1)
                self.close()

            elif query_data== str(self._answer):
                days=[1,1,2,5,10,20,40]
                bot.answerCallbackQuery(query_id, text=' درسته ')

                id=self._answer

                word=Word.objects.get(id=id)
                i=word.level
                if i<7:
                    word.next_review_time=datetime.now()+timedelta(days=days[i])
                else:
                    word.next_review_time = datetime.now() + timedelta(days=40)

                self._score= self._score+5
                word.level = word.level + 1
                word.correct_answer=word.correct_answer+1
                word.save()
                a.points=a.points+5
                a.save()
                self._answer = self._show_next_question(msg=msg)

            else:
                if self._answer==None:

                    key1 = ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text='ثبت لغت جدید ✍🏻'), KeyboardButton(text='مرور لغت ها 🔎')],
                                  [KeyboardButton(text='لیست لغت های ثبت شده📝'),
                                   KeyboardButton(text='معرفی به دوستان❣️')]],
                        resize_keyboard=True, one_time_keyboard=True)
                    self.sender.sendMessage('برای شروع مجدد یکی از گزینه های زیر را انتخاب کنید',reply_markup=key1)
                    a.state=1
                    a.save()
                else:
                    id = self._answer
                    word = Word.objects.get(id=id)
                    word.level=0
                    word.wrong_answer=word.wrong_answer+1
                    word.save()
                    bot.answerCallbackQuery(query_id, text='ghalat')
                    self._answer = self._show_next_question(msg=msg)

    def on__idle(self, event):
        from_id=event['_idle']['source']['id']
        a=TeleUser.objects.get(user_id=from_id)

        key1 = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='ثبت لغت جدید ✍🏻'), KeyboardButton(text='مرور لغت ها 🔎')],
                      [KeyboardButton(text='لیست لغت های ثبت شده📝'), KeyboardButton(text='معرفی به دوستان❣️')]],
            resize_keyboard=True, one_time_keyboard=True)
        if a.state==5:
            a.state=1
            a.save()
            self.sender.sendMessage('زمان شما به پایان رسید.',reply_markup=key1)
            self._answer=None
            self.close()
        else:
            pass

    def on_close(self, ex):
        if self._message_ind:
            key1 = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='ثبت لغت جدید ✍🏻'), KeyboardButton(text='مرور لغت ها 🔎')],
                          [KeyboardButton(text='لیست لغت های ثبت شده📝'), KeyboardButton(text='معرفی به دوستان❣️')]],
                resize_keyboard=True, one_time_keyboard=True)
            text='score: {score}'.format(score=self._score)
            self.sender.sendMessage(text,reply_markup=key1)
            bot.editMessageReplyMarkup(msg_identifier=self._message_ind,reply_markup=None)
        else:
            pass


PORT = 9080



loop = asyncio.get_event_loop()
app = web.Application(loop=loop)

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
    pave_event_space())(per_chat_id(), create_open, Start, timeout=60),

])

webhook = OrderedWebhook(bot)
# bot.message_loop(run_forever='Listening ...')


loop.run_until_complete(init(app, bot))

loop.create_task(webhook.run_forever())

class Command(BaseCommand):
    try:
        web.run_app(app, port=PORT)
    except KeyboardInterrupt:
        pass
