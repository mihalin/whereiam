import peewee
from datetime import datetime


db = peewee.SqliteDatabase("data.db")


class Point(peewee.Model):
    date = peewee.DateTimeField()
    comment = peewee.TextField()
    x = peewee.TextField()
    y = peewee.TextField()
    is_newline = peewee.BooleanField(default=False)

    class Meta:
        database = db


def default_point_factory() -> Point:
    return Point(x="55.76", y="37.64", date=datetime.now(), comment=str(datetime.now()), is_newline=True)


if __name__ == '__main__':
    Point.create_table()
    point = Point(date=datetime.now(), comment="foo", x="ix", y="yg")
    point.save()

    for point in Point.select():
        print(point.get().x)

