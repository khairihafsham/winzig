from sqlalchemy import Column, String, TIMESTAMP, Integer, func

from winzig.database import Base


class URLMap(Base):
    """
    declaration of url_maps table. the table records the mapping of the
    original url to the generated id
    """
    __tablename__ = "url_maps"

    id = Column(Integer, primary_key=True)
    url = Column(String(2083), unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(True), default=func.now(), nullable=False)

    def __repr__(self):
        return "<URLMap(id=%d, url='%s')>" % (self.id, self.url)
