from matchers import And, HasAtLeast, PlaysIn, All, HasFewerThan

EMPTY = 0

class QueryBuilder:
    def __init__(self, query = None):
        if query is None:
            query = []
        self.query = query

    def has_at_least(self, value, attribute):
        new_query = self.query + [HasAtLeast(value, attribute)]
        return QueryBuilder(new_query)

    def plays_in(self, team):
        new_query = self.query + [PlaysIn(team)]
        return QueryBuilder(new_query)
    
    def has_fewer_than(self, value, attribute):
        new_query = self.query + [HasFewerThan(value, attribute)]
        return QueryBuilder(new_query)

    def build(self):
        if len(self.query) == EMPTY:
            return All(all)
        return And(*self.query)