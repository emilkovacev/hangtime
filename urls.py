from crablib.http.path import Path
import views


urls = [
    Path('^/$', views.index),
    Path('^/yoshi$', views.yoshi),
    Path('^\\/(images\\/[^.]+\\.(jpg|jpeg))$', views.img),
    Path('^\\/(style\\/[^.]+\\.css)$', views.css),
    Path('^\\/(script\\/[^.]+\\.js)$', views.js),
    Path('^/(images\\?[^?]+)$', views.images),
    Path('^/comment$', views.form),
]
