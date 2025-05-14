from app.exceptions import ZvuksException


class AlbumCreateException(ZvuksException):
    pass


class SongCreateException(ZvuksException):
    pass


class StatsException(ZvuksException):
    pass
