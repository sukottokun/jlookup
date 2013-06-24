jlookup
=======

Japanese lookup tools

Often I have a news article or blog post with a bunch of words I don't know. Most of what I want are the Kanji and the verb stem, the corresponding hiragana, and the most common meaning.

This python script reads the article and using the most excellent Tiny Segmenter ( http://chasen.org/~taku/software/TinySegmenter/ ) parses each verb and kanji compound. Then it pulls the first, most common definition from Jim Breen's wwwjdic dictionary ( http://www.csse.monash.edu.au/~jwb/wwwjdicinf.html ). It spits it all out onto a text file.

Pretty basic. At some point it might be nice to make furigana an option. But I pretty much learn the words, then go back and read the article when I am studying.
