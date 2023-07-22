#1 Создаем пользователей
from django.contrib.auth.models import User

user=User.objects.create_user('User1', password='User1')
user=User.objects.create_user('User2', password='User2')
user.is_superuser=False
user.is_staff=False
user.save()

#2 Создаем два объекта модели Author связанные с пользователями
from news.models import *
User.objects.all()
#  В выводе получаю: <QuerySet [<User: admin>, <User: User1>, <User: User2>]>
u1 = User.objects.get(username='User1')
Author.objects.create(user=u1, rating='1')
#  В выводе получаю: <Author: Author object (1)>
u1.save()

u2 = User.objects.get(username='User2')
Author.objects.create(user=u2, rating='2')
#  В выводе получаю: <Author: Author object (2)>
u2.save()


#3 Добавляем 4 категории
from news.models import Category
category_1 = Category.objects.create(category_name='Наука')
category_2 = Category.objects.create(category_name='Технологии')
category_3 = Category.objects.create(category_name='Обо всем')
category_4 = Category.objects.create(category_name='Спорт')


#4 Добавляем 2 статьи и 1 новость
from news.models import *
post_news = Post.objects.create(author=Author.objects.get(pk=1), title='о фейках', text='В Москве заочно арестованы двое граждан Венесуэлы по делу о распространении фейков о ВС РФ', choice='news')
post_art_1 = Post.objects.create(author=Author.objects.get(pk=1), title='Выводы ученых о АКБ', text='Исследователи определили, откуда у твердотельных литиевых аккумуляторов растут дендриты', choice='articles')
post_art_2 = Post.objects.create(author=Author.objects.get(pk=2), title='«Спартак»', text='«Спартак» намерен совершить крупный трансфер', choice='articles')
post_news_2 = Post.objects.create(author=Author.objects.get(pk=2), title='угроза вторжения Китая на Тайвань', text='Потенциальная угроза вторжения Китая на Тайвань стала помехой единству стран G7 (объединяет Великобританию, Германию, Италию, Канаду, Францию, Японию и США) на саммите в Хиросиме, который пройдет с 19 по 21 мая', choice='news')

#5 Присвоим им категории (в одной статье сделаем 2 категории).
from news.models import *
category_1 = Category.objects.all()[0]
category_2 = Category.objects.all()[1]
category_3 = Category.objects.all()[2]
category_4 = Category.objects.all()[3]
post_news.category.add(category_3)
post_art_1.category.add(category_1, category_2)
post_art_2.category.add(category_3, category_4)
post_news_2.category.add(category_3)

#6 Создаем 4 комментария к разным объектам Post
from news.models import Comment
post_news = Post.objects.get(pk=1)
comment_1 = Comment.objects.create(comment_user=User.objects.get(pk=3), comment_post=post_news,comment_text='Требую повысить следователя!')
post_news = Post.objects.get(pk=4)
comment_2 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_news, comment_text='Очень интересно')
post_art_1 = Post.objects.get(pk=2)
comment_3 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_art_1, comment_text='Прикуплю себе пару')
post_art_2 = Post.objects.get(pk=3)
comment_4 = Comment.objects.create(comment_user=User.objects.get(pk=2), comment_post=post_art_2, comment_text='Главное чтобы играть умел, а не как обычно')
post_news_2 = Post.objects.get(pk=4)
comment_5 = Comment.objects.create(comment_user=User.objects.get(pk=2), comment_post=post_news_2, comment_text='Во живем')


#7 Применю like и dislike к статьям/новостям и комментариям, корректирую их рейтинги
post_news.like()
post_news.like()
post_news.like()
post_art_1.like()
post_art_2.like()
post_art_2.like()
post_news.like()
comment_1.like()
comment_3.dislike()
comment_4.dislike()
post_art_1.like()
post_news_2.dislike()
post_news_2.dislike()
post_news_2.like()
post_art_1.like()

#8 Обновляю рейтинги для  авторов статей
author_1 = Author.objects.get(pk=1)
author_1.update_rating()

author_2 = Author.objects.get(pk=2)
author_2.update_rating()

#9 Вывожу имя и рейтинг лучшего пользователя (применяя сортировку)
Author.objects.all().order_by('-rating').values('user__username', 'rating').first()
#  В выводе получаю: {'user__username': 'User1', 'rating': 8}

#10 Вывожу дату добавления, имя автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках и дизлайках.
best_post = Post.objects.all().order_by('-post_rating').first()
best_post_data = Post.objects.all().order_by('-post_rating').values('posting_time', 'author__user__username', 'post_rating', 'title').first()
best_post_preview = Post.objects.all().order_by('-post_rating').first().preview()
best_post_preview
#  В выводе получаю: 'Исследователи определили, откуда у твердотельных литиевых аккумуляторов растут дендриты...'

#11 Вывожу все комментарии (дата, пользователь, рейтинг, текст) к лучшей статье.
comments = Comment.objects.filter(comment_post=best_post).values('comment_date', 'comment_user', 'comment_rating', 'comment_text')
comments
#  В выводе получаю: <QuerySet [{'comment_date': None, 'comment_user': 1, 'comment_rating': -1, 'comment_text': 'Прикуплю себе пару'}]>
