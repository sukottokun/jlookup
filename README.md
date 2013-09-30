jlookup
=======

Japanese lookup tools

Often I have a news article or blog post with a bunch of words I don't know. Most of what I want are the Kanji and the verb stem, the corresponding hiragana, and the most common meaning.

This python script reads the article and using the most excellent Tiny Segmenter ( http://chasen.org/~taku/software/TinySegmenter/ ) parses each verb and kanji compound. Then it pulls the first, most common definition from Jim Breen's wwwjdic dictionary ( http://www.csse.monash.edu.au/~jwb/wwwjdicinf.html ). It spits it all out onto a text file.

Pretty basic. At some point it might be nice to make furigana an option. But I pretty much learn the words, then go back and read the article when I am studying.

TODOS:
[ ] Add goo, other alternative dictionaries: http://search.goo.ne.jp/web.jsp?MT=%s

[ ] Return non-jisho kei verbs better

[ ] Skip writing redundant exact matches

[ ] Show total tokens, show token progress

[ ] Tiny segmenter alternatives?

[ ] Step forward and back while building the search list

[ ] Lookup hiragana too

[ ] Review, edit known kanji

[ ] IN PROGRESS: Use a database, make Japanese work

[ ] Read a word doc as input

[ ] Maybe put on the web
