import os
import jpype
from flask import Flask, request, g, jsonify


class DefaultSettings(object):
    DEBUG = False
    TESTING = False
    CONVERT_PATH = '/usr/bin/convert'
    IDENTIFY_PATH = '/usr/bin/identify'
    IMAGE_MIN_BYTES = 4500
    HOST = "0.0.0.0"
    PORT = 5000

app = Flask(__name__)
app.config.from_object('application.DefaultSettings')
app.config.from_pyfile('application.cfg', silent=True)


@app.before_first_request
def init_jpype():
    build_dir = os.path.join(
        os.path.abspath(os.path.split(__file__)[0]),
        'build'
    )
    jpath = jpype.getDefaultJVMPath()
    jpype.startJVM(jpath, "-ea", "-Djava.ext.dirs=%s" % build_dir)


@app.before_request
def init_goose():
    Configuration = jpype.JClass('com.gravity.goose.Configuration')
    c = Configuration()
    c.setMinBytesForImages(app.config['IMAGE_MIN_BYTES'])
    c.setLocalStoragePath("/tmp/goose")
    c.setEnableImageFetching(True)
    c.setImagemagickConvertPath(app.config['CONVERT_PATH'])
    c.setImagemagickIdentifyPath(app.config['IDENTIFY_PATH'])
    g.goose = jpype.JPackage('com').gravity.goose.Goose(c)


@app.route("/")
def get_url():
    url = request.args['url']
    article = g.goose.extractContent(url)
    result = {
        'title': article.title(),
        'meta_description': article.metaDescription(),
        'meta_keywords': article.metaKeywords(),
        'canonical_link': article.canonicalLink(),
        'domain': article.domain(),
        'publish_date': article.publishDate(),
        'top_image': article.topImage().imageSrc,
        'content': article.cleanedArticleText(),
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])
