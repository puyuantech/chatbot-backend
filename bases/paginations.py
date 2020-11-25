from sqlalchemy import text


class BasePagination:
    def __init__(self, page=1, page_size=10, ordering=None):
        self.page = int(page)
        self.page_size = int(page_size)
        self.ordering = ordering if ordering else []
        self.convert_ordering()

    def paginate(self, query):
        raise NotImplementedError

    def convert_ordering(self):
        raise NotImplementedError


class SQLPagination(BasePagination):

    def paginate(self, query, call_back=None):
        if self.ordering:
            query = query.order_by(*[text(i) for i in self.ordering])
        instances = query.limit(self.page_size).offset((self.page - 1) * self.page_size).all()
        if call_back:
            results = call_back(instances)
        else:
            results = [i.to_dict() for i in instances]
        return {
            'page': self.page,
            'page_size': self.page_size,
            'count': query.count(),
            'results': results,
        }

    def convert_ordering(self):
        for i in range(len(self.ordering)):
            if self.ordering[i].startswith('-'):
                self.ordering[i] = '{} {}'.format(self.ordering[i][1:], 'DESC')
            else:
                self.ordering[i] = '{} {}'.format(self.ordering[i], 'ASC')

