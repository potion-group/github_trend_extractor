#
import time
import datetime as dt

#
import pandas as pd

#
import airflow
from airflow import DAG
from airflow.decorators import task

#
from github_trend_extractor import GithubTrendExtractor, SoupInfoPreproc
from github_trend_extractor import GithubTrendPrivate
from common import DBController

#
p_langs = [
    "",
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "rust",
    "go",
    "php",
    "ruby",
    "scala",
    "kotlin",
]
params = {"since": "daily"}


#
def get_trending_repos_soup(p_lang):
    get_trending_repos_soup = GithubTrendExtractor(params, p_lang)
    return get_trending_repos_soup


with DAG(
    dag_id="github_trend_daily",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    tags=["github_trend"],
) as dag:

    @task
    def extract():
        trending_repos_soup_list = list()
        for p_lang in p_langs:
            trending_repos_soup = get_trending_repos_soup(p_lang)
            time.sleep(3)
            trending_repos_soup_list.append(trending_repos_soup)
        return trending_repos_soup_list

    @task
    def preproc(trending_repos_soup_list):
        preproc_soups = list()
        for trending_repos_soup in trending_repos_soup_list:
            for trending_repo_soup in trending_repos_soup:
                preproc_soups.append(SoupInfoPreproc(trending_repo_soup)())
        return preproc_soups

    @task
    def format2df(result):
        df = pd.DataFrame(result)
        return df

    @task
    def df2db(df, db_controller):
        result = df.to_sql(
            name="github_trend_daily",
            con=db_controller.engine,
            if_exists="append",
        )
        return result

    db_controller = DBController(GithubTrendPrivate.db_cfg)

    trending_repos_soup_list = extract()
    preproc_soups = preproc(trending_repos_soup_list)
    df = format2df(preproc_soups)
    result = df2db(df, db_controller)
