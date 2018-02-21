import requests
import os
import unidecode
from pyquery import PyQuery as pq

count = 0
with open('index.html', 'w') as index:
    print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>All Lessons</title>\n</head>\n<body>', file=index)
    print('<h3><u>Flashcard Instructions</u></h3><h4>Space bar = flip flashcard<br/>\nRight arrow key = next flashcard<br/>\nLeft arrow key = previous flashcard<br/>\nDelete/backspace = restart lesson<br/>\nEscape = return to list of lessons</h4>', file=index)
    print('<a href="full_list.html">Full List of Terms</a>\n<br/>', file=index)
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
                print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Lesson {} #{}</title>\n<link rel="stylesheet" href="../style_1.0.css">\n<script src="https://code.jquery.com/jquery-latest.min.js"></script>\n<script src="../app.js"></script>\n</head>\n<body>'.format(count, c), file=out)
                print('<h4>\nSpace bar = flip flashcard<br/>\nRight arrow key = next flashcard<br/>\nLeft arrow key = previous flashcard<br/>\nDelete/backspace = restart lesson<br/>\nEscape = return to list of lessons</h4>', file=out)
                print('<div class="stage">\n<div class="flashcard">\n<div class="front"><p>', file=out)
                imgurl = h('div.image')('img').attr('src')
                if not os.path.exists('lesson_{}/images'.format(count)):
                    os.makedirs('lesson_{}/images'.format(count))
                imgloc = 'lesson_{}/images/{}.{}'.format(count, c, imgurl.split('.')[-1])
                if not os.path.exists(imgloc):
                    with open(imgloc, 'wb') as img:
                        img.write(requests.get(imgurl).content)
                print('<img src="../{}">'.format(imgloc), file=out)
                print('</p></div>\n<div class="back"><p>', file=out)
                print('<strong>Transliteration: </strong>', file=out)
                print(t('div.col_a.col.text').text(), file=out)
                print('<br/>', file=out)
                print('<strong>Definition: </strong>', file=out)
                print(h.text(), file=out)
                print('</p>\n</div>\n</div>\n</div>', file=out)
                if c != len(vocab):
                    print('<br/>\n<a id="next" href="{}.html">Next Card</a>'.format(c + 1), file=out)
                if c != 1:
                    print('<br/>\n<a id="previous" href="{}.html">Previous Card</a>'.format(c - 1), file=out)
                print('<br/>\n<a id="restart" href="1.html">Start Lesson Over</a>', file=out)
                print('<br/>\n<a id="index" href="../index.html">All Lessons</a>'.format(c - 1), file=out)
                print('</body>\n</html>', file=out)
    for i in range(2):
        count += 1
        print('<a href="lesson_{}/1.html">Lesson {}</a>\n<br/>'.format(count, count), file=index)

        for c in range(len([img for img in os.listdir('lesson_{}/hieroglyphs'.format(count)) if img.split('.')[-1] == 'png'])):
            c = c + 1
            h, t = v
            with open('lesson_{}/{}.html'.format(count, c), 'w') as out:
                print('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Lesson {} #{}</title>\n<link rel="stylesheet" href="../style_1.0.css">\n<script src="https://code.jquery.com/jquery-latest.min.js"></script>\n<script src="../app.js"></script>\n</head>\n<body>'.format(count, c), file=out)
                print('<h4>\nSpace bar = flip flashcard<br/>\nRight arrow key = next flashcard<br/>\nLeft arrow key = previous flashcard<br/>\nDelete/backspace = restart lesson<br/>\nEscape = return to list of lessons</h4>', file=out)
                print('<div class="stage">\n<div class="flashcard">\n<div class="front"><p>', file=out)
                
                print('<img src="../{}" style="max-width:100%;max-height:100%;">'.format('lesson_{}/hieroglyphs/{}.png'.format(count, c)), file=out)
                print('</p></div>\n<div class="back"><p>', file=out)
                print('<img src="../{}" style="max-width:100%;max-height:100%;">'.format('lesson_{}/translations/{}.png'.format(count, c)), file=out)
                print('</p>\n</div>\n</div>\n</div>', file=out)
                if c != len(vocab):
                    print('<br/>\n<a id="next" href="{}.html">Next Card</a>'.format(c + 1), file=out)
                if c != 1:
                    print('<br/>\n<a id="previous" href="{}.html">Previous Card</a>'.format(c - 1), file=out)
                print('<br/>\n<a id="restart" href="1.html">Start Lesson Over</a>', file=out)
                print('<br/>\n<a id="index" href="../index.html">All Lessons</a>'.format(c - 1), file=out)
                print('</body>\n</html>', file=out)
    print('<br/><p>Flashcard HTML/CSS/JavaScript adapted from <a href="http://codrspace.com/kara/implementing-flashcard-flip-with-css3-transitions/">http://codrspace.com/kara/implementing-flashcard-flip-with-css3-transitions/</a></p>', file=index)
    print('<br/><p>Vocabulary scraped from <a href="https://www.memrise.com/course/771953/middle-egyptian-hoch-hieroglyphs/">memrise</a></p>', file=index)
    print('</body>\n</html>', file=index)