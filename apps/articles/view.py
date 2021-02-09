
from flask import g

from bases.exceptions import ParamsError, VerifyError
from bases.viewhandler import ApiViewHandler
from models import WeChatArticle, WeChatPublicAccount
from utils.decorators import login_required, params_required


class PublicAccountListAPI(ApiViewHandler):

    @login_required
    def get(self):
        accounts = WeChatPublicAccount.get_public_accounts()
        return accounts


class PublicAccountAPI(ApiViewHandler):

    @login_required
    @params_required(*['wxid'])
    def get(self):
        # print(self.input.wxid)
        account_detail = WeChatPublicAccount.get_public_account_detail(self.input.wxid)
        return account_detail


class ArticleCountAPI(ApiViewHandler):

    @login_required
    def post(self):
        wxids = getattr(self.input, 'wxids')
        start_time = getattr(self.input, 'start_time')
        end_time = getattr(self.input, 'end_time')

        print(f'wxids: {wxids}')

        articles = WeChatArticle.get_article_count(wxids, start_time, end_time)
        return articles


class ArticleAPI(ApiViewHandler):

    @login_required
    @params_required(*['page_index', 'page_size'])
    def post(self):
        page_index = int(self.input.page_index)
        page_size = int(self.input.page_size)

        if page_index < 0 or page_size <= 0 and page_size > 100:
            raise VerifyError('查询参数不合法！')

        wxids = getattr(self.input, 'wxids')
        start_time = getattr(self.input, 'start_time')
        end_time = getattr(self.input, 'end_time')

        print(f'wxids: {wxids}')

        articles = WeChatArticle.get_articles(wxids, page_index, page_size, start_time, end_time)
        return articles
