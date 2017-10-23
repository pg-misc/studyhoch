import requests
import os
import unidecode
from pyquery import PyQuery as pq

def typable(s):
    # s = s.replace(u'ṯ', 'T')
    s = s.replace(u'ꜣ', '3')
    s = s.replace(u'ꜥ', 'a')
    # s = s.replace(u'ḥ', 'H')
    # s = s.replace(u'ḫ', 'x')
    # s = s.replace(u'ḏ', 'D')
    # s = s.replace(u'ẖ', 'X')
    # s = s.replace(u'š', 'S')
    return unidecode.unidecode(s)

count = 0
with open('index.html', 'w') as index:
    print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>All Lessons</title>\n</head>\n<body>', file=index)
    print('<h3><u>Flashcard Instructions</u></h3><h4>Space bar = flip flashcard<br/>\nRight arrow key = next flashcard<br/>\nLeft arrow key = previous flashcard<br/>\nDelete/backspace = restart lesson<br/>\nEscape = return to list of lessons</h4>', file=index)
    print('<a href="full_list.html">Full List of Terms</a>\n<br/>', file=index)
    with open('full_list.html', 'w') as full_list:
        print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Full Term List</title>\n</head>\n<body>', file=full_list)
        print('<h4>For "typable transliterations", all accents are stripped. "ꜥ" is transliterated to "a" and "ꜣ" is transliterated to "3"</h4>\n</br>', file=full_list)
        for i in range(1, 23, 2):
            count += 1
            print('<a href="lesson_{}/1.html">Lesson {}</a>\n<br/>'.format(count, count), file=index)
            if not os.path.exists('lesson_{}'.format(count)):
                os.makedirs('lesson_{}'.format(count))
            h_html = requests.get('https://www.memrise.com/course/771953/middle-egyptian-hoch-hieroglyphs/{}'.format(i))
            hdoc = pq(h_html.content)
            t_html = requests.get('https://www.memrise.com/course/771953/middle-egyptian-hoch-hieroglyphs/{}'.format(i + 1))
            tdoc = pq(t_html.content)

            hieroglyphs = [thing for thing in hdoc('div').items() if str(thing('div').attr('class')) == 'thing text-image']
            transliterations = [thing for thing in tdoc('div').items() if str(thing('div').attr('class')) == 'thing text-text']

            vocab = list(zip(hieroglyphs, transliterations))

            for c, v in enumerate(vocab):
                c = c + 1
                h, t = v
                with open('lesson_{}/{}.html'.format(count, c), 'w') as out:
                    print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Lesson {} #{}</title>\n<link rel="stylesheet" href="../style.css">\n<script src="http://code.jquery.com/jquery-latest.min.js"></script>\n<script src="../app.js"></script>\n</head>\n<body>'.format(count, c), file=out)
                    print('<h4>\nSpace bar = flip flashcard<br/>\nRight arrow key = next flashcard<br/>\nLeft arrow key = previous flashcard<br/>\nDelete/backspace = restart lesson<br/>\nEscape = return to list of lessons</h4>', file=out)
                    print('<div class="stage">\n<div class="flashcard">\n<div class="front">', file=out)
                    imgurl = h('div.image')('img').attr('src')
                    if not os.path.exists('lesson_{}/images'.format(count)):
                        os.makedirs('lesson_{}/images'.format(count))
                    imgloc = 'lesson_{}/images/{}.{}'.format(count, c, imgurl.split('.')[-1])
                    if not os.path.exists(imgloc):
                        with open(imgloc, 'wb') as img:
                            img.write(requests.get(imgurl).content)
                    print('<img src="../{}">'.format(imgloc), file=out)
                    print('<img src="{}">'.format(imgloc), file=full_list)
                    print('<br/>', file=full_list)
                    print('</div>\n<div class="back">', file=out)
                    print('<strong>Transliteration: </strong>', file=out)
                    print(t('div.col_a.col.text').text(), file=out)
                    print('<strong>Transliteration: </strong>', file=full_list)
                    print(t('div.col_a.col.text').text(), file=full_list)
                    print('<br/>', file=full_list)
                    print('<strong>Typable Transliteration: </strong>', file=full_list)
                    print(typable(t('div.col_a.col.text').text()), file=full_list)
                    print('<br/>', file=out)
                    print('<br/>', file=full_list)
                    print('<strong>Definition: </strong>', file=out)
                    print(h.text(), file=out)
                    print('<strong>Definition: </strong>', file=full_list)
                    print(h.text(), file=full_list)
                    print('</div>\n</div>\n</div>', file=out)
                    print('<br/>', file=full_list)
                    print('<br/>', file=full_list)
                    if c != len(vocab):
                        print('<br/>\n<a id="next" href="{}.html">Next Card</a>'.format(c + 1), file=out)
                    if c != 1:
                        print('<br/>\n<a id="previous" href="{}.html">Previous Card</a>'.format(c - 1), file=out)
                    print('<br/>\n<a id="restart" href="1.html">Start Lesson Over</a>', file=out)
                    print('<br/>\n<a id="index" href="../index.html">All Lessons</a>'.format(c - 1), file=out)
                    print('</body>\n</html>', file=out)
        print('<br/><p>Flashcard HTML/CSS/JavaScript slightly modified from <a href="http://codrspace.com/kara/implementing-flashcard-flip-with-css3-transitions/">http://codrspace.com/kara/implementing-flashcard-flip-with-css3-transitions/</a></p>', file=index)
        print('<br/><p>Vocabulary scraped from <a href="https://www.memrise.com/course/771953/middle-egyptian-hoch-hieroglyphs/">memrise</a></p>', file=index)
        print('</body>\n</html>', file=index)
        print('</body>\n</html>', file=full_list)
