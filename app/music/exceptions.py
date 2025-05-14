from app.exceptions import ZvuksException


class AlbumCreateException(ZvuksException):
    pass


class SongCreateException(ZvuksException):
    pass


class SongReadException(ZvuksException):
    pass


class SongUpdateException(ZvuksException):
    pass


class StatsException(ZvuksException):
    pass
