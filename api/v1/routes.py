from api.v1 import medication_repo


@medication_repo.route('/', defaults={'page': 'index'})
@medication_repo.route('/<page>')
def show(page):
    return page
