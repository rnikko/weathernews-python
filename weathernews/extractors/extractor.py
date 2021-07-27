from abc import abstractmethod, ABC


class Extractor(ABC):
    """Extract data from BeautifulSoup soup."""
    @abstractmethod
    def extract(soup):
        pass
