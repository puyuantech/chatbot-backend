from bases.exceptions import AuthError
from models import Token


class TokenAuthentication:
    """
    基于自定义的AuthToken做的Authentication

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    model = Token
    keyword = 'Token'

    @staticmethod
    def get_authorization_header(request):
        """
        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.headers.get('Authorization', '')
        if not isinstance(auth, str):
            auth = auth.decode()
        return auth

    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower():
            return None, None

        if len(auth) == 1:
            raise AuthError('无Token信息')
        elif len(auth) > 2:
            raise AuthError('Token格式不正确，不能包含空格')

        try:
            token = auth[1]
        except UnicodeError:
            raise AuthError('Token包含特殊字符')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        token = Token.filter_by_query(
            key=key,
        ).one_or_none()

        if not token:
            print('Token不存在 ' + key)
            raise AuthError('Token无效')

        if not token.is_valid():
            print('Token过期 ' + key)
            raise AuthError('Token已过期')

        if token.user.is_deleted:
            print('用户inactive ')
            raise AuthError('用户无效')

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword
