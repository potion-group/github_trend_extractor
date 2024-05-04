from typing import Tuple


def return_none_if_raise(func):
    def wrapper(*arg, **kwargs):
        try:
            return func(*arg, **kwargs)
        except:
            return None

    return wrapper


class SoupInfoPreproc:

    def __init__(self, soup) -> None:
        self.soup = soup

    @return_none_if_raise
    def _extract_basic_info(self) -> Tuple[str, str]:
        owner, _, name = self.soup.find("a", class_="Link").text.split()
        return owner, name

    @return_none_if_raise
    def _extract_desc(self):
        desc = self.soup.find(
            "p", class_="col-9 color-fg-muted my-1 pr-4"
        ).text.strip()
        return desc

    @return_none_if_raise
    def _extract_planguage(self):
        planguage = self.soup.find(
            "span", itemprop="programmingLanguage"
        ).text.strip()
        return planguage

    @return_none_if_raise
    def _extract_total_star(self, owner, name):
        total_star = self.soup.find(
            "a",
            href=f"/{owner}/{name}/stargazers",
        ).text.strip()
        return total_star

    @return_none_if_raise
    def _extract_total_folk(self, owner, name):
        total_folk = self.soup.find(
            "a",
            href=f"/{owner}/{name}/forks",
        ).text.strip()
        return total_folk

    @return_none_if_raise
    def _extract_trending_star(self):
        trending_star = self.soup.find(
            "span",
            class_="d-inline-block float-sm-right",
        ).text.strip()
        return trending_star

    def __call__(self):
        owner, name = self._extract_basic_info()
        desc = self._extract_desc()
        plang = self._extract_planguage()
        total_star = self._extract_total_star(owner, name)
        total_folk = self._extract_total_folk(owner, name)
        trending_star = self._extract_trending_star()

        return {
            "owner": owner,
            "name": name,
            "desc": desc,
            "plang": plang,
            "total_star": total_star,
            "total_folk": total_folk,
            "trending_star": trending_star,
        }
