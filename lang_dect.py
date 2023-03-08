from polyglot.detect import Detector
from polyglot.text import Text
from polyglot.downloader import downloader
# example of langage text detection
print(downloader.supported_languages_table("sentiment2", 3))
sample_text = '''Pour le moment, ce que je vois me semble remarquable. Donc félicitations aux concepteurs.'''
text = Text(sample_text)
print(text.polarity)

