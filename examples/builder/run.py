from examples.builder.params import FormParams


if __name__ == '__main__':
    form = FormParams().set_user_id(124243224).set_github_handle('kailashnath/python-patternlib')\
                .set_url('https://github.com/kailashnath/python-patternlib')\
                .set_repo_type('public')

    print form.params

