from multiprocessing import context
from operator import le
from django.shortcuts import render
from django.http import HttpResponse
from .models import data_Russian, data_output
import re
from prompt_toolkit import HTML


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


# Create your views here.
def search_view(request):
    print(request.GET)
    index_final = 0
    doc_list = []
    pre_list = []
    key_list = []
    post_list = []
    para_list = []
    context = {}
    obj = data_Russian.objects.all()
    obj2 = data_output.objects.all()
    if 'search1' in request.POST:
        print(request.POST)
        # search_text = request.POST.get('search_text')
        # try:
        #     words = request.POST.get('words')
        #     words = int(words)
        # except ValueError:
        #     print('')
        # for i in range(len(obj)):
        #     id = list(obj.values_list('id', flat=True))[i]
        #     text = list(obj.values_list('text', flat=True))[i]
        #     if findWholeWord(search_text)(text) != None:
        #         pre = ''
        #         post = ''
                # print(text)
            # list_one = re.split('(\W+?)', text)
            # empty = ['', ' ', '  ']
            # list_one = [el for el in list_one if el not in empty]
            # print(list_one)
            # pre = ''
            # post = ''
            # for i in range(len(list_one)):
            #     if list_one[i] == search_text:
            #         index_final = i
            #     else:
            #         continue
            #     pre_start = index_final-1
            #     pos_start = index_final + words
            #     try:
            #         if len(list_one) > words:
            #             for i in range(words):
            #                 if pre_start >= 0:
            #                     pre = list_one[pre_start]  + ' ' + pre
            #                     pre_start -= 1
            #                 else:
            #                     break
            #             for i in range(words):
            #                 if pos_start < len(list_one):
            #                     post = list_one[pos_start] + ' ' + post
            #                     pos_start -= 1
            #                 else:
            #                     break
            #         else:
            #             break
            #     except IndexError:
            #         continue
                # doc_list.append(id)
                # pre_list.append(pre)
                # key_list.append(search_text)
                # post_list.append(post)
                # para_list.append(text)

        content = [{'id' : id,'search_word' : key,'pre':pre,'post':post,'text' :para} for id, key, pre, post, para in zip(doc_list, key_list, pre_list, post_list, para_list)]
        context = {
            "content" : content
        }
    elif 'search2' in request.POST:
        first_list = []
        second_list = []
        final = []
        firstpart = []
        secondpart = []
        thirdpart = []
        print(request.POST)
        first_word = request.POST.get('search_text1')
        second_word = request.POST.get('search_text2')
        try:
            space = request.POST.get('space')
            space = int(space) + 1
        except ValueError:
            print('')
        olemma = list(obj2.values_list('Text_Lemma', flat=True))
        opos = list(obj2.values_list('Only_POS', flat=True))
        id = list(obj.values_list('id', flat=True))
        for num in range(len(olemma)):
            o_pos = opos[num].split(' ')
            index_of_punc = []
            for i in range(len(o_pos)):
                if o_pos[i] == 'PUNCT':
                    index_of_punc.append(i)

            o_test = olemma[num].split(' ')
            for i in range(len(o_test)):
                for j in index_of_punc:
                    if i == j:
                        o_test[i - 1] = o_test[i - 1] + o_test[i]
                        o_test[i] = ''
            for i in o_test:
                if i == '':
                    o_test.remove(i)
            list_one = []
            list_two = []
            for i in range(len(o_test)):
                if first_word in o_test[i]:
                    list_one.append(i)
            for j in range(len(o_test)):
                if second_word in o_test[j]:
                    list_two.append(j)
            ans = []
            for i in list_one:
                for j in list_two:
                    if i - j == space or j - i == space:
                        list_three = []
                        list_three.append(i)
                        list_three.append(j)
                        list_three = sorted(list_three)
                        if list_three not in ans:
                            ans.append(list_three)
            if len(ans) != 0:
                print(ans)
                for i in ans:
                    o_test_first = o_test[0:i[0]]
                    o_test_sec = o_test[i[0] + 1: i[1]]
                    o_test_third = o_test[i[1] + 1 :len(o_test)]
                sen = ''
                for a in o_test_first:
                    sen = sen + a + ' '
                firstpart.append(sen)
                sen = ''
                for b in o_test_sec:
                    sen = sen + b + ' '
                secondpart.append(sen)
                sen = ''
                for c in o_test_third:
                    sen = sen + c + ' '
                thirdpart.append(sen)
                first_list.append(first_word)
                second_list.append(second_word)
                for i in ans:
                    final.append(id[num])
        content = [{'id':id,'first' : first,'second' : second,'text_1':text1, 'text_2':text2, 'text_3':text3} for id, first, second, text1 , text2 ,text3 in zip(final, first_list, second_list, firstpart, secondpart, thirdpart)]
        context = {
            "content" : content
        }
        # for i in final:
        #     print(i)
    elif 'search3' in request.POST:
        print(request.POST)
        opos = list(obj2.values_list('Only_POS', flat=True))
        otext = list(obj2.values_list('text', flat=True))
        first_list_pos = []
        second_list_pos = []
        final = []
        ans = []
        first_pos = request.POST.get('first_pos')
        second_pos = request.POST.get('second_pos')
        id = list(obj.values_list('id', flat=True))
        try:
            space = request.POST.get('space2')
            space = int(space) + 1
        except ValueError:
            print('')
        # 開始進入迴圈
        for num in range(len(opos)):
        # for num in range(35):
        # 每筆資料先做切割
        #     print(num)
            opos_test = opos[num].split(' ')
            for i in opos_test:
                if i == '' or i == 'PUNCT':
                    opos_test.remove(i)
            try:
                # 找出在list當中第一次出現的順位
                first =  opos_test.index(first_pos)
            except ValueError as e:
                print('',end='')
            try:
                # 找出在list當中第一次出現的順位
                second = opos_test.index(second_pos)
            except ValueError as e:
                print('',end='')

            # 找出出現幾次
            countone = opos_test.count(first_pos)
            #找出出現幾次
            counttwo = opos_test.count(second_pos)

            value_one = []
            # 找出所有的序列
            for i in range(countone):
                value_one.append(first)
                try:
                    first = opos_test.index(first_pos, first + 1)
                except ValueError as e:
                    break
            value_two = []
            # 找出所有的序列
            for i in range(counttwo):
                value_two.append(second)
                try:
                    second = opos_test.index(second_pos, second + 1)
                except ValueError as e:
                    break
            sen = ''
            for a in value_one:
                for b in value_two:
                    if a - b == space or b - a == space:
                        otext_test = otext[num].split(" ")
                        try:
                            if otext_test[a].find(',') != -1 or otext_test[a].find('.') != -1:
                                beg = otext_test[a][:len(otext_test[a])-1]
                                end = otext_test[a][len(otext_test[a])-1:]
                                new = beg + '(' +opos_test[a] + ')' + end
                                otext_test[a] = new
                                beg = otext_test[b][:len(otext_test[b])-1]
                                end = otext_test[b][len(otext_test[b])-1:]
                                new = beg + '(' +opos_test[b] + ')' + end
                                otext_test[b] = new
                            else:
                                try:
                                    otext_test[a] = otext_test[a] + '(' + opos_test[a] + ')'
                                    otext_test[b] = otext_test[b] + '(' + opos_test[b] + ')'
                                except IndexError as e:
                                    print(num, "Out of bound.")
                                    break
                        except IndexError as e:
                            print(num, "Out of bound. Outside")
                            break
                        for c in otext_test:
            #                 print(c, end = ' ')
                            sen = sen + c + ' '
                        ans.append(sen)
                        sen = ''
                        first_list_pos.append(first_pos)
                        second_list_pos.append(second_pos)
                        final.append(id[num])
        content = [{'id2': id,'first_pos' : first,'second_pos' : second,'text3':text} for id, first, second, text in zip(final, first_list_pos, second_list_pos, ans)]
        context = {
            "content" : content
        }
        # for i in ans:
        #     print(i)
    return render(request, "search_one.html", context)
