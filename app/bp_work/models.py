# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 13:51
"""
import arrow

from app.db.model import BaseModel
from app.extensions import db


class Channel(db.Model, BaseModel):
    """文章专栏表"""

    __tablename__ = "mz_article_channel"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键
    name = db.Column(db.String(20), nullable=False)  # 专栏名称
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 专栏创建时间
    update_time = db.Column(db.BigInteger)  # 专栏最近一次的更新时间


class Category(db.Model, BaseModel):
    """文章分类表"""

    __tablename__ = "mz_article_category"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    name = db.Column(db.String(30), unique=True, nullable=False)  # 分类名称
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 分类创建时间
    update_time = db.Column(db.BigInteger)  # 分类最近一次的更新时间

    channel_id = db.Column(
        db.Integer, db.ForeignKey("mz_article_channel.id")
    )  # 文章专栏id，外键
    channel = db.relationship("Channel", backref=db.backref("categories"))  # 文章专栏

    @classmethod
    def query_by_channel(cls, channel_id: int) -> list or None:
        """根据文章专栏分页查询文章，

        :param channel_id: 文章专栏id
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return cls.query.filter(Category.channel_id == channel_id).all()


# 文章和标签是多对多的关系，需要有一张中间表来关联两者，这里官方文档建议使用 db.Table 来实现一个实际的表，不推荐使用模型来实现
article_re_tag = db.Table(
    "mz_article_re_tag",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, nullable=False),
    db.Column("article_id", db.Integer, db.ForeignKey("mz_article.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("mz_article_tag.id")),
)


class Article(db.Model, BaseModel):
    """文章表"""

    __tablename__ = "mz_article"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    title = db.Column(db.String(100), nullable=False)  # 标题
    cover_url = db.Column(db.String(255))  # 封面图片的url
    body = db.Column(db.Text, nullable=False)  # markdown格式的文章内容
    body_html = db.Column(db.Text, nullable=False)  # html格式的文章内容
    read_count = db.Column(db.Integer, default=0)  # 阅读量
    create_time = db.Column(
        db.BigInteger, nullable=False, index=True, default=arrow.utcnow().timestamp
    )  # 文章创建时间
    update_time = db.Column(db.BigInteger)  # 文章最近一次的更新时间
    status = db.Column(
        db.Integer, default=3
    )  # 文章状态  0-私密保存 1-发布审核中 2-审核未通过 3-审核通过 4-已被删除
    is_commentable = db.Column(db.Boolean, default=True)  # 是否可评论

    author_id = db.Column(
        db.Integer, db.ForeignKey("mz_user.id", ondelete="CASCADE"), nullable=False
    )  # 作者id，外键
    author = db.relationship(
        "User",
        backref=db.backref("articles", lazy="dynamic", cascade="all, delete-orphan"),
    )  # 作者，父级删除，子级跟着删除

    channel_id = db.Column(
        db.Integer, db.ForeignKey("mz_article_channel.id")
    )  # 文章专栏id，外键
    channel = db.relationship(
        "Channel",
        backref=db.backref("articles", lazy="dynamic", cascade="all, delete-orphan"),
    )  # 文章专栏

    category_id = db.Column(
        db.Integer, db.ForeignKey("mz_article_category.id")
    )  # 文章分类id，外键
    category = db.relationship(
        "Category",
        backref=db.backref("articles", lazy="dynamic", cascade="all, delete-orphan"),
    )  # 文章分类数据

    tags = db.relationship(
        "Tag", secondary=article_re_tag, backref=db.backref("articles", lazy="dynamic")
    )  # 标签列表

    @classmethod
    def query_private(cls, author_id: int, page: int, per_page: int):
        """分页查询私密文章，根据文章创建时间，降序排列

        :param author_id: 用户id
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return (
            cls.query.filter_by(author_id=author_id, status=0)
            .order_by(Article.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_order_by_createtime(cls, page: int, per_page: int):
        """分页查询文章，根据文章创建时间，降序排列

        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return (
            cls.query.filter_by(status=3)
            .order_by(Article.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_by_channel(cls, channel_id: int, page: int, per_page: int):
        """根据文章专栏分页查询文章，

        :param channel_id: 文章专栏id
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return (
            cls.query.filter_by(channel_id=channel_id, status=3)
            .order_by(Article.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_by_category(cls, category_id: int, page: int, per_page: int):
        """根据文章分类分页查询文章，

        :param category_id: 文章专栏id
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return (
            cls.query.filter_by(category_id=category_id, status=3)
            .order_by(Article.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_in_full_by_key(cls, keyword: str, page: int, per_page: int):
        """全文搜索

        :param keyword: 搜索关键词
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return (
            cls.query.filter(
                Article.title.like("%" + keyword + "%"),
                Article.body_html.like("%" + keyword + "%"),
            )
            .order_by(Article.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_pre(cls, article_id: int):
        """查询上一篇

        :param article_id: 当前文章id
        """
        return (
            cls.query.filter(Article.id < article_id)
            .order_by(Article.create_time.desc())
            .first()
        )

    @classmethod
    def query_next(cls, article_id: int):
        """查询下一篇

        :param article_id: 当前文章id
        """
        return (
            cls.query.filter(Article.id > article_id)
            .order_by(Article.create_time.asc())
            .first()
        )

    def increase_read_count(self):
        """增加文章阅读量"""
        self.read_count += 1
        db.session.commit()

    def modify_update_time(self):
        """修改文章更新时间"""
        self.update_time = arrow.utcnow().timestamp
        db.session.commit()


class Tag(db.Model, BaseModel):
    """文章标签表"""

    __tablename__ = "mz_article_tag"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    name = db.Column(db.String(30), nullable=False)  # 标签名称
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 标签创建时间

    @classmethod
    def query_by_name(cls, tag_name: str):
        """根据标签名查询文章标签"""
        return cls.query.filter_by(name=tag_name).first()

    def query_articles(self, page: int, per_page: int):
        """根据文章标签分页查询文章，

        :param tag_id: 文章标签id
        :param page: 当前的页码
        :param per_page: 每页的文章数
        """
        return self.articles.order_by(Article.create_time.desc()).paginate(
            page=page, per_page=per_page
        )  # 创建分页器对象


class Comment(db.Model, BaseModel):
    """文章评论表"""

    __tablename__ = "mz_article_comment"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    content = db.Column(db.Text)  # 评论内容
    comment_level = db.Column(db.Integer, nullable=False, default=1)  # 评论的等级，一共2级
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 评论创建时间
    status = db.Column(
        db.Integer, default=2
    )  # 评论状态  0-审核中 1-审核未通过 2-审核通过，未读 3-已读 4-已被删除，管理员可见

    article_id = db.Column(
        db.Integer, db.ForeignKey("mz_article.id", ondelete="CASCADE")
    )  # 文章id，外键
    article = db.relationship(
        "Article",
        backref=db.backref("comments", lazy="joined", cascade="all, delete-orphan"),
    )  # 评论所属文章

    from_uid = db.Column(
        db.Integer, db.ForeignKey("mz_user.id", ondelete="CASCADE")
    )  # 评论者id，外键
    from_user = db.relationship(
        "User",
        backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"),
        foreign_keys=[from_uid],
    )  # 评论人

    to_uid = db.Column(
        db.Integer, db.ForeignKey("mz_user.id", ondelete="CASCADE")
    )  # 被评论人id，外键
    to_user = db.relationship(
        "User",
        backref=db.backref(
            "received_comments", lazy="dynamic", cascade="all, delete-orphan"
        ),
        foreign_keys=[to_uid],
    )  # 被评论人

    parent_id = db.Column(
        db.Integer, db.ForeignKey("mz_article_comment.id", ondelete="CASCADE")
    )  # 父评论id，外键
    parent_comment = db.relationship(
        "Comment",
        backref=db.backref("child_comments", cascade="all, delete-orphan"),
        foreign_keys=[parent_id],
        remote_side=[id],
    )  # 父评论，自引用

    replied_id = db.Column(
        db.Integer, db.ForeignKey("mz_article_comment.id", ondelete="CASCADE")
    )  # 被回复的评论id，外键
    replied_comment = db.relationship(
        "Comment",
        backref=db.backref("reply_comments", cascade="all, delete-orphan"),
        foreign_keys=[replied_id],
        remote_side=[id],
    )  # 被回复的评论，自引用

    @classmethod
    def query_by_uid(cls, user_id: int, page: int, per_page: int):
        """分页查询指定用户发布的评论，根据评论创建时间，降序排列

        :param user_id: 用户id
        :param page: 当前的页码
        :param per_page: 每页的评论数
        """
        return (
            cls.query.filter_by(from_uid=user_id)
            .order_by(Comment.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_received_by_uid(cls, received_uid: int, page: int, per_page: int):
        """分页查询指定用户收到的评论，根据评论创建时间，降序排列

        :param received_uid: 收到评论的用户id
        :param page: 当前的页码
        :param per_page: 每页的评论数
        """
        return (
            cls.query.filter_by(to_uid=received_uid)
            .order_by(Comment.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象


class Like(db.Model, BaseModel):
    """文章喜欢表"""

    __tablename__ = "mz_article_like"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    status = db.Column(db.Integer, default=0)  # 喜欢状态  0-取消喜欢 1-有效喜欢，未读 2-已读
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 创建时间
    update_time = db.Column(db.BigInteger)  # 最近一次的更新时间

    article_id = db.Column(
        db.Integer, db.ForeignKey("mz_article.id"), nullable=False
    )  # 文章id，外键
    article = db.relationship(
        "Article",
        backref=db.backref("likes", lazy="joined", cascade="all, delete-orphan"),
    )  # 喜欢的文章

    from_uid = db.Column(
        db.Integer, db.ForeignKey("mz_user.id", ondelete="CASCADE")
    )  # 喜欢用户的id，外键
    from_user = db.relationship(
        "User",
        backref=db.backref("likes", lazy="dynamic", cascade="all, delete-orphan"),
        foreign_keys=[from_uid],
    )  # 喜欢的用户

    to_uid = db.Column(
        db.Integer, db.ForeignKey("mz_user.id", ondelete="CASCADE")
    )  # 收到喜欢的用户id，外键
    to_user = db.relationship(
        "User",
        backref=db.backref(
            "received_likes", lazy="dynamic", cascade="all, delete-orphan"
        ),
        foreign_keys=[to_uid],
    )  # 收到喜欢的用户

    @classmethod
    def query_by_aid(cls, article_id: int, user_id: int):
        """根据文章id查询

        :param article_id: 文章id
        :param user_id: 用户id
        """
        return cls.query.filter_by(article_id=article_id, from_uid=user_id).first()

    @classmethod
    def query_by_uid(cls, user_id: int, page: int, per_page: int):
        """分页查询指定用户的喜欢，根据喜欢创建时间，降序排列

        :param user_id: 用户id
        :param page: 当前的页码
        :param per_page: 每页的喜欢数
        """
        return (
            cls.query.filter_by(from_uid=user_id)
            .order_by(Like.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象

    @classmethod
    def query_received_by_uid(cls, received_uid: int, page: int, per_page: int):
        """分页查询收到的喜欢，根据喜欢创建时间，降序排列

        :param received_uid: 收到喜欢的用户id
        :param page: 当前的页码
        :param per_page: 每页的喜欢数
        """
        return (
            cls.query.filter_by(to_uid=received_uid)
            .order_by(Like.create_time.desc())
            .paginate(page=page, per_page=per_page)
        )  # 创建分页器对象
